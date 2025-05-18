from flask import Flask, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import hashlib
from security import Security
import database

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'prog2-25-B1'
jwt = JWTManager(app)

@app.route('/')
def home():
    return 'Home', 200

class Usuario:
    @app.route('/signup', methods=['POST'])
    def signup():
        try:
            email = request.json.get('email', None)
            password = request.json.get('password', None)
            admin = request.json.get('admin', False)

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
            return {'token': token}, 200

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

@app.route('/test', methods=['GET'])
@jwt_required()
def test():
    return 'Secret!', 200

if __name__ == '__main__':
    app.run(debug=False)