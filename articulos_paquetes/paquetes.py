from database.db import Db
import articulos_paquetes.articulos as ar
db=Db()

'''
atributos
-------------------
codigo_paquete: str

    se generará aleatorio y se asegurará que no está ya en el csv
    
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

mostrar_codigo():

    este método muestra el atributo privado código

funciones 
    
    
    
'''

class Paquete:

    def __init__(self,codigo_paquete:str,direccion:str,usuario:str,id_contenido:str):
        try:
            if codigo_paquete not in db.get_codigos_paquetes():
                self.__codigo_paquete=codigo_paquete
            else:
                raise KeyError
        except:
            
            print('El código ya existe')
            
        else:
            
            self.direccion=direccion
            self.usuario=usuario
            self.enviado=False
            self.id_contenido=id_contenido
            print('Paquete creado exitosamente')
            db.add_paquete( self.__codigo_paquete, self.direccion, self.usuario, self.id_contenido)
    
        
    def __str__(self):
        return f'Paquete ({self.mostrar_codigo()}) con direccion {self.direccion} para {self.usuario} '

    def se_ha_enviado(self):
        self.enviado=True
        db.Db.update_estado_envio(self.mostrar_codigo(),self.enviado)
        
    def mostrar_codigo(self):
        return self.__codigo_paquete

    def controlador_ver_paquete(self,id_paquete: str):
        p=db.get_paquete_by_codigo(id_paquete)
        print(p)
        
def controlador_agregar_articulo(paquete: Paquete ,id_articulo: str):
    try:
        if id_articulo in codigos_articulos:
            a=db.Db.get_articulo_codigo(id_articulo)
            paquete.contenido=id_articulo
        else:
            raise ValueError
    except:
        print('El id del articulo no existe')
    
def controlador_crear_paquete(codigo_paquete: str,direccion: str,usuario: str ,contenido: str):
        return Paquete(codigo_paquete,direccion,usuario,contenido)
    
def controlador_ver_paquete(id_paquete: str):
    try:
        print(db.get_paquete_by_codigo(id_paquete))
    except:
        print('Error')
