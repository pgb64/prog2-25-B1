"""
Script de simulación de reparto de paquetes

Este módulo proporciona una función para ejecutar una simulación básica
basada en eventos discretos (paso de minutos). No utiliza clases complejas
ni depende de la base de datos o de otros módulos del proyecto. Su objetivo
principal es ilustrar el concepto de simulación de forma clara y sencilla,
utilizando parámetros globales configurables.
"""

import random
import time

"""
Esta es una clara simulación de un sistema de reparto ideal y totalmente funcional
donde los repartidores están disponibles para entregar paquetes a medida que llegan.
Esto se cambiaría cuando toda la lógica de reparto esté funcional y ya no serían valores
estáticos sino vendrían siguendo la lógica de la app
"""


NUM_REPARTIDORES: int = 3 # Número total de repartidores disponibles en la simulación.
TIEMPO_SIMULACION_MINUTOS: int = 60 # Duración total de la simulación en minutos.
PROBABILIDAD_NUEVO_PAQUETE: float = 0.3 # Probabilidad (entre 0.0 y 1.0) de que un nuevo paquete llegue en cada minuto.
TIEMPO_ENTREGA_MIN: int = 5      # Tiempo mínimo (en minutos) que tarda un repartidor en completar una entrega.
TIEMPO_ENTREGA_MAX: int = 15     # Tiempo máximo (en minutos) que tarda un repartidor en completar una entrega.

def ejecutar_simulacion_simple():
    """
    Ejecuta el bucle principal de la simulación simple de reparto.

    Avanza la simulación minuto a minuto durante el tiempo total especificado
    en `TIEMPO_SIMULACION_MINUTOS`. En cada minuto, gestiona:
    1. La finalización de entregas que estaban en curso.
    2. La posible llegada aleatoria de nuevos paquetes (basado en `PROBABILIDAD_NUEVO_PAQUETE`).
    3. La asignación de paquetes que están pendientes a repartidores que están libres (`NUM_REPARTIDORES`).
    Los tiempos de entrega individuales se calculan aleatoriamente dentro del rango
    definido por `TIEMPO_ENTREGA_MIN` y `TIEMPO_ENTREGA_MAX`.

    Utiliza las constantes globales definidas al inicio de este módulo para su configuración.
    Imprime el estado de la simulación en cada paso (minuto) y un resumen final
    de resultados en la consola estándar. Esta función no retorna ningún valor.
    """
    print("--- Iniciando Simulación ---")
    print(f"Configuración: {NUM_REPARTIDORES} repartidores, {TIEMPO_SIMULACION_MINUTOS} minutos de simulación.")

    repartidores_libres: int = NUM_REPARTIDORES # Contador de repartidores actualmente sin asignación.
    paquetes_pendientes: int = 0           # Contador de paquetes que han llegado pero esperan asignación.
    entregas_en_curso: list[int] = []      # Lista que almacena los minutos restantes para cada entrega activa.
 
    paquetes_creados_total: int = 0
    paquetes_entregados_total: int = 0

    for minuto_actual in range(TIEMPO_SIMULACION_MINUTOS):
        print(f"\n----- Minuto {minuto_actual + 1} -----")

        # Actualizar estado de las entregas en curso
        # Se reduce en 1 el tiempo restante de cada entrega activa.
        entregas_terminadas_este_minuto: int = 0
        # Iteramos hacia atrás para poder eliminar elementos de la lista sin afectar índices posteriores.
        for i in range(len(entregas_en_curso) - 1, -1, -1):
            entregas_en_curso[i] -= 1 # Un minuto ha pasado para esta entrega.
            if entregas_en_curso[i] <= 0:
                # Esta entrega ha terminado.
                entregas_terminadas_este_minuto += 1
                paquetes_entregados_total += 1
                del entregas_en_curso[i] # Eliminar la entrega completada de la lista.

        # Si alguna entrega terminó, los repartidores correspondientes quedan libres.
        if entregas_terminadas_este_minuto > 0:
            repartidores_libres += entregas_terminadas_este_minuto
            print(f"  Entregas completadas este minuto: {entregas_terminadas_este_minuto}. Repartidores libres ahora: {repartidores_libres}")

        # Simular la posible llegada de un nuevo paquete.
        # Se genera un número aleatorio; si es menor que la probabilidad, llega un paquete.
        if random.random() < PROBABILIDAD_NUEVO_PAQUETE:
            paquetes_pendientes += 1
            paquetes_creados_total += 1
            print(f"  ¡Nuevo paquete ha llegado, Pendientes: {paquetes_pendientes}")

        # Intentar asignar paquetes pendientes a repartidores libres.
        paquetes_asignados_este_minuto: int = 0
        # Se asignan paquetes mientras haya pendientes Y haya repartidores libres.
        while paquetes_pendientes > 0 and repartidores_libres > 0:
            # Realizar una asignación:
            paquetes_pendientes -= 1           # Un paquete menos en espera.
            repartidores_libres -= 1            # Un repartidor menos libre.
            paquetes_asignados_este_minuto += 1

            # Calcular aleatoriamente cuánto tiempo tardará esta nueva entrega.
            tiempo_esta_entrega: int = random.randint(TIEMPO_ENTREGA_MIN, TIEMPO_ENTREGA_MAX)
            # Añadir el tiempo restante de esta nueva entrega a la lista de seguimiento.
            entregas_en_curso.append(tiempo_esta_entrega)

        # Informar si se realizaron asignaciones en este minuto.
        if paquetes_asignados_este_minuto > 0:
             print(f"  Asignados {paquetes_asignados_este_minuto} paquetes a repartidores. Quedan libres: {repartidores_libres}. En curso: {len(entregas_en_curso)}")


    print("\n--- Simulación Finalizada ---")
    print(f"Total de paquetes creados: {paquetes_creados_total}")
    print(f"Total de paquetes entregados: {paquetes_entregados_total}")
    print(f"Paquetes que quedaron pendientes (sin asignar): {paquetes_pendientes}")
    print(f"Paquetes aún en entrega al finalizar la simulación: {len(entregas_en_curso)}")
    print(f"Repartidores que quedaron libres al finalizar: {repartidores_libres}")

if __name__ == "__main__":
    ejecutar_simulacion_simple()