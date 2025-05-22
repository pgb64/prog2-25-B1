import requests
from mapas import ors_api, visual

def menu_usuario(url):
    thread = []
    start = """\nSelecciona una opción:
1. Hacer una consulta
2. Hacer un pedido
3. Salir"""
    while True:
        match thread:
            case []:
                print(start)
            case [1]:
                print("""\nConsultar...
1. El catálogo
2. Un pedido
3. Atrás""")
            case [1, 1]:
                print('\n--- Datos ---') #datos de los articulos (data.get_articulos())
                info = requests.get(f'{url}/articulos')
                print(info)
                thread = []
                continue
            case [1, 2]:
                cod = input('\nCódigo del pedido: ') 
                info = requests.get(f'{url}/pedidos/{cod}') #datos del pedido suministrado (data.get_paquete_by_codigo(cod))
                print(info.text)
                thread = []
                continue
            case [1, 3]:
                thread.pop()
                thread.pop()
                continue
            case [2]:
                art = input('\nCódigo del artículo: ')
                calle = input('Calle: ')
                num = input('Numero: ')
                cod_p = input('Codigo postal: ')
                provincia = input('Provincia: ')
                direccion = (calle, num, cod_p, provincia)
                requests.post(f'{url}/paquetes', json={'direccion': direccion, 'articulo': art})
                direccion = f'{calle}, {num}, {cod_p}, {provincia}'
                maps = ors_api.OpenRouteService()
                coords = maps.obtener_coords(direccion)
                try:
                    sede = maps.sede_mas_cercana(coords)
                except:
                    pass
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
    start = """\nSelecciona una opción:
1. Realizar gestiones
2. Ver estadísticas
3. Salir"""
    while True:
        match thread:
            case []:
                print(start)
            case [1]:
                print("""\nGestionar...
1. Artículos
2. Repartidores
3. Atrás""")
            case [1, 1]:
                print("""\nGestionar artículos:
1. Añadir un artículo
2. Eliminar un artículo
3. Atrás""")
            case [1, 1, 1]:
                while True:
                        try:
                            nom = input('\nNombre: ')
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
                print("""\nGestionar repartidores:
1. Añadir un repartidor
2. Eliminar un repartidor
3. Atrás""")
                
            case [1, 2, 1]:
                while True:
                        try:
                            nom = input('\nNombre: ')
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
                print("""\nVer estadísticas:
1. Artículos
2. Repartidores
3. Mostrar mapa
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
                visual.MapaGestor().mostrar_mapa_sedes()
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
                print('\nIntroduce una opción válida')
                thread.pop()
                continue

        op = input('Selección: ')
        try:
            op = int(op)
            thread.append(op)
        except:
            print('\nIntroduce una selección válida.')
            continue