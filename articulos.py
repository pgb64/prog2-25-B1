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
        
    métodos
    --------------
    __init__():
    
        construye un producto
    
    editar datos:
    
        cambia los datos de un producto. Por defecto no cambiará nada
        
    eliminar producto
    
        se elimina el producto indicado. Se hará automatico cuando la cantidad del producto llegue a 0
    
    '''
    def __init__(self,nombre,cantidad,codigo,proveedor):
        self.nombre=nombre
        self.cantidad=cantidad
        self.codigo=codigo
        self.proveedor=proveedor
    
    def editar_datos(self,nombre=self.nombre,cantidad=self.cantidad,proveedor=self.proveedor):
        self.nombre=nombre
        self.cantidad=cantidad
        self.proveedor=proveedor
        # no se eliminar objetos, aquí se comprueba
    
    def eliminar_producto(self): # no se como se hace esto

        
    
        

