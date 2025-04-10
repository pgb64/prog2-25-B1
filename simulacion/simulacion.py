import random
import math
import time
import uuid
from database.db import Db
import articulos_paquetes.paquetes as ctrl_paquetes
import articulos_paquetes.articulos as ctrl_articulos

class SimulacionDataDriven:
    """
    Gestiona una simulación del proceso de reparto basada en los datos reales
    disponibles a través de la instancia Db.

    Interactúa con los datos de artículos y repartidores existentes y simula
    la creación de paquetes y su asignación/entrega de forma probabilística.
    """

    def __init__(self, db: Db, tasa_pedidos_hora: float, duracion_sim_horas: float):
        """
        Inicializa la simulación basada en datos.

        Args:
            db (Db): Instancia del gestor de base de datos para acceder a datos reales.
            tasa_pedidos_hora (float): Número promedio de solicitudes de artículos por hora.
            duracion_sim_horas (float): Duración total de la simulación en horas.
        """
        self.db = db
        self.lambda_eventos_por_seg = tasa_pedidos_hora / 3600.0
        self.duracion_sim_seg = duracion_sim_horas * 3600.0

        self.tiempo_actual_seg = 0.0
        # Usaremos códigos de paquete para rastrear
        self.paquetes_pendientes = []
        self.paquetes_en_ruta = {}
        self.paquetes_entregados = []

        # Cargar y preparar repartidores reales
        self.repartidores = self._cargar_repartidores_reales()

        # Estadísticas
        self.total_solicitudes_generadas = 0
        self.total_paquetes_creados = 0
        self.tiempos_espera_total_seg = 0.0
        self.tiempos_entrega_total_seg = 0.0
        self.fallos_creacion_paquete = 0

    def _cargar_repartidores_reales(self) -> dict:
        """Carga los repartidores desde la BD y prepara su estado para la simulación."""
        repartidores_activos = {}
        try:
            lista_repartidores_db = self.db.get_repartidores()
            if not lista_repartidores_db:
                 print("ADVERTENCIA: No se encontraron repartidores en la base de datos.")
                 return {}

            for rep_data in lista_repartidores_db:
                repartidor_id = rep_data.get('id')
                if repartidor_id:
                     repartidores_activos[repartidor_id] = {
                         'estado': 'disponible',
                         'tiempo_fin_entrega': None,
                         'data': rep_data
                     }
                else:
                     print(f"ADVERTENCIA: Repartidor encontrado sin 'id' en los datos: {rep_data}")

            print(f"Simulación iniciada con {len(repartidores_activos)} repartidores cargados desde la BD.")

        except Exception as e:
            print(f"Error cargando repartidores desde la BD: {e}")
            return {}

        return repartidores_activos

    def _generar_evento_solicitud(self, delta_tiempo_seg: float):
        """Determina si ocurre un evento de solicitud y, si es así, intenta crear un paquete."""
        prob_evento = 1 - math.exp(-self.lambda_eventos_por_seg * delta_tiempo_seg)

        if random.random() < prob_evento:
            self.total_solicitudes_generadas += 1
            self._intentar_crear_paquete()


    def _intentar_crear_paquete(self):
        """Selecciona un artículo disponible y usa el controlador para crear un paquete."""
        try:
            # 1. Obtener artículos disponibles (con stock > 0)
            articulos_db = self.db.get_articulos()
            articulos_disponibles = [
                a for a in articulos_db
                if a and 'cantidad' in a and int(a.get('cantidad', 0)) > 0 and 'codigo' in a and 'nombre' in a
            ]


            if not articulos_disponibles:
                self.fallos_creacion_paquete += 1
                return

            articulo_seleccionado = random.choice(articulos_disponibles)
            codigo_articulo = articulo_seleccionado['codigo']
            nombre_articulo = articulo_seleccionado['nombre']

            codigo_paquete_nuevo = f"SIM-{uuid.uuid4().hex[:8].upper()}"
            direccion_dummy = f"Calle Ficticia {random.randint(1, 100)}, Ciudad Sim"
            usuario_dummy = f"UserSim_{random.randint(1000,9999)}"

            # Crear el paquete usando el controlador
            resultado_creacion = self.db.add_paquete(
                 codigo_paquete=codigo_paquete_nuevo,
                 direccion=direccion_dummy,
                 usuario=usuario_dummy,
                 contenido=codigo_articulo
            )

            if resultado_creacion == 201 :
                self.total_paquetes_creados += 1
                codigo_creado = codigo_paquete_nuevo
                self.paquetes_pendientes.append(codigo_creado)
                print(f"T={self.tiempo_actual_seg:.2f}s: Paquete '{codigo_creado}' creado (articulo: {nombre_articulo} [{codigo_articulo}]) y añadido a pendientes.")

                # No estamos decrementando el stock del artículo en la BD aquí
                # para evitar múltiples escrituras en el CSV durante la simulación.
                # La comprobación de stock > 0 al principio es la que limita.
                # Si se requiere actualizar el stock real, se necesitaría db.update_articulo_cantidad().

            elif resultado_creacion == 409:
                 print(f"T={self.tiempo_actual_seg:.2f}s: Fallo al crear paquete - Código duplicado: {codigo_paquete_nuevo}")
                 self.fallos_creacion_paquete += 1
            else:
                 print(f"T={self.tiempo_actual_seg:.2f}s: Fallo al añadir paquete a la BD para artículo {codigo_articulo}. Código de estado: {resultado_creacion}")
                 self.fallos_creacion_paquete += 1

        except Exception as e:
            print(f"Error grave en _intentar_crear_paquete: {e}")
            self.fallos_creacion_paquete += 1


    def _asignar_paquetes(self):
        """Asigna paquetes pendientes a repartidores disponibles."""
        if not self.paquetes_pendientes:
            return

        repartidores_disp_ids = [rid for rid, data in self.repartidores.items() if data['estado'] == 'disponible']

        if not repartidores_disp_ids:
            return

        # Iteramos mientras haya paquetes pendientes y repartidores disponibles
        while self.paquetes_pendientes and repartidores_disp_ids:
            repartidor_id = random.choice(repartidores_disp_ids)
            codigo_paquete = self.paquetes_pendientes.pop(0)

            media_entrega_seg = 1800
            std_entrega_seg = 600
            tiempo_entrega = max(60, random.normalvariate(media_entrega_seg, std_entrega_seg))

            # Actualizar estado del repartidor
            self.repartidores[repartidor_id]['estado'] = 'ocupado'
            self.repartidores[repartidor_id]['tiempo_fin_entrega'] = self.tiempo_actual_seg + tiempo_entrega

            # Mover paquete a 'en ruta'
            self.paquetes_en_ruta[codigo_paquete] = repartidor_id

            # Quitar el repartidor de la lista de disponibles para esta ronda de asignación
            repartidores_disp_ids.remove(repartidor_id)

            print(f"T={self.tiempo_actual_seg:.2f}s: Paquete {codigo_paquete} asignado a Repartidor {repartidor_id}. Entrega estimada en {tiempo_entrega/60.0:.1f} min.")


    def _actualizar_estado_repartidores(self):
        """Verifica si los repartidores ocupados han terminado su entrega."""
        repartidores_que_terminan = []
        for repartidor_id, data in self.repartidores.items():
            if data['estado'] == 'ocupado' and data['tiempo_fin_entrega'] is not None and self.tiempo_actual_seg >= data['tiempo_fin_entrega']:
                repartidores_que_terminan.append(repartidor_id)

        for repartidor_id in repartidores_que_terminan:
            # Encontrar qué paquete entregó iterando sobre paquetes_en_ruta
            paquete_entregado_codigo = None
            for codigo, rid in self.paquetes_en_ruta.items():
                if rid == repartidor_id:
                    paquete_entregado_codigo = codigo
                    break

            if paquete_entregado_codigo:
                print(f"T={self.tiempo_actual_seg:.2f}s: Repartidor {repartidor_id} ha terminado entrega del paquete {paquete_entregado_codigo} y está disponible.")
                # Mover paquete de en_ruta a entregados
                del self.paquetes_en_ruta[paquete_entregado_codigo]
                self.paquetes_entregados.append(paquete_entregado_codigo)

            else:
                 # Esto no debería pasar si la lógica es correcta, pero por si acaso
                 print(f"ADVERTENCIA: Repartidor {repartidor_id} terminó pero no se encontró su paquete en ruta.")


            # Marcar repartidor como disponible y resetear su tiempo
            self.repartidores[repartidor_id]['estado'] = 'disponible'
            self.repartidores[repartidor_id]['tiempo_fin_entrega'] = None


    def ejecutar(self, paso_tiempo_seg: float = 10.0):
        """Ejecuta la simulación data-driven paso a paso."""
        if not self.repartidores:
            print("ERROR: No hay repartidores cargados. No se puede ejecutar la simulación.")
            return

        print(f"\n--- Iniciando Simulación Data-Driven (Duración: {self.duracion_sim_seg / 3600.0:.2f} horas, Paso: {paso_tiempo_seg}s) ---")

        while self.tiempo_actual_seg < self.duracion_sim_seg:
            # Generar eventos de solicitud y potencialmente crear paquetes
            self._generar_evento_solicitud(paso_tiempo_seg)

            # Actualizar estado de repartidores (ver si terminaron entregas)
            self._actualizar_estado_repartidores()

            # asignar paquetes pendientes a repartidores disponibles
            self._asignar_paquetes()

            # avanzar el tiempo
            self.tiempo_actual_seg += paso_tiempo_seg


        print(f"\n--- Simulación Finalizada (Tiempo total: {self.tiempo_actual_seg / 3600.0:.2f} horas) ---")
        self.mostrar_resultados()

    def mostrar_resultados(self):
        """Muestra las estadísticas finales de la simulación."""
        print("\n--- Resultados de la Simulación Data-Driven ---")
        print(f"Total de solicitudes de artículo generadas: {self.total_solicitudes_generadas}")
        print(f"Total de paquetes creados exitosamente: {self.total_paquetes_creados}")
        print(f"Intentos fallidos de creación de paquete (sin stock/error): {self.fallos_creacion_paquete}")
        print(f"Paquetes asignados y entregados: {len(self.paquetes_entregados)}")
        print(f"Paquetes que quedaron en ruta al finalizar: {len(self.paquetes_en_ruta)}")
        print(f"Paquetes que quedaron pendientes de asignación: {len(self.paquetes_pendientes)}")
        print(f"\nEstado final de los {len(self.repartidores)} repartidores:")
        ocupados = sum(1 for r in self.repartidores.values() if r['estado'] == 'ocupado')
        disponibles = len(self.repartidores) - ocupados
        print(f" - Disponibles: {disponibles}")
        print(f" - Ocupados: {ocupados}")