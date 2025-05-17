from flask import Flask, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import hashlib
from security import Security
import database

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret'
jwt = JWTManager(app)

@app.route('/')
def home():
    return 'Hello World', 200

#@app.route('/paquetes', methods=['GET', 'POST'])
class Paquetes:
    @app.route('/paquetes/<cod>', methods=['GET'])
    def get(cod):
        return {f'Paquete {cod}': Paquetes.paquetes[int(cod)]}
    
    @app.route('/paquetes/nuevo', methods=['POST'])
    def post():
        data = request.form
        return {'data': data}

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
                return 'Este usuario ya existe', 409
            finally:
                db.close()

            token = create_access_token(identity=email)
            return {'token': token}, 200

        except TypeError as e: 
            return f'How did you get here? {e}', 400

    @app.route('/login', methods=['POST'])
    def login():
        try:
            email = request.json.get('email', None)
            password = request.json.get('password', None)
            hashed = hashlib.sha256(password.encode()).hexdigest()

            if not email:
                return 'Missing email', 400
            if not password:
                return 'Missing password', 400
            
            db = database.UserDB()
            if hashed == db.get_user(username=email)['password']: #if user in users and hashed == users[email[hash]]
                return {'token': create_access_token(identity=email)}, 200
            
            return 'Something went wrong', 500
            
        except TypeError as e:
            return f'How did you get here? {e}', 400

@app.route('/test', methods=['GET'])
@jwt_required()
def test():
    return 'Secret!', 200

if __name__ == '__main__':
    app.run(debug=False)