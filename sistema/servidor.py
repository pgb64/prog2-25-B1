import socket
from .api import ApiResponse 

class Server(ApiResponse):

    def __init__(self):
        super().__init__()  
        self.path = self.path 
        self.routes() 

    @classmethod
    def get_state(cls, path):
        url = path.split('://')[1]
        host, port = url.split(':')
        try:
            s = socket.socket()
            s.connect((host, int(port)))
            s.close()
            return True
        except:
            return False

    def launch(self):
        if not self.get_state(self.path):
            print("Activando servidor...")
            self.app.run(debug=True, use_reloader=False)
        else:
            print("El servidor ya está activo.")
