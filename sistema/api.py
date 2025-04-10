from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from database import Db

class ApiResponse:
    path = 'http://127.0.0.1:5000'
    db = Db()  # Instanciamos la clase Db correctamente aquí

    def __init__(self):
        self.app = Flask(__name__)  
        self.app.config['JWT_SECRET_KEY'] = 'e8u2rg8e2r7' 
        self.jwt = JWTManager(self.app)
        self.routes()
    
    def routes(self):
        @self.app.route('/signup', methods=['POST'])
        def signup():
            data = request.get_json()
            user = data.get('user')
            password = data.get('password')
            tipo = data.get('tipo', 'usuario')  # Establecer 'usuario' como tipo por defecto

            if not all([user, password]):
                return jsonify({'message': 'Faltan datos'}), 400

            # Verificar si el usuario ya existe en la base de datos
            result = self.db.add_user(user, password, tipo)

            # Usuario creado con éxito
            if result == 201:
                return jsonify({'message': 'Usuario creado'}), 201
            # Usuario ya existe
            elif result == 409:
                return jsonify({'message': 'El usuario ya existe'}), 409
            # Error al crear el usuario
            else:
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
                result_password = self.db.check_password_strength(password)
                if result_password == 401:
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
