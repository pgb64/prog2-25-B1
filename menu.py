import database.db as db
import articulos_paquetes.paquetes as paq
import informes as inf

def menu(usuario: str, permisos = 'usuario'):
    data = db.Db()
    if permisos == 'usuario':
        menu_usuario(data, usuario)
    if permisos == 'admin' or permisos == 'administrador':
        menu_vendedor(data)


def menu_usuario(data, usuario):
    while True:
        op = input(f"""Selecciona una opción:
1. Hacer una consulta
2. Hacer un pedido
3. Salir
          """)
        
#1: Hacer una consulta
        if '1' in op:
            op = input(f"""Selecciona una opción:
1. Consultar el catálogo
2. Consultar un pedido
3. Atrás
          """)
            
#11: Consultar el catálogo
            if '1' in op:
                print(data.get_articulos())

#12: Consultar un pedido
            elif '2' in op:
                cod = input('Código del pedido: ')
                print(data.get_paquete_by_codigo(cod))

#13: Atrás
            elif '3' in op:
                op = 0
                continue

#2: Hacer un pedido
        elif '2' in op:
            direccion = input('Dirección: ')
            paq.controlador_crear_paquete(direccion, usuario)

#3: Salir
        elif '3' in op:
            op = 0
            break
    
def menu_vendedor(data, usuario):
    while True:
        op = input(f"""Selecciona una opción:
1. Realizar gestiones
2. Ver estadísticas
3. Salir
          """)
        
#1: Realizar gestiones
        if '1' in op:
            op = input(f"""Gestionar...
1. Artículos
2. Repartidores
3. Atrás
          """)
            
#11: Gestionar artículos
            if '1' in op:
                op = input(f"""Gestionar artículos:
1. Añadir un artículo
2. Eliminar un artículo
3. Atrás
          """)

#111: Añadir un artículo
                if '1' in op:
                    while True:
                        try:
                            nom = int(input('Nombre del artículo: '))
                            cant = int(input('Cantidad del artículo: '))
                            desc = int(input('Descripción del artículo: '))
                            break
                        except ValueError:
                            print('Ha de ser un número.')
                    data.add_articulo(nom, cant, usuario, desc)

#112: Eliminar un artículo
                elif '2' in op:
                    while True:
                        try:
                            cod = int(input('Código del artículo: '))
                            break
                        except ValueError:
                            print('Ha de ser un número.')
                    data.delete_articulo(cod)

#113: Atrás
                elif '3' in op:
                    op = 0
                    continue

#12: Gestionar repartidores
            elif '2' in op:
                op = input(f"""Gestionar repartidores:
1. Añadir un repartidor
2. Eliminar un repartidor
3. Atrás
          """)

#13: Atrás
            elif '3' in op:
                op = 0
                continue

#2: Ver estadísticas
        elif '2' in op:
            op = input(f"""Ver estadísticas:
1. Ver artículos
2. Ver repartidores
3. Estadísticas personalizadas
4. Atrás
          """)
            
#21: Ver artículos      
            if '1' in op:
                data.get_articulos()

#22: Ver repartidores
            if '2' in op:
                data.get_repartidores()

#23: Estadísticas personalizadas
            if '3' in op:
                # por implementar
                pass

#24: Atrás
            if '4' in op:
                op = 0
                continue

#3: Salir
        elif '3' in op:
            op = 0
            break