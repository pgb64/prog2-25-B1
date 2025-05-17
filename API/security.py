import hashlib
import os
import base64

class Security:
    '''
    Clase para manejar la seguridad de las contraseñas

    Métodos:
    -------
    hash_password(password: str) -> str
        Genera el hash de una contraseña utilizando PBKDF2 con hashlib
    verify_password(password: str, hash: str) -> bool
        Verifica si la contraseña coincide con el hash proporcionado
    check_password_strength(password: str) -> int
        Valida la fortaleza de la contraseña
    '''
    
    @staticmethod
    def hash_password(password):
        '''
        Genera el hash de una contraseña utilizando PBKDF2 con hashlib
        
        Parámetros:
        -----------
        password : str
            La contraseña que será cifrada
        
        Retorna:
        --------
        str
            La contraseña cifrada como un string
        '''
        salt = os.urandom(32)
        
        #Genero un hash de PBKDF2 con y le pongo 100000 iteraciones (No se si es mucho o poco)
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        
        #Combinación de salt y hash codificados en base64 para almacenamiento
        hashed = base64.b64encode(salt + key).decode('utf-8')
        return hashed
    
    @staticmethod
    def verify_password(password, storage):
        '''
        Verifica si la contraseña proporcionada coincide con el hash
        
        Parámetros:
        -----------
        password : str
            La contraseña que será verificada
        storage : str
            El hash+salt de la contraseña almacenados
        
        Devuelve:
        --------
        bool
            True si las contraseñas coinciden, False si no
        '''
        try:
            #Decodificaa la combinacion de salt+hash
            decoded = base64.b64decode(storage.encode('utf-8'))
            
            salt = decoded[:32]
            
            key = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt,
                100000
            )
            
            #Compararamos el hash generado con el almacenado
            return decoded[32:] == key
        except:
            return False
    
    @staticmethod
    def check_password_strength(password):
        '''
        Valida la fortaleza de la contraseña
        
        Parámetros:
        -----------
        password : str
            La contraseña a validar
        
        Devuelve:
        --------
        int
            True si la contraseña es válida, False si no cumple con los requisitos
        '''
        mayus = any(letter.isupper() for letter in password)
        minus = any(letter.islower() for letter in password)
        num = any(letter.isdigit() for letter in password)
        especial = any(letter in '!@#$%^&*()_+.' for letter in password)
        
        if len(password) < 8 or not (mayus and minus and num and especial):
            return False
        
        return True
