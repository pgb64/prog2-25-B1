import database.db as db
import articulos_paquetes.articulos as ar
'''
atributos
-------------------
nombre: str

    el mismo nombre que el artículo
    
codigo_paquete: str

    se generará aleatorio y se asegurará que no está ya en el csv
    
procedencia: str

    la misma que el paquete
    
usuario: str

    Nombre de usuario del login actual
    
enviado: bool

    Booleano que define si un paquete ha sido enviado o no
    
    
métodos
--------------------
__init__():

    crea un paquete
    
__str__():
    
    muestra información comprensible sobre el paquete
    
se_ha_enviado():

    este método pone a True el atributo enviado cuando el usuario reciba el paquete.
    
'''
class Paquete:

    def __init__(self,codigo_paquete,direccion,usuario):
        try:
            if codigo_paquete not in [1,2,3]: #db.Db.get_codigos_paquetes():
                self.__codigo_paquete=codigo_paquete
            else:
                raise KeyError
        except:
            print('El código ya existe')
        else:
            self.direccion=direccion
            self.usuario=usuario
            self.enviado=False
            print('Paquete creado exitosamente')
            self.contenido=''
    
        
    def __str__(self):
        return f'Paquete ({self.mostrar_codigo()}) con direccion {self.direccion} para {self.usuario} '

    def se_ha_enviado(self):
        self.enviado=True
        db.Db.update_estado_envio(self.mostrar_codigo(),self.enviado)
        
    def mostrar_codigo(self):
        return self.__codigo_paquete

    def controlador_ver_paquete(self,id):
        p=db.get_paquete_by_codigo(id)
        print(p)
        
def controlador_agregar_articulo(paquete,id_articulo):
    pass
    #IGNACIO RESPONDE POR FAVOR
    
def controlador_crear_paquete(codigo_paquete,direccion,usuario):
        return Paquete(codigo_paquete,direccion,usuario)
    
def controlador_ver_paquete(paquete):
    try:
        if not isinstance(paquete,Paquete):
            raise TypeError
        else:
            print(paquete)
    except:
        print('lo que se desea ver no es un Paquete')