import random

repartidores=3
tiempo_total=60
prob_paquete=0.3
tiempo_min=5
tiempo_max=15
def simular():
    print("simulación iniciada")
    repartidores_libre = repartidores
    paquetes_espera = 0
    entregas = []
    total_entregados = 0
    for minuto in range(tiempo_total):
        print(f"\nMinuto {minuto + 1}")
        for i in range(len(entregas)-1, -1, -1):
            entregas[i] -= 1
            if entregas[i] <= 0:
                repartidores_libre += 1
                total_entregados += 1
                print(f"Paquete entregado. Repartidores libres: {repartidores_libre}")
                del entregas[i]
        if random.random() < prob_paquete:
            paquetes_espera += 1
            print(f"Llegó paquete nuevo. Pendientes: {paquetes_espera}")
        while paquetes_espera > 0 and repartidores_libre > 0:
            paquetes_espera -= 1
            repartidores_libre -= 1
            tiempo = random.randint(tiempo_min, tiempo_max)
            entregas.append(tiempo)
            print(f"Repartidor asignado. Tiempo estimado: {tiempo} min")  
    print("\n--- Fin ---")
    print(f"Paquetes entregados: {total_entregados}")
    print(f"Paquetes sin entregar: {paquetes_espera}")

if __name__ == "__main__":
    simular()