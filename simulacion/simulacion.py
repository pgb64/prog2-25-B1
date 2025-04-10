# simulacion_simple.py
import random
import time

# --- Parámetros Configurables ---
NUM_REPARTIDORES = 3       # ¿Cuántos repartidores tenemos?
TIEMPO_SIMULACION_MINUTOS = 60 # ¿Cuántos minutos simulamos? (Ej: 1 hora)
PROBABILIDAD_NUEVO_PAQUETE = 0.3 # Probabilidad (0 a 1) de que llegue un paquete CADA MINUTO
TIEMPO_ENTREGA_MIN = 5      # Tiempo MÍNIMO que tarda una entrega (minutos)
TIEMPO_ENTREGA_MAX = 15     # Tiempo MÁXIMO que tarda una entrega (minutos)
# --- Fin de Parámetros ---

def ejecutar_simulacion_simple():
    """
    Ejecuta una simulación muy básica de llegada y entrega de paquetes.
    Se enfoca en la claridad del proceso.
    """
    print("--- Iniciando Simulación Simple ---")
    print(f"Configuración: {NUM_REPARTIDORES} repartidores, {TIEMPO_SIMULACION_MINUTOS} minutos de simulación.")

    # Estado inicial
    repartidores_libres = NUM_REPARTIDORES
    paquetes_pendientes = 0           # Contador de paquetes esperando repartidor
    entregas_en_curso = []            # Lista para rastrear cuánto le falta a cada entrega activa
                                      # Guardaremos los minutos restantes para cada entrega: [5, 12, 8]
    paquetes_creados_total = 0
    paquetes_entregados_total = 0

    # Bucle principal: Avanza minuto a minuto
    for minuto_actual in range(TIEMPO_SIMULACION_MINUTOS):
        print(f"\n----- Minuto {minuto_actual + 1} -----")

        # 1. Actualizar entregas en curso (pasa 1 minuto)
        entregas_terminadas_este_minuto = 0
        # Usamos una copia de la lista para poder modificarla mientras iteramos
        for i in range(len(entregas_en_curso) - 1, -1, -1): # Iterar hacia atrás para poder eliminar
            entregas_en_curso[i] -= 1 # Reducir un minuto al tiempo restante
            if entregas_en_curso[i] <= 0:
                # ¡Entrega completada!
                entregas_terminadas_este_minuto += 1
                paquetes_entregados_total += 1
                del entregas_en_curso[i] # Quitarla de la lista de en curso

        # Si terminaron entregas, los repartidores se liberan
        if entregas_terminadas_este_minuto > 0:
            repartidores_libres += entregas_terminadas_este_minuto
            print(f"  Entregas completadas este minuto: {entregas_terminadas_este_minuto}. Repartidores libres ahora: {repartidores_libres}")

        # 2. ¿Llega un nuevo paquete?
        if random.random() < PROBABILIDAD_NUEVO_PAQUETE:
            paquetes_pendientes += 1
            paquetes_creados_total += 1
            print(f"  ¡Nuevo paquete ha llegado! Pendientes: {paquetes_pendientes}")

        # 3. Asignar paquetes pendientes a repartidores libres
        paquetes_asignados_este_minuto = 0
        while paquetes_pendientes > 0 and repartidores_libres > 0:
            # Hay paquete esperando y repartidor libre: ¡asignar!
            paquetes_pendientes -= 1
            repartidores_libres -= 1
            paquetes_asignados_este_minuto += 1

            # Decidir cuánto tardará esta entrega (aleatorio entre MIN y MAX)
            tiempo_esta_entrega = random.randint(TIEMPO_ENTREGA_MIN, TIEMPO_ENTREGA_MAX)
            entregas_en_curso.append(tiempo_esta_entrega)

        if paquetes_asignados_este_minuto > 0:
             print(f"  Asignados {paquetes_asignados_este_minuto} paquetes a repartidores. Quedan libres: {repartidores_libres}. En curso: {len(entregas_en_curso)}")

        # Pequeña pausa para poder leer la salida (opcional)
        # time.sleep(0.1)

    # Fin de la simulación
    print("\n--- Simulación Simple Finalizada ---")
    print(f"Total de paquetes creados: {paquetes_creados_total}")
    print(f"Total de paquetes entregados: {paquetes_entregados_total}")
    print(f"Paquetes que quedaron pendientes: {paquetes_pendientes}")
    print(f"Paquetes aún en entrega al finalizar: {len(entregas_en_curso)}")
    print(f"Repartidores que quedaron libres: {repartidores_libres}")

# --- Ejecutar la simulación al correr el script ---
if __name__ == "__main__":
    ejecutar_simulacion_simple()