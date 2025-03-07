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
        
    
    '''
    def __init__(self,nombre,cantidad,codigo,proveedor):
        self.nombre=nombre
        self.cantidad=cantidad
        self.codigo=codigo
        self.proveedor=proveedor
        
        

