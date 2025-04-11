# Importamos los módulos necesarios
import requests
from sistema import ApiResponse
import time


class MenuLogin():
    '''
    Clase para gestionar el menú de inicio de sesión y registro

    Atributos:
    ----------
    api : ApiResponse
        Instancia de la clase ApiResponse para gestionar la API.
    user : str
        Nombre de usuario del cliente.
    password : str
        Contraseña del cliente.
    token : str
        Token de acceso del cliente.
    path : str
        URL base de la API.
    '''
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
        # Solicitar usuario y contraseña
        user = input('Usuario: ')
        password = input('Contraseña: ')
        # URL de inicio de sesión
        login_url = f'{self.path}/login?user={user}&password={password}'

        # Realizar la solicitud de inicio de sesión
        try:
            response = requests.get(login_url)

            # Verificar si todo funciona bien
            if response.status_code == 200:
                data = response.json()
                self.user = user
                self.password = password
                self.token = data.get('access_token')
                return True
            # Si no se encuentra el usuario
            elif response.status_code == 400:
                print('Error: Usuario no encontrado.')
                return False
            # Si la contraseña es incorrecta
            elif response.status_code == 401:
                print('Error: Contraseña inválida.')
                return False
            # Si sucede cualquier otro error
            else:
                print(f'Error: {response.status_code}')
                return False
        # Por si sucede un error de conexión 
        except Exception as e:
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

        # Pedir usuario y contraseña
        user = input('Usuario: ')
        password = input('Contraseña: ')
        
        # Solicitar tipo de usuario
        print("\nSeleccione tipo de cuenta:")
        print("1. Usuario")
        print("2. Trabajador")
        print("3. Administrador")
        
        type_option = input("Opción: ")
        
        # Mapear opción a tipo
        type_status = {
            "1": "user",
            "2": "worker", 
            "3": "admin"
        }
        
        user_type = type_status.get(type_option)
        
        # Validar tipo de usuario
        if not user_type:
            print("Opción inválida. Se asignará 'user' por defecto.")
            user_type = "user"

        # URL de registro
        signup_url = f'{self.path}/signup'

        data = {
            'user': user,
            'password': password,
            'type': user_type
        }

        # Realizar la solicitud de registro a la api
        try:
            response = requests.post(signup_url, json=data)
            # Verificar si la solicitud fue exitosa
            if response.status_code == 201:
                print('Usuario creado exitosamente.')
                return True
            # Si el usuario ya existe
            elif response.status_code == 409:
                print('El usuario ya existe.')
                return False
            # Si la contraseña no cumple con los requisitos
            elif response.status_code == 400:
                try:
                    error_message = response.json().get("message", "Error desconocido")
                except ValueError:
                    error_message = "Respuesta inválida del servidor"
                print(f"Error: {error_message}")
                return False
            # Si el tipo de usuario no es válido
            else:
                print(f"Error inesperado: {response.status_code}")
                return False
        # Por si sucede un error de conexión
        except Exception as e:
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
    '''
    Una vez pasado el login se pasa al menú real de la aplicación
    '''
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
            print('1. Ver pedidos')
            print('2. Crear pedido')
            print('3. Salir')
            print('-'*20)
            option = input('Elige una opción: ')

            if option == '1':
                # Lógica para ver pedidos
                pass

            elif option == '2':
                # Lógica para crear pedido
                pass

            elif option == '3':
                print('Saliendo...')
                break


if __name__ == '__main__':
    
    menu = MenuLogin()
    menu.menu_login()
