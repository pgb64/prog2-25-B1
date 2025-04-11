import requests
from sistema import ApiResponse
import time
from database.db import Db
from articulos_paquetes.paquetes import *

db=Db() #inicializo la base de datos

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
                self.user = user
                self.password = password
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
        print("\n=== REQUISITOS DE REGISTRO ===")
        print("• Usuario: Debe ser único en el sistema")
        print("• Contraseña: Debe contener al menos:")
        print("  - 8 caracteres")
        print("  - Una letra mayúscula")
        print("  - Una letra minúscula")
        print("  - Un número")
        print("  - Un carácter especial (!@#$%^&*()_+.)")
        print("• Tipos de cuenta:")
        print("  - Usuario: Acceso básico al sistema")
        print("  - Trabajador: Acceso a funciones de gestión de envíos")
        print("  - Administrador: Acceso completo a todas las funciones")
        print("===============================\n")
        
        user = input('Usuario: ')
        password = input('Contraseña: ')
        
        # Solicitar tipo de usuario
        print("\nSeleccione tipo de cuenta:")
        print("1. Usuario")
        print("2. Trabajador")
        print("3. Administrador")
        
        type_option = input("Opción: ")
        
        # Mapear opción a tipo
        type_mapping = {
            "1": "user",
            "2": "worker", 
            "3": "admin"
        }
        
        user_type = type_mapping.get(type_option)
        
        if not user_type:
            print("Opción inválida. Se asignará 'user' por defecto.")
            user_type = "user"

        signup_url = f'{self.path}/signup'

        data = {
            'user': user,
            'password': password,
            'type': user_type
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
                    self.effect()  
                    print('')
                    print(self.user, self.password, self.token)

            elif option == '2':
                if self.signup():
                    self.effect() 

            elif option == '3':
                print('Saliendo...')
                break

class MainMenu(MenuLogin):
    
    def __init__(self):
        super().__init__()
    
    def main_menu(self):
        '''
        Menú principal después de iniciar sesión
        '''
        while True:
            print('-'*20)
            print('TuPaquete - Menú Principal')
            print('-'*20)
            print('1. Ver articulos')
            print('2. Crear pedido')
            print('3. Salir')
            print('-'*20)
            option = input('Elige una opción: ')

            if option == '1':
                # Lógica para ver articulos
                print(db.get_articulos())

            elif option == '2':
                # Lógica para crear pedido
                dp=input('Introduce tu direccion postal: ')
                el=input('Introduce el código del paquete que deseas: ')
                try:
                    if el in db.get_articulos():
                        controlador_crear_paquete(usuario=MenuLogin.user,direcion=dp,id_contenido=el)
                    else:
                        raise ValueError
                except:
                    print('El índice seleccionado no existe')
                

            elif option == '3':
                print('Saliendo...')
                break


if __name__ == '__main__':
    
    menu = MenuLogin()
    menu.menu_login()
