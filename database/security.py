import bcrypt

class Security:
    '''
    Clase para manejar la seguridad de las contraseñas

    Métodos:
    -------
    hash_password(password: str) -> str
        Genera el hash de una contraseña utilizando bcrypt
    verify_password(password: str, hash: str) -> bool
        Verifica si la contraseña coincide con el hash proporcionado
    check_password_strength(password: str) -> int
        Valida la fortaleza de la contraseña
    '''
    
    @staticmethod
    def hash_password(password):
        '''
        Genera el hash de una contraseña utilizando bcrypt
        
        Parámetros:
        -----------
        password : str
            La contraseña que será cifrada
        
        Retorna:
        --------
        str
            La contraseña cifrada como un string
        '''
        hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hash.decode('utf-8')
    
    @staticmethod
    def verify_password(password, hash):
        '''
        Verifica si la contraseña proporcionada coincide con el hash
        
        Parámetros:
        -----------
        password : str
            La contraseña que será verificada
        hash : str
            El hash de la contraseña que se desea verificar
        
        Retorna:
        --------
        bool
            True si las contraseñas coinciden, False si no
        '''
        return bcrypt.checkpw(password.encode(), hash.encode())
    
    @staticmethod
    def check_password_strength(password):
        '''
        Valida la fortaleza de la contraseña, asegurando que cumpla con ciertos requisitos:
        - Longitud mínima de 8 caracteres
        - Al menos una mayúscula, una minúscula, un número y un carácter especial
        
        Parámetros:
        -----------
        password : str
            La contraseña a validar
        
        Retorna:
        --------
        int
            200 si la contraseña es válida, 401 si no cumple con los requisitos
        '''
        mayus = any(letter.isupper() for letter in password)
        minus = any(letter.islower() for letter in password)
        num = any(letter.isdigit() for letter in password)
        especial = any(letter in '!@#$%^&*()_+.' for letter in password)
        
        if len(password) < 8 or not (mayus and minus and num and especial):
            return 401  # Contraseña inválida
        
        return 200
