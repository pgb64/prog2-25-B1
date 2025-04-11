import bcrypt

class Security:
    
    @staticmethod
    def hash_password(password):
        hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hash.decode('utf-8')
    
    @staticmethod
    def verify_password(password, hash):
        return bcrypt.checkpw(password.encode(), hash.encode())
    
    @staticmethod
    def check_password_strength(password):
        print(f"Validando fortaleza de la contraseña: {password}")  # Depuración
        mayus = any(letter.isupper() for letter in password)
        minus = any(letter.islower() for letter in password)
        num = any(letter.isdigit() for letter in password)
        especial = any(letter in '!@#$%^&*()_+.' for letter in password)
        
        print(f"Mayúsculas: {mayus}, Minúsculas: {minus}, Números: {num}, Especiales: {especial}")  # Depuración
        if len(password) < 8 or not (mayus and minus and num and especial):
            print("Contraseña no cumple con los requisitos")  # Depuración
            return 401  # Contraseña inválida
        
        print("Contraseña válida")  # Depuración
        return 200