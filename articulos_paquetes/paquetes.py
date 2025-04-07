from articulos import Articulo
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

    def __init__(self,nombre,codigo_paquete,procedencia,usuario):
        self.nombre=nombre
        self.__codigo_paquete=codigo_paquete
        self.procedencia=procedencia
        self.usuario=usuario
        self.enviado=False
        #se mete al csv aquí
        
    def __str__(self):
        return f'Paquete {self.nombre} ({self.codigo_paquete}) desde {self.procedencia} a {self.usuario} '

    def se_ha_enviado(self):
        self.enviado=True
        # ???
