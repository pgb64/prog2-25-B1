class Articulo: #por ahora sin herenchia
    '''
    atrubutos
    -------------
    dicc_proced:  diccionario (de clase)

        un diccionario cuyas claves son los origenes de cada artículo y sus valores son listas de los códigos que tengan el mismo origen

    nombre: str
    
        nombre del producto
        
    cantidad :int
    
        cantidad total disponible del producto
        
    codigo: str
    
        los nombres pueden ser iguales, el gódigo no
        
    proveedor: str
    
        Será el nombre de usuario de la persona que venda, o el cif de la empresa que los ofrezca

    descripción: str

        descripción del artículo
        
    métodos
    --------------
    __init__():
    
        construye un producto
    
    editar_datos():
    
        cambia los datos de un producto
        
    eliminar_producto():
    
        se elimina el producto indicado. Solo podrá hacerlo el usuario que haya creado el articulo

    pedir_paquete():

        transofma un articulo en paquete. Recibe como parámetro el nombre de usuario del destinatario.

    dop():

        añade un código al diccionario dicc_proced según su procedencia

    
    '''

    dicc_proced = {}

    def __init__(self,nombre,cantidad,proveedor,codigo,descripcion,procedencia):
        self.nombre=nombre
        self.cantidad=cantidad
        '''
        try:
            if codigo not in basedatos.claves()???:
                self.__codigo=codigo # es necesario que sea único
            else:
                raise KeyError
        except:
            print('ERROR: Código duplicado')
            '''
        self.proveedor=proveedor # la base de datos, por favor
        self.descripcion=descripcion
        try:
            self.procedencia=procedencia # cuando tengamos la base de datos, se podrá obtener la procedencia de un paquete de alguna otra forma
            type(self).dop(procedencia,self.__codigo)
        except:
            print('Procedencia no válida')
        # csv!!!!!!

    @classmethod
    def dop(cls,procedencia,cod):
        if not isinstance(procedencia,str):
            raise ValueError
        else:
            cls.dicc_proced[procedencia].append(cod)
    
    def __str__(self):
        return f'{self.nombre} ({self.mostrar_codigo()}): {self.cantidad} unidades en total. Distribuido por {self.proveedor} desde {self.procedencia}'

    def mostrar_codigo(self):
        return self.__codigo
    
    def editar_datos(self,nombre,cantidad,proveedor):
        self.nombre=nombre
        self.cantidad=cantidad
        self.proveedor=proveedor
        
    def eliminar_producto(self): # esto solo podrá hacerlo quén haya subido el artículo
        del self

    def pedir_paquete(self,usuario):
        from paquetes import Paquete
        if self.cantidad>=1:
            self.cantidad-=1
            p=Paquete(self.nombre,self.mostrar_codigo(),self.procedencia,usuario)
            print('artículo pedido exitosamente')
            
            return p

        else:
            print('No quedan artículos de este tipo')
            
