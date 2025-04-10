# probar_simulacion.py (Modificado)
"""
Script independiente para ejecutar y probar la clase SimulacionDataDriven.
"""

from database.db import Db
# Asegúrate de importar la clase correcta
from simulacion.simulacion import SimulacionDataDriven

# --- Configuración del Escenario de Simulación ---
# La simulación ahora usará los repartidores REALES de la BD.
# Solo necesitas configurar la tasa de llegada y la duración.
PEDIDOS_POR_HORA = 15         # Tasa promedio de LLEGADA DE SOLICITUDES de artículos
DURACION_SIMULACION_HORAS = 1 # Cuántas horas simular
PASO_TIEMPO_SEGUNDOS = 15     # Resolución de la simulación
# --- Fin de la Configuración ---

def ejecutar_prueba_simulacion():
    """Función principal que configura y ejecuta la simulación data-driven."""
    print("--- Iniciando Script de Prueba de Simulación Data-Driven ---")

    try:
        db_instance = Db()
        print("Instancia de Db creada.")
    except Exception as e:
        print(f"Error al crear la instancia de Db: {e}")
        print("Asegúrate de que la estructura de directorios y archivos CSV existan en la carpeta 'data'.")
        return

    print(f"\nConfigurando simulación con:")
    print(f" - Repartidores: Reales desde la BD") # Indicamos que son los reales
    print(f" - Tasa de Solicitudes: {PEDIDOS_POR_HORA}/hora")
    print(f" - Duración: {DURACION_SIMULACION_HORAS} horas")
    print(f" - Paso de tiempo: {PASO_TIEMPO_SEGUNDOS} segundos")

    # Crear la instancia de la simulación data-driven
    sim = SimulacionDataDriven(
        db=db_instance,
        tasa_pedidos_hora=PEDIDOS_POR_HORA,
        duracion_sim_horas=DURACION_SIMULACION_HORAS
    )
    print("Instancia de SimulacionDataDriven creada.")

    # Ejecutar la simulación
    print("\n--- Ejecutando Simulación... ---")
    sim.ejecutar(paso_tiempo_seg=PASO_TIEMPO_SEGUNDOS)

    print("\n--- Script de Prueba de Simulación Finalizado ---")

if __name__ == "__main__":
    ejecutar_prueba_simulacion()