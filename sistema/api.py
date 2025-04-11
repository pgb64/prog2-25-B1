# Importamos las librerías necesarias
from flask import Flask, jsonify, request
import requests
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from database import Db, Security

class ApiResponse:
    '''
    Clase para manejar la API de la aplicación

    Atributos:
    ----------
    path : str
        URL base de la API
    db : Db
        Instancia de la clase Db para manejar la base de datos
    app : Flask
        Instancia de la aplicación Flask
    jwt : JWTManager
        Instancia del manejador de JWT  

    Métodos:
    -------
    __init__ : None
        Inicializa la aplicación Flask y configura el JWT
    routes : None
        Define las rutas de la API, si no se llama no se define ningún 'endpoint'
    '''
    path = 'http://127.0.0.1:5000'
    db = Db()  # Instanciamos la clase Db correctamente aquí

    def __init__(self):
        '''
        Inicializa la aplicación Flask y configura el JWT

        Este método inicializa la aplicación Flask y establece la clave secreta 
        para la creación de tokens JWT. También se llaman las rutas de la API al 
        iniciar la aplicación.

        Atributos:
        ----------
        self.app : Flask
            Instancia de la aplicación Flask
        self.jwt : JWTManager
            Instancia del manejador de JWT
        '''
        self.app  = Flask(__name__)  
        # Clave secreta de los tokens
        self.app.config['JWT_SECRET_KEY'] = 'e8u2rg8e2r7' 
        self.jwt = JWTManager(self.app)
        # Al iniciar la Api se definen los endpoints
        self.routes()
    
    def routes(self):
        '''
        Método para definir las rutas de la API

        Define los endpoints de la API que la aplicación proporcionará, incluyendo
        la creación de usuarios, inicio de sesión, manejo de pedidos y modificación de datos.

        Rutas:
        -------
        / : GET
            Respuesta básica para comprobar que el servidor está activo
        /signup : POST
            Registrar un nuevo usuario en la base de datos
        /login : GET
            Iniciar sesión y generar un token JWT
        /pedidos : GET
            Obtener todos los pedidos de un usuario autenticado
        /pedidos/<id> : GET
            Obtener un pedido específico por ID para el usuario autenticado
        /pedidos : POST
            Crear un nuevo pedido para el usuario autenticado
        /pedidos/<id> : DELETE
            Eliminar un pedido por ID para el usuario autenticado
        /modificar_usuario : PUT
            Modificar los datos de usuario autenticado
        '''
        
        # Caso base
        @self.app.route('/', methods=['GET'])
        def home():
            '''
            Endpoint de prueba para asegurarse de que el servidor está activo.

            Método:
            -------
            GET

            Respuesta:
            ----------
            200: El servidor está activo
            '''
            return jsonify({'message': 'Servidor de TuPaquete activado'}), 200

        # Endpoint para registrar usuarios
        @self.app.route('/signup', methods=['POST'])
        def signup():
            '''
            Lógica para registrar un nuevo usuario

            Este endpoint recibe los datos del usuario y su contraseña, valida que no
            estén vacíos y que la contraseña cumpla con los requisitos de seguridad.
            Si el usuario es válido, se almacena en la base de datos.

            Método:
            -------
            POST

            Parámetros:
            -----------
            user : str
                Nombre de usuario
            password : str
                Contraseña del usuario
            type : str (opcional)
                Tipo de usuario ('user', 'worker', 'admin')

            Respuesta:
            ----------
            201: Usuario creado exitosamente
            400: Error de validación de entrada
            409: El usuario ya existe
            '''
            data = request.get_json()  # Obtener datos del cuerpo de la solicitud  
            user = data.get('user')
            password = data.get('password')
            user_type = data.get('type', 'user')

            if not user or not password:
                return jsonify({'message': 'El usuario y la contraseña no pueden estar vacíos'}), 400

            password_strength = Security.check_password_strength(password)
            if password_strength == 401: 
                return jsonify({'message': 'La contraseña no cumple con los requisitos de seguridad'}), 400

            valid_types = ['user', 'worker', 'admin']
            if user_type not in valid_types:
                user_type = 'user'  

            result = self.db.add_user(user, password, tipo=user_type)

            if result == 201:
                return jsonify({'message': 'Usuario creado exitosamente'}), 201
            elif result == 409:
                return jsonify({'message': 'El usuario ya existe'}), 409
            else:
                return jsonify({'message': 'Error al crear el usuario'}), 400

        @self.app.route('/login', methods=['GET'])
        def login():
            '''
            Lógica para iniciar sesión

            Este endpoint permite al usuario iniciar sesión proporcionando su nombre 
            de usuario y contraseña. Si las credenciales son correctas, se genera un 
            token JWT para el usuario autenticado.

            Método:
            -------
            GET

            Parámetros:
            -----------
            user : str
                Nombre de usuario
            password : str
                Contraseña del usuario

            Respuesta:
            ----------
            200: Token de acceso generado
            400: Usuario no encontrado
            401: Contraseña inválida
            '''
            user = request.args.get('user')
            password = request.args.get('password')

            try:
                result = self.db.login(user, password)
                if result == 400:
                    return jsonify({'message': f'Usuario "{user}" no encontrado'}), 400

                password_strength = Security.check_password_strength(password)
                if password_strength == 401:
                    return jsonify({'message': 'Contraseña inválida'}), 401

                token = create_access_token(identity=user)
                return jsonify({'access_token': token}), 200
            except Exception as e:
                return jsonify({'message': f"Error en el servidor: {str(e)}"}), 500

        @self.app.route('/pedidos', methods=['GET'])
        @jwt_required()
        def get_orders():
            '''
            Obtener todos los pedidos del usuario autenticado.

            Método:
            -------
            GET

            Respuesta:
            ----------
            200: Pedidos encontrados
            404: No hay pedidos
            '''
            user = get_jwt_identity()
            
            pedidos = self.db.get_orders_by_user(user)
            if not pedidos:
                return jsonify({'message': 'No hay pedidos'}), 404
            
            return jsonify({'message': 'Pedidos encontrados', 'data': pedidos}), 200
        
        @self.app.route('/pedidos/<int:id>', methods=['GET'])
        @jwt_required()
        def get_order_with_id(id):
            '''
            Obtener un pedido específico por ID para el usuario autenticado.

            Método:
            -------
            GET

            Parámetros:
            -----------
            id : int
                ID del pedido

            Respuesta:
            ----------
            200: Pedido encontrado
            404: No se encontró el pedido
            '''
            user = get_jwt_identity()
            
            pedido = self.db.get_order_by_id(user, id)
            if not pedido:
                return jsonify({'message': 'No hay pedidos'}), 404
            
            return jsonify({'message': 'Pedido encontrado', 'data': pedido}), 200
        
        @self.app.route('/pedidos', methods=['POST'])
        @jwt_required()
        def add_order():
            '''
            Crear un nuevo pedido para el usuario autenticado.

            Método:
            -------
            POST

            Respuesta:
            ----------
            201: Pedido creado
            400: Error al crear el pedido
            '''
            user = get_jwt_identity()
            data = request.get_json()

            result = self.db.add_order(user, data)
            if result == 201:
                return jsonify({'message': 'Pedido creado'}), 201
            else:
                return jsonify({'message': 'Error al crear el pedido'}), 400
        
        @self.app.route('/pedidos/<int:id>', methods=['DELETE'])
        @jwt_required()
        def delete_order_with_id(id):
            '''
            Eliminar un pedido por ID para el usuario autenticado.

            Método:
            -------
            DELETE

            Parámetros:
            -----------
            id : int
                ID del pedido a eliminar

            Respuesta:
            ----------
            200: Pedido eliminado
            400: Error al eliminar el pedido
            '''
            user = get_jwt_identity()

            result = self.db.delete_order(user, id)
            if result == 200:
                return jsonify({'message': 'Pedido eliminado'}), 200
            else:
                return jsonify({'message': 'Error al eliminar el pedido'}), 400

        @self.app.route('/modificar_usuario', methods=['PUT'])
        @jwt_required()
        def modify_user_info():
            '''
            Modificar los datos del usuario autenticado.

            Método:
            -------
            PUT

            Respuesta:
            ----------
            200: Datos modificados exitosamente
            404: Usuario no encontrado
            400: Error al modificar los datos
            '''
            user = get_jwt_identity()
            data = request.get_json()

            resultado = self.db.update_user_info(user, data)

            if resultado == 200:
                return jsonify({'message': 'Datos modificados exitosamente'}), 200
            elif resultado == 404:
                return jsonify({'message': 'Usuario no encontrado'}), 404
            else:
                return jsonify({'message': 'Error al modificar los datos'}), 400
