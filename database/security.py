import bcrypt

class Security:
    
    @staticmethod
    def hash_password(password):
        KEY = Security.get_key().encode('utf-8')
        hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.hashpw(KEY, bcrypt.gensalt()))
        return hash.decode('utf-8')
    
    @staticmethod
    def verify_password(password, hash):
        return bcrypt.checkpw(password.encode(), hash.encode())
    
    @staticmethod
    def check_password_strength(password):
        mayus = any(letter.isupper() for letter in password)
        minus = any(letter.islower() for letter in password)
        num = any(letter.isdigit() for letter in password)
        especial = any(letter in '!@#$%^&*()_+.' for letter in password)
        
        if len(password) < 8 or not (mayus and minus and num and especial):
            return 401 # Contraseña invalida
        
        return 200