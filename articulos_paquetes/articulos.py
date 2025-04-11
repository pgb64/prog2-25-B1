from database.db import Db

db=Db()

class Articulo:
    '''
    atrubutos
    -------------
    dicc_proced:  diccionario (de clase)

        un diccionario cuyas claves son los origenes de cada artículo y sus valores son listas de los códigos que tengan el mismo origen

    nombre: str
    
        nombre del producto
        
    cantidad :int
    
        cantidad total disponible del producto
        
    codigo: int
    
        los nombres pueden ser iguales, el código no, será un contador de instancias.
        
    proveedor: str
    
        Será el nombre de usuario de la persona que venda, o el cif de la empresa que los ofrezca

    descripción: str

        descripción del artículo
        
    métodos
    --------------
    __init__():
    
        construye un producto

    __str__():

        representa un artticulo de manera comprensible
    
    editar_datos():
    
        cambia los datos de un producto
        
    eliminar_producto():
    
        se elimina el producto indicado. Solo podrá hacerlo el usuario que haya creado el articulo

    dop():

        añade un código al diccionario dicc_proced según su procedencia

    editar_datos():
    
        edita los datos de un artículo a nivel de objetos
        
    eliminar_producto():
    
        elimina un articulo a nivel objeto
        
    funciones
    ----------------------------
    controlador_crear_articulo()
    
        crea un articulo dados todos sus atributos
        
    controlador_ver_articulo()
    
        dado el id de un articulo, devuelve sus datos
        
    '''
    codigo=1
    dicc_proced = {}

    def __init__(self,nombre: str,cantidad: int,proveedor: str,descripcion: str,procedencia: str):
        try:
            if type(self).codigo not in db.get_codigos_articulos():
                
                self.__codigo=type(self).codigo # es necesario que sea único
                
            elif type(self).codigo in db.get_codigos_articulos(): # si no lo es da error
                raise KeyError
        except:
            print('ERROR: Código duplicado')
        else: # si todo sale bien inicializa el objeto
            self.nombre=nombre
            self.cantidad=cantidad
            self.proveedor=proveedor
            self.descripcion=descripcion
            try:
                self.procedencia=procedencia
                type(self).dop(procedencia,self.__codigo) # intenta introducir la procedencia
            except:
                print('Procedencia no válida')
            else:
                #introduce el objeto sin errores a la base de datos
                db.add_articulo(nombre=self.nombre,codigo=self.__codigo,cantidad=self.cantidad,proveedor=self.proveedor,descripcion=self.descripcion)
                print('Articulo creado exitosamente')
                type(self).codigo+=1
    
    @classmethod
    
    def dop(cls,procedencia,cod):
        if not isinstance(procedencia,str): # si la procedencia no es un string da error
            raise ValueError
        else:
            cls.dicc_proced[procedencia]=cod
    
    def __str__(self):
        return f'{self.nombre} ({self.mostrar_codigo()}): {self.cantidad} unidades en total. Distribuido por {self.proveedor} desde {self.procedencia}'

    def mostrar_codigo(self):
        return self.__codigo
    
    def editar_datos(self,nombre:str,cantidad:str,proveedor:str):
        self.nombre=nombre
        self.cantidad=cantidad
        self.proveedor=proveedor
        
    def eliminar_producto(self): # esto solo podrá hacerlo quén haya subido el artículo
        db.delete_articulo(self.mostrar_codigo())
        del self

def controlador_crear_articulo(nombre:str,cantidad:int,proveedor:str,codigo:str,descripcion:str,procedencia:str):
        return Articulo(nombre,cantidad,proveedor,codigo,descripcion,procedencia)
    
def controlador_ver_articulo(articulo: str):
    try:
        print(db.get_articulo_codigo(articulo)) # obtiene la información desde la base de datos
    except:
        print('el id no pertenece al de ningun articulo')
