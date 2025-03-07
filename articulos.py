class Articulo: #por ahora sin herenchia
    '''
    atrubutos
    -------------
    nombre: str
    
        nombre del producto
        
    cantidad :int
    
        cantidad total disponible del producto
        
    codigo: str
    
        los nombres pueden ser iguales, el gódigo no
        
    proveedor: str
    
        Será el nombre de usuario de la persona que venda, o el cif de la empresa que los ofrezca

    descripción: diccionario

        En ese diccionario habrán cosas como el peso o sus dimensiones
        
    métodos
    --------------
    __init__():
    
        construye un producto
    
    editar datos:
    
        cambia los datos de un producto. Por defecto no cambiará nada
        
    eliminar producto
    
        se elimina el producto indicado. Se hará automatico cuando la cantidad del producto llegue a 0
    
    '''
    def __init__(self,nombre,cantidad,codigo,proveedor,descripcion):
        self.nombre=nombre
        self.cantidad=cantidad
        self.__codigo=codigo # es necesario que sea único
        self.proveedor=proveedor # la base de datos, por favor
        self.descripcion=descripcion
        # self.procedencia=procedencia, cuando tengamos la base de datos, se podrá obtener la procedencia de un paquete de alguna otra forma


    def mostrar_codigo(self):
        return self.__codigo

    
    def editar_datos(self,nombre=self.nombre,cantidad=self.cantidad,proveedor=self.proveedor):
        self.nombre=nombre
        self.cantidad=cantidad
        self.proveedor=proveedor
        # no se eliminar objetos, aquí se comprueba.

    def eliminar_producto(self):

    def pedir_paquete(self):
        self.cantidad-=1 # quita un paquete del cantidad
        if self.cantidad<1:
            self.eliminar_producto()


class Paquete(Articulo):

    def __init__(self,):