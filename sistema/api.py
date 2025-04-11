from flask import Flask, jsonify, request
import requests
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from database import Db, Security

class ApiResponse:
    path = 'http://127.0.0.1:5000'
    db = Db()  # Instanciamos la clase Db correctamente aquí

    def __init__(self):
        self.app = Flask(__name__)  
        self.app.config['JWT_SECRET_KEY'] = 'e8u2rg8e2r7' 
        self.jwt = JWTManager(self.app)
        self.routes()
    
    def routes(self):
        @self.app.route('/', methods=['GET'])
        def home():
            return jsonify({'message': 'Servidor de TuPaquete activado'}), 200

        @self.app.route('/signup', methods=['POST'])
        def signup():
            '''
            Lógica para registrar un nuevo usuario
            '''
            print("Recibida solicitud en /signup")  # Depuración inicial
            data = request.get_json()  # Obtener datos del cuerpo de la solicitud
            print(f"Datos recibidos: {data}")  # Verificar datos recibidos

            user = data.get('user')
            password = data.get('password')
            user_type = data.get('type', 'user')  # Si no se proporciona, usar 'user' por defecto

            # Validar entrada del usuario
            if not user or not password:
                print("Error: Usuario o contraseña vacíos")  # Depuración
                return jsonify({'message': 'El usuario y la contraseña no pueden estar vacíos'}), 400

            # Validar fortaleza de la contraseña
            password_strength = Security.check_password_strength(password)
            print(f"Resultado de validación de contraseña: {password_strength}")  # Depuración
            if password_strength == 401:
                print("Error: Contraseña no cumple con los requisitos de seguridad")  # Depuración
                return jsonify({'message': 'La contraseña no cumple con los requisitos de seguridad'}), 400

            # Validar tipo de usuario
            valid_types = ['user', 'worker', 'admin']
            if user_type not in valid_types:
                print(f"Error: Tipo de usuario inválido: {user_type}")  # Depuración
                user_type = 'user'  # Valor por defecto

            # Intentar registrar al usuario en la base de datos
            result = self.db.add_user(user, password, tipo=user_type)
            print(f"Resultado de add_user: {result}")  # Depuración
            if result == 201:
                print("Usuario creado exitosamente")  # Depuración
                return jsonify({'message': 'Usuario creado exitosamente'}), 201
            elif result == 409:
                print("Error: El usuario ya existe")  # Depuración
                return jsonify({'message': 'El usuario ya existe'}), 409
            else:
                print("Error: Fallo al crear el usuario")  # Depuración
                return jsonify({'message': 'Error al crear el usuario'}), 400

        @self.app.route('/login', methods=['GET'])
        def login():
            user = request.args.get('user')
            password = request.args.get('password')

            try:
                # Verificar si el usuario existe
                result = self.db.login(user, password)
                if result == 400:
                    return jsonify({'message': f'Usuario "{user}" no encontrado'}), 400

                # Verificar la fortaleza de la contraseña
                password_strength = Security.check_password_strength(password)
                if password_strength == 401:
                    return jsonify({'message': 'Contraseña inválida'}), 401

                # Si todo está correcto, generar el token
                token = create_access_token(identity=user)
                return jsonify({'access_token': token}), 200
            except Exception as e:
                return jsonify({'message': f"Error en el servidor: {str(e)}"}), 500

        @self.app.route('/pedidos', methods=['GET'])
        @jwt_required()
        def get_orders():
            user = get_jwt_identity()
            
            # Función de la BD que devuelva los pedidos del usuario
            pedidos = self.db.get_orders_by_user(user)  # Usamos self.db aquí
            if not pedidos:
                return jsonify({'message': 'No hay pedidos'}), 404
            
            return jsonify({'message': 'Pedidos encontrados', 'data': pedidos}), 200
        
        @self.app.route('/pedidos/<int:id>', methods=['GET'])
        @jwt_required()
        def get_order_with_id(id):
            user = get_jwt_identity()
            
            # Función de la BD que devuelva el pedido del usuario
            pedido = self.db.get_order_by_id(user, id)  # Usamos self.db aquí
            if not pedido:
                return jsonify({'message': 'No hay pedidos'}), 404
            
            return jsonify({'message': 'Pedido encontrado', 'data': pedido}), 200
        
        @self.app.route('/pedidos', methods=['POST'])
        @jwt_required()
        def add_order():
            user = get_jwt_identity()
            data = request.get_json()

            # Función de la BD que añada el pedido
            result = self.db.add_order(user, data)  # Usamos self.db aquí
            if result == 201:
                return jsonify({'message': 'Pedido creado'}), 201
            else:
                return jsonify({'message': 'Error al crear el pedido'}), 400
        
        @self.app.route('/pedidos/<int:id>', methods=['DELETE'])
        @jwt_required()
        def delete_order_with_id(id):
            user = get_jwt_identity()

            # Función de la BD que elimine el pedido
            result = self.db.delete_order(user, id)  # Usamos self.db aquí
            if result == 200:
                return jsonify({'message': 'Pedido eliminado'}), 200
            else:
                return jsonify({'message': 'Error al eliminar el pedido'}), 400

        @self.app.route('/modificar_usuario', methods=['PUT'])
        @jwt_required()
        def modify_user_info():
            user = get_jwt_identity()
            data = request.get_json()

            # Aquí actualizamos los datos del usuario en la base de datos
            resultado = self.db.update_user_info(user, data)  # Usamos self.db aquí

            if resultado == 200:
                return jsonify({'message': 'Datos modificados exitosamente'}), 200
            elif resultado == 404:
                return jsonify({'message': 'Usuario no encontrado'}), 404
            else:
                return jsonify({'message': 'Error al modificar los datos'}), 400
