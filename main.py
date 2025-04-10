import requests
from sistema import ApiResponse
import time

class MenuLogin():
    path = ApiResponse.path  # Ruta base de la API
    def __init__(self):
        self.api = ApiResponse()
        self.user = None
        self.password = None
        self.token = None
    
    @staticmethod
    def effect():
        '''
        Efecto de carga
        '''
        for _ in range(3):
            for i in range(3):
                time.sleep(0.1)
                print('.', end='')  # Efecto de puntos de carga
            print('\r', end='')  # Regresa a la misma línea para borrar los puntos

    def login(self):
        '''
        Lógica para iniciar sesión
        '''
        user = input('Usuario: ')
        password = input('Contraseña: ')
        login_url = f'{self.path}/login?user={user}&password={password}'

        try:
            response = requests.get(login_url)

            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success':
                    self.token = data['access_token']  # Guarda el token
                    print('Inicio de sesión exitoso.')
                    return True
                else:
                    print('Error: ', data['message'])
                    return False
            else:
                print('Error: ', response.status_code)
                return False
                
        except requests.exceptions.RequestException as e:
            print('Error: ', e)
            return False

    def signup(self):
        '''
        Lógica para registrar un nuevo usuario
        '''
        user = input('Usuario: ')
        password = input('Contraseña: ')

        signup_url = f'{self.path}/signup'

        data = {
            'user': user,
            'password': password
        }

        try:
            # Realizar la solicitud POST para crear el usuario
            response = requests.post(signup_url, json=data)

            if response.status_code == 201:
                print('Usuario creado exitosamente.')
                return True
            elif response.status_code == 409:
                print('El usuario ya existe.')
                return False
            else:
                print(f'Error al crear el usuario: {response.json()["message"]}')
                return False

        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con el servidor: {e}")
            return False

    def logout(self):
        '''
        Lógica para cerrar sesión
        '''
        self.token = None
        print('Sesión cerrada.')

    def menu_login(self):
        '''
        Menú principal de inicio de sesión y registro
        '''
        while True:
            print('Bienvenido a TuPaquete')
            print('-'*20)
            print('1. Iniciar sesión')
            print('2. Registrarse')
            print('3. Salir')
            print('-'*20)
            option = input('Elige una opción: ')

            if option == '1':
                if self.login():
                    self.effect()  # Efecto de carga
                    print("Pasando al siguiente menú...")
                    # Aquí podrías pasar al siguiente menú después del login exitoso

            elif option == '2':
                if self.signup():
                    self.effect()  # Efecto de carga
                    print("Pasando al siguiente menú...")
                    # Aquí podrías pasar al siguiente menú después de registrarse

            elif option == '3':
                print('Saliendo...')
                break

class MainMenu():
    def __init__(self):
        pass

if __name__ == '__main__':
    menu = MenuLogin()
    menu.menu_login()
