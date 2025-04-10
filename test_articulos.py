from articulos_paquetes.articulos import controlador_crear_articulo,controlador_ver_articulo
from articulos_paquetes.paquetes import controlador_crear_paquete, controlador_ver_paquete



p=controlador_crear_articulo(nombre='Prueba',cantidad=2,codigo='7f30',proveedor='CMAX',procedencia='China',descripcion='Pandemonium regnat')

a=controlador_crear_paquete(codigo_paquete='a113',direccion='123 calle romeros',usuario='Josepepe')

controlador_ver_articulo(p)

controlador_ver_paquete(a)

