

def menu_usuario():
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
                print('Datos') #datos de los articulos (data.get_articulos())
                thread = []
                continue
            case [1, 2]:
                cod = input('Código del pedido: ')
                print(f'Pedido {cod}') #datos del pedido suministrado (data.get_paquete_by_codigo(cod))
                thread = []
                continue
            case [1, 3]:
                thread.pop()
                thread.pop()
                continue
            case [2]:
                direccion = input('Dirección: ')
                #paq.controlador_crear_paquete(direccion, usuario)
                thread = []
                continue
            case [3]:
                thread = []
                break

        op = input('Selección: ')
        try:
            op = int(op)
            thread.append(op)
        except:
            print('Introduce una selección válida.')
            continue
        
def menu_vendedor():
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
                #data.add_articulo(nom, cant, usuario, desc)
                thread.pop()
                continue
            case [1, 1, 2]:
                while True:
                        try:
                            cod = int(input('Código: '))
                            break
                        except ValueError:
                            print('Ha de ser un número.')
                #data.delete_articulo(cod)
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
                            id = input('DNI: ')
                            break
                        except ValueError:
                            print('Ha de ser un número entero.')
                            continue
                #data.add_articulo(nom, cant, usuario, desc)
                thread.pop()
                continue

            case [1, 2, 2]:
                while True:
                        cod = input('DNI: ')
                        #if cod not in data.repartidores:
                        #    print('Repartidor no encontrado')
                        #else:
                        #    break
                        break
                #data.delete_repartidor(cod)
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
                #print(data.get_artículos)
                thread.pop()
                continue

            case [2, 2]:
                #print(data.get_repartidores)
                thread.pop()
                continue

            case [2, 3]:
                #print(data.get_data(cat))??
                thread.pop()
                continue

            case [2, 4]:
                thread.pop()
                thread.pop()
                continue

            case [3]:
                thread = []
                break

        op = input('Selección: ')
        try:
            op = int(op)
            thread.append(op)
        except:
            print('Introduce una selección válida.')
            continue