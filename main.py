import requests
from sistema import ApiResponse
import time

class MenuLogin():
    path = ApiResponse.path
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
                print('.', end='')  
            print('\r', end='') 

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
                self.token = data.get('access_token')
                return True
            elif response.status_code == 400:
                print('Error: Usuario no encontrado.')
                return False
            elif response.status_code == 401:
                print('Error: Contraseña inválida.')
                return False
            else:
                print(f'Error: {response.status_code}')
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
            response = requests.post(signup_url, json=data)

            if response.status_code == 201:
                print('Usuario creado exitosamente.')
                return True
            elif response.status_code == 409:
                print('El usuario ya existe.')
                return False
            elif response.status_code == 400:
                try:
                    error_message = response.json().get("message", "Error desconocido")
                except ValueError:
                    error_message = "Respuesta inválida del servidor"
                print(f"Error: {error_message}")
                return False
            else:
                print(f"Error inesperado: {response.status_code}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con el servidor: {e}")
            return False


    def menu_login(self):
        '''
        Menú principal de inicio de sesión y registro
        '''
        while True:
            print('-'*20)
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
                    ... # Aquí puedes agregar la lógica para el menú principal después de iniciar sesión

            elif option == '2':
                if self.signup():
                    self.effect() 

            elif option == '3':
                print('Saliendo...')
                break

class MainMenu():
    def __init__(self):
        pass

if __name__ == '__main__':
    menu = MenuLogin()
    menu.menu_login()
