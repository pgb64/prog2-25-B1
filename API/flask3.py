from _sqlite3 import IntegrityError, Error
from flask import Flask, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from security import Security
import database

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'prog2-25-B1'
jwt = JWTManager(app)

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
        email = request.json.get('email', None)
        db = database.UserDB()
        is_admin = db.is_admin(email)
        db.close()
        return is_admin, 200

class Articulo:
    @app.route('/articulos', methods=['POST'])
    def add_art():
        data = request.get_json()
        db = database.ArticuloDB()
        db.insert("articulos", data)
        db.close()
        return 201

    @app.route('/articulos', methods=['GET'])
    def get_art():
        db = database.ArticuloDB()
        data = db.get("articulos")
        db.close()
        return data, 200

    @app.route('/articulos', methods=['DELETE'])
    def delete_art():
        cod = request.json.get('cod')
        db = database.ArticuloDB()
        db.delete("articulos", {'codigo': cod})
        db.close()
        return 204

class Paquete:
    @app.route('/paquetes/<cod>', methods=['GET'])
    def get_by_cod(cod):
        db = database.PaqueteDB()
        info = db.get_paquete_by_codigo(cod)
        db.close()
        if info == [] or info == {}:
            return 'Código de paquete no encontrado', 404
        return info, 200

    @app.route('/pedidos', methods=['POST'])
    def add_paq():
        return 'Lo sentimos, aún estamos trabajando en ello', 501

class Repartidor:
    @app.route('/repartidores', methods=['POST'])
    def add_rep():
        data = request.get_json()
        db = database.RepartidorDB()
        db.insert("repartidores", data)
        db.close()
        return 201

    @app.route('/repartidores', methods=['GET'])
    def get_rep():
        db = database.RepartidorDB()
        data = db.get("repartidores")
        db.close()
        return data, 200

    @app.route('/repartidores', methods=['DELETE'])
    def delete_rep():
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
        return 'Not yet implemented', 501

@app.route('/test', methods=['GET'])
@jwt_required()
def test():
    return 'Secret!', 200

if __name__ == '__main__':
    app.run(debug=False)