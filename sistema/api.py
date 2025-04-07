from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from database import Security, DB

class ApiResponse:
    path = 'http://127.0.0.1:5000'
    db = DB()

    def __init__(self):
        self.app = Flask(__name__)  
        self.app.config['JWT_SECRET_KEY'] = 'e8u2rg8e2r7' 
        self.jwt = JWTManager(self.app)
        self.routes()
    
    def routes(self):
        
        @self.app.route('/')
        def index():
            return 'API de la empresa de reparto activada'
        
        @self.app.route('/signup', methods=['POST'])
        def signup():
            data = request.get_json()
            user = data.get('user')
            password = data.get('password')

            if not all([user, password]):
                return jsonify({'message': 'Faltan datos'}), 400
            
            # Añadirlo a la BD (result = llamada a la bd))
            result = ...

            # Usuario creado con exito
            if result == 201:
                return jsonify({'message': 'Usuario creado'}), 201
            # Usuario ya existe
            elif result == 409:
                return jsonify({'message': 'El usuario ya existe'}), 409
            # Error al crear el usuario
            else :
                return jsonify({'message': 'Error al crear el usuario'}), 400
            

        @self.app.route('/login', methods=['GET'])
        def login():
            user = request.args.get('user')
            password = request.args.get('password')
           
            # # Añadirlo a la BD (result = llamada a la bd)) --> crear función que verifique si el usuario existe dentro de la BD, usar funciones de Security para verificar el hash y la contraseña en texto plano
            result = ...

            # Usuario no existe
            if result == 404:
                return jsonify({'message': 'Usuario no existe'}), 404
            
            # Contraseña incorrecta
            elif result == 401:
                return jsonify({'message': 'Contraseña incorrecta'}), 401
            
            token = create_access_token(identity=user)
            return jsonify({'access_token': token}), 200
        
        @self.app.route('/pedidos', methods=['GET'])
        @jwt_required()
        def get_orders():
            user = get_jwt_identity()
            
            # Función de la BD que devuelva los pedidos del usuario
            pedidos = ...
            if not pedidos:
                return jsonify({'message': 'No hay pedidos'}), 404
            
            return jsonify({'message': 'Pedidos encontrados', 'data': pedidos}), 200
        
        @self.app.route('/pedidos/<int:id>', methods=['GET'])
        @jwt_required()
        def get_order_with_id(id):
            user = get_jwt_identity()
            
            # Función de la BD que devuelva el pedido del usuario
            pedido = ...
            if not pedido:
                return jsonify({'message': 'No hay pedidos'}), 404
            
            return jsonify({'message': 'Pedido encontrado', 'data': pedido}), 200
        
        @self.app.route('/pedidos', methods=['POST'])
        @jwt_required()
        def add_order():
            user = get_jwt_identity()
            data = request.get_json()
            
            # Función de la BD que añada el pedido
            result = ...
            if result == 201:
                return jsonify({'message': 'Pedido creado'}), 201
            else:
                return jsonify({'message': 'Error al crear el pedido'}), 400
        
        @self.app.route('/pedidos/<int:id>', methods=['DELETE'])
        @jwt_required()
        def delete_order_with_id(id):
            user = get_jwt_identity()
            
            # Función de la BD que elimine el pedido
            result = ...
            if result == 200:
                return jsonify({'message': 'Pedido eliminado'}), 200
            else:
                return jsonify({'message': 'Error al eliminar el pedido'}), 400
            
        
        

      
