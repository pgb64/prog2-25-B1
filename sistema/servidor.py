# Importamos los módulso necesarios
import socket
from .api import ApiResponse 

class Server(ApiResponse):
    '''
    Clase para gestionar el servidor de la API

    Atributos:
    ----------
    path : str
        URL base del servidor (heredado de ApiResponse)
    
    Métodos:
    -------
    __init__ : None
        Inicializa la clase Server, heredando atributos de ApiResponse
    get_state : bool
        Verifica si el servidor está activo
    launch : None
        Lanza el servidor si no está activo, o muestra un mensaje si ya lo está
    '''

    def __init__(self):
        '''
        Inicializa la clase Server y establece la URL base del servidor heredado de ApiResponse.

        Este método invoca el constructor de la clase base ApiResponse y configura la URL base.
        '''
        super().__init__()  
        self.path = self.path  # La URL base es heredada de ApiResponse
    
    @classmethod
    def get_state(cls, path):
        '''
        Verifica si el servidor especificado en la URL está activo.

        Parámetros:
        -----------
        path : str
            URL del servidor, que debe incluir el protocolo
        
        Retorna:
        --------
        bool
            True si el servidor está activo, False si no lo está
        '''
        url = path.split('://')[1]
        host, port = url.split(':')
        try:
            s = socket.socket()
            s.connect((host, int(port)))  # Intenta conectarse al servidor
            s.close()
            return True
        except:
            return False  # Si ocurre algún error, el servidor no está activo
    
    def launch(self):
        '''
        Lanza el servidor si no está activo.

        Si el servidor ya está activo, muestra un mensaje indicando que no es necesario reiniciarlo.
        Si no está activo, inicia el servidor en el puerto y la dirección especificados en self.path.
        '''
        if not self.get_state(self.path):
            print("Activando servidor...")  # Si el servidor no está activo, lo activamos
            self.app.run(debug=True, use_reloader=False)
        else:
            print("El servidor ya está activo.")  # Si el servidor está activo, informamos al usuario
