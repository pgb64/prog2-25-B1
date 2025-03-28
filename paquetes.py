from articulos import Articulo
'''
atributos
-------------------
*kwargs:

    debe tener los mismos atributos que artículo, pero no me importan en el código (por ahora)
    
enviado:

    Booleano que define si un paquete ha sido enviado o no
    
'''
class Paquete(Articulo):

    def __init__(self,*kwargs):
        super().__init()
        self.enviado=False

    def se_ha_enviado(self):
        self.enviado=True
