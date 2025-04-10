from database.db import Db

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
    
contenido: str

    id del artículo que va en un paquete
    
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
-----------------------
controlador_crear_paquete():

    crea un paquete dados sus atributos
    
controlador_ver_paquete():

    musetra los datos de un paquete dado su id
    
'''

class Paquete:

    def __init__(self,codigo_paquete:str,direccion:str,usuario:str,id_contenido:str):
        try:
            if codigo_paquete not in db.get_codigos_paquetes():
                self.__codigo_paquete=codigo_paquete # el coldigo debe ser unico
            else:
                raise KeyError
        except:
            
            print('El código ya existe')
            
        else: # si todo sale bien inicializa el objeto
            
            self.direccion=direccion
            self.usuario=usuario
            self.enviado=False
            self.id_contenido=id_contenido
            print('Paquete creado exitosamente')
            db.add_paquete( self.__codigo_paquete, self.direccion, self.usuario, self.id_contenido) # lo añade a la bd
        
    def __str__(self):
        return f'Paquete ({self.mostrar_codigo()}) con direccion {self.direccion} para {self.usuario} '

    def se_ha_enviado(self): # el paquete ha llegado a su destino?
        self.enviado=True
        
    def mostrar_codigo(self):
        return self.__codigo_paquete
    
def controlador_crear_paquete(codigo_paquete: str,direccion: str,usuario: str ,contenido: str): # construye desde fuera
        return Paquete(codigo_paquete,direccion,usuario,contenido)
    
def controlador_ver_paquete(id_paquete: str): # observa desde fuera
    try:
        print(db.get_paquete_by_codigo(id_paquete))
    except:
        print('Error')
