from _sqlite3 import IntegrityError, Error
from flask import Flask, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from security import Security
import database

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'prog2-25-B1'
jwt = JWTManager(app)

"""
En casi toda la API, donde pone parámetros realmente es un json, haciendo un request de la siguiente forma:
requests.<method>(f'{url}/<directory>', json=<data>)
Reemplazando:
<method> por get, post, update, delete o fetch
<directory> por la ruta a la que se quiere acceder
<data> por el json que requieren los parámetros
"""

@app.route('/')
def home():
    return 'Home', 200

def execute_query_error_handler(funct):
    try:
        funct()
    except IntegrityError as e:
        print(f"Error de integridad: {e}")
        return None, 409
    except Error as e:
        return {e}, 400

class Usuario:
    @app.route('/signup', methods=['POST'])
    def signup():
        """
        Da de alta a un usuario

        Parámetros:
        -----------
        email : string
            Email del usuario. Si contiene @vendedor, se le dará de alta al usuario en modo vendedor en vez de usuario
        password : tuple
            Contraseña para la cuenta a crear

        Returns:
        --------
        str
            Si ocurre algún inconveniente a la hora de crear una cuenta
        dict
            Si se crea la cuenta correctamente, devuelve un dict con el token de la cuenta
        """
        try:
            email = request.json.get('email', None)
            password = request.json.get('password', None)
            admin = True if '@vendedor' in email else False

            if not email:
                return 'Missing email', 400
            if not password:
                return 'Missing password', 400

            if not Security.check_password_strength(password):
                return """The password isn't strong enough, it should, at least:
                - Be 8 characters long
                - Include an uppercase character
                - Include a lowercase character
                - Include a number
                - Include a special character""", 400

            hashed = Security.hash_password(password)
            try:
                db = database.UserDB()
                db.add_user(email, hashed, admin)
            except database.db.AlreadyExistsError:
                db.close()
                return 'Este usuario ya existe', 409
            finally:
                db.close()

            token = create_access_token(identity=email)
            return {'token': token}, 201

        except TypeError as e:
            return f'{e}', 400

    @app.route('/login', methods=['POST'])
    def login():
        """
        Inicia sesión a un usuario

        Parámetros:
        -----------
        email : string
            Email del usuario
        password : tuple
            Contraseña del usuario

        Returns:
        --------
        str
            Si ocurre algún inconveniente a la hora de crear una cuenta
        dict
            Si se entra en la cuenta correctamente, devuelve un dict con el token de la cuenta
        """
        try:
            email = request.json.get('email', None)
            password = request.json.get('password', None)
            if not email:
                return 'Missing email', 400
            if not password:
                return 'Missing password', 400

            db = database.UserDB()
            user = db.get_user(username=email)
            if not user:
                db.close()
                raise database.db.DataNotFoundError('El usuario no existe')

            if Security.verify_password(password, user['password']):
                db.close()
                return {'token': create_access_token(identity=email)}, 200
            else:
                db.close()
                raise database.db.DataDoesntMatchError('Contraseña incorrecta')

        except Exception as e:
            return f'{e}', 400

    @app.route('/is_admin', methods=['GET'])
    def is_admin():
        """
        Comprueba si un usuario es vendedor

        Parámetros:
        -----------
        email : string
            Email del usuario

        Returns:
        --------
        string
            Devuelve el valor booleano en forma de string
        """
        email = request.json.get('email', None)
        db = database.UserDB()
        is_admin = db.is_admin(email)
        db.close()
        return f'{is_admin}', 200

class Articulo:
    @app.route('/articulos', methods=['POST'])
    def add_art():
        """
        Añade un artículo a la base de datos

        Parámetros:
        -----------
        data : dict
            Diccionario que contiene toda la información pertinente del artículo    
        
        Returns:
        --------
        int
            Devuelve 201 si el artículo ha sido creado correctamente
            Devuelve 500 si ha habido un error en la creación
        """
        try:
            data = request.get_json()
            db = database.ArticuloDB()
            db.insert("articulos", data)
            db.close()
            return 201
        except:
            return 500

    @app.route('/articulos/<cod>', methods=['GET'])
    def get_art(cod):
        """
        Busca la información de un artículo por su código

        Parámetros:
        -----------
        cod : string
            Código del artículo a buscar

        Returns:
        --------
        dict
            Un diccionario con la información del artículo
        """
        db = database.ArticuloDB()
        data = db.get("articulos")
        db.close()
        return data, 200

    @app.route('/articulos', methods=['DELETE'])
    def delete_art():
        """
        Borra un artículo del catálogo

        Parámetros:
        -----------
        cod : string
            Código del artículo

        Returns:
        --------
        int
            Devuelve 204 si el artículo ha sido borrado correctamente
        """
        cod = request.json.get('cod')
        db = database.ArticuloDB()
        db.delete("articulos", {'codigo': cod})
        db.close()
        return 204

class Paquete:
    @app.route('/paquetes/<cod>', methods=['GET'])
    def get_by_cod(cod):
        """
        Busca la información del paquete

        Parámetros:
        -----------
        cod : string
            Código del paquete

        Returns:
        --------
        dict
            Devuelve la información del paquete (si ha sido encontrada)
        str
            Devuelve un mensaje de error si no existe el paquete
        """
        db = database.PaqueteDB()
        info = db.get_paquete_by_codigo(cod)
        db.close()
        if info == [] or info == {}:
            return 'Código de paquete no encontrado', 404
        return info, 200

    @app.route('/pedidos', methods=['POST'])
    def add_paq():
        """
        WIP
        Crea un paquete en base a la información suministrada
        """
        return 'Lo sentimos, aún estamos trabajando en ello', 501

class Repartidor:
    @app.route('/repartidores', methods=['POST'])
    def add_rep():
        """
        Inserta un repartidor en la base de datos

        Parámetros:
        -----------
        data : dict
            Información pertinente del repartidor

        Returns:
        --------
        int
            Devuelve 201 si la operación ha sido exitosa
        """
        data = request.get_json()
        db = database.RepartidorDB()
        db.insert("repartidores", data)
        db.close()
        return 201

    @app.route('/repartidores', methods=['GET'])
    def get_rep():
        """
        Busca la información de los repartidores

        Returns:
        --------
        dict
            Devuelve la información sobre los repartidores
        """
        db = database.RepartidorDB()
        data = db.get("repartidores")
        db.close()
        return data, 200

    @app.route('/repartidores', methods=['DELETE'])
    def delete_rep():
        """
        Borra a un repartidor de la base de datos

        Parámetros:
        -----------
        id : string
            id del repartidor

        Returns:
        --------
        int
            204 si ha sido eliminado exitosamente
        """
        id = request.json.get('id')
        db = database.RepartidorDB()
        try:
            db.delete("repartidores", {"id": id})
        except database.db.DataNotFoundError as e:
            return {e}, 400
        db.close()
        return 204

class Stats:
    @app.route('/stats', methods=['GET'])
    def get_stats():
        """
        WIP
        Devuelve un informe con los datos pedidos
        """
        return 'Not yet implemented', 501

@app.route('/test', methods=['GET'])
@jwt_required()
def test():
    return 'Secret!', 200

if __name__ == '__main__':
    app.run(debug=False)