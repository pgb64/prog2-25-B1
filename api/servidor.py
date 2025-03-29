from flask import Flask, request
import socket, hashlib, json
from excepcion import Except

class Server:
    path = 'http://127.0.0.1:5000'

    def __init__(self):
        self.app = Flask(__name__)

        @self.app.route('/')
        def base():
            return '¡SERVIDOR ACTIVADO!'

        if not Server.get_state(self.path):
            print("Activando servidor...")
            self.app.run(debug = True, use_reloader = False)
        else:
            print("El servidor ya está activo.")

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
        
    # Todas las funciones

    def routes(self):

        @self.app.route('/get_users', methods = ['POST'])
        def get_users():
            pass


        @self.app.route('/signup', methods = ['GET'])
        def signup():
            data = get_users()
            if not data:
                return Except.data_not_found()
            user = data.get('user')
            
            # Si el usuario ya existe
            if user in data.keys(): # --> Implementar db
                return Except.invalid_user('El usuario ya existe')


            password = data.get('password')
            
            # Si la contraseña tiene un tamaño inválido
            if not (8 <= len(password) <= 20):
                return Except.invalid_password('Tamaño de contraseña inválido')

            
            # Si la contraseña contiene el usuario
            if user in password:
                return Except.invalid_password('La contraseña no puede tener el nombre de usuario')
            
            # Si la contraseña no tiene letras mayúsculas
            if not any(char.isupper() for char in password):
                return Except.invalid_password('La contraseña debe tener al menos una letra mayúscula')
            
            # Si la contraseña no tiene letras minúsculas
            if not any(char.islower() for char in password):
                return Except.invalid_password('La contraseña debe tener alguna letra minúscula')
            
            # Si la contraseña no tiene números
            if not any(char.isdigit() for char in password):
                return Except.invalid_password('La contraseña debe tener algún número')
            
            # Si la contraseña no tiene caracteres especiales
            special = "!@#$%^&*()-_=+[]{}|;:',.<>?/"
            if not any(char in special for char in password):
                return Except.invalid_password('La contraseña debe tener algún carácter especial')
            


            return 'Usuario registrado', 200




if __name__ == '__main__':
    server = Server()
