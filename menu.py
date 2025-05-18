import requests

def menu_usuario(url):
    thread = []
    start = """Selecciona una opción:
1. Hacer una consulta
2. Hacer un pedido
3. Salir"""
    while True:
        match thread:
            case []:
                print(start)
            case [1]:
                print("""Consultar...
1. El catálogo
2. Un pedido
3. Atrás""")
            case [1, 1]:
                print('--- Datos ---') #datos de los articulos (data.get_articulos())
                info = requests.get(f'{url}/articulos')
                print(info)
                thread = []
                continue
            case [1, 2]:
                cod = input('Código del pedido: ') 
                info = requests.get(f'{url}/pedidos/{cod}') #datos del pedido suministrado (data.get_paquete_by_codigo(cod))
                print(info.text)
                thread = []
                continue
            case [1, 3]:
                thread.pop()
                thread.pop()
                continue
            case [2]:
                direccion = input('Dirección: ')
                requests.post(f'{url}/paquetes', json={'direccion': direccion})
                thread = []
                continue
            case [3]:
                thread = []
                break

            case _:
                print('Introduce una opción válida')
                thread.pop()
                continue

        op = input('Selección: ')
        try:
            op = int(op)
            thread.append(op)
        except:
            print('Introduce una selección válida.')
            continue
        
def menu_vendedor(url, email):
    thread = []
    start = """Selecciona una opción:
1. Realizar gestiones
2. Ver estadísticas
3. Salir"""
    while True:
        match thread:
            case []:
                print(start)
            case [1]:
                print("""Gestionar...
1. Artículos
2. Repartidores
3. Atrás""")
            case [1, 1]:
                print("""Gestionar artículos:
1. Añadir un artículo
2. Eliminar un artículo
3. Atrás""")
            case [1, 1, 1]:
                while True:
                        try:
                            nom = input('Nombre: ')
                            cant = int(input('Cantidad: '))
                            desc = input('Descripción: ')
                            break
                        except ValueError:
                            print('Ha de ser un número entero.')
                            continue
                requests.post(f'{url}/articulo', json={"nombre": nom, "cantidad": cant, "proveedor": email, "descripcion": desc})
                thread.pop()
                continue
            case [1, 1, 2]:
                while True:
                        try:
                            cod = int(input('Código: '))
                            break
                        except ValueError:
                            print('Ha de ser un número.')
                requests.delete(f'{url}/articulo', json={'codigo': cod})
                thread.pop()
                continue

            case [1, 1, 3]:
                thread.pop()
                thread.pop()
                continue

            case [1, 2]:
                print("""Gestionar repartidores:
1. Añadir un repartidor
2. Eliminar un repartidor
3. Atrás""")
                
            case [1, 2, 1]:
                while True:
                        try:
                            nom = input('Nombre: ')
                            tlf = input('Telefono: ')
                            prov = input('Provincia: ')
                            vehiculo = input('Vehiculo: ')
                            break
                        except ValueError:
                            print('Ha de ser un número entero.')
                            continue
                requests.post(f'{url}/repartidores', json={'nombre': nom, 'telefono': tlf, 'provincia': prov, 'vehiculo': vehiculo})
                thread.pop()
                continue

            case [1, 2, 2]:
                cod = input('DNI: ')
                requests.delete(f'{url}/repartidores', json={"id": id})
                thread.pop()
                continue

            case [1, 2, 3]:
                thread.pop()
                thread.pop()
                continue
                
            case [1, 3]:
                thread.pop()
                thread.pop()
                continue
                
            case [2]:
                print("""Ver estadísticas:
1. Artículos
2. Repartidores
3. Estadísticas personalizadas
4. Atrás""")
                
            case [2, 1]:
                res = requests.get(f'{url}/articulos')
                print(res.json())
                thread.pop()
                continue

            case [2, 2]:
                res = requests.get(f'{url}/repartidores')
                print(res.json())
                thread.pop()
                continue

            case [2, 3]:
                res = requests.get(f'{url}/stats')
                print(res.text)
                thread.pop()
                continue

            case [2, 4]:
                thread.pop()
                thread.pop()
                continue

            case [3]:
                thread = []
                break

            case _:
                print('Introduce una opción válida')
                thread.pop()
                continue

        op = input('Selección: ')
        try:
            op = int(op)
            thread.append(op)
        except:
            print('Introduce una selección válida.')
            continue