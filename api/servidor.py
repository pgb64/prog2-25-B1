from flask import Flask, request
import socket
from api.gestion import ApiResponse
from database import Security, DB


class Server:
    path = 'http://127.0.0.1:5000'

    def __init__(self):
        self.app = Flask(__name__)
        self.app.config["JWT_SECRET_KEY"] = Security.get_key()
        self.db = DB()
        self.routes()

    def launch(self):
        if not self.get_state(self.path):
            print("Activando servidor...")
            self.app.run(debug=True, use_reloader=False)
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
    

    def routes(self):
        @self.app.route('/')
        def base():
            return ApiResponse.success('Servidor activo.', None), ApiResponse.OK


        @self.app.route('/get_all_info_public', methods=['GET'])
        def get_all_info_public():
            data = self.db.get_all_users_info()
            return ApiResponse.success('Datos obtenidos.', data), ApiResponse.OK

        @self.app.route('/get_all_data_public', methods=['GET'])
        def get_all_data_public():
            data = self.db.get_all_users_data()
            return ApiResponse.success("Datos obtenidos.", data), ApiResponse.OK

        # Decorador
        @self.app.route('/get_all_info_private', methods=['GET'])
        def get_all_info_private():
            data = self.db.get_all_users_info()
            return ApiResponse.success("Datos privados obtenidos.", data), ApiResponse.OK

        # Decorador
        @self.app.route('/get_all_data_private', methods=['GET'])
        def get_all_data_private():
            data = self.db.get_all_users_data()
            return ApiResponse.success("Datos privados obtenidos.", data), ApiResponse.OK

        # Intercción con usuarios

        @self.app.route('/login', methods=['POST'])
        # Aquí irá el decorador del token
        def login(username, password):
            if username not in DB.get_all_usernames():
                return ApiResponse.error('El usuario no está registrado', ApiResponse.NOT_FOUND)
            hash = DB.get
            




