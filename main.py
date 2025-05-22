import requests
import menu

def main():
    url = 'https://ruukha.pythonanywhere.com'

    #inicio
    print('--- Gestión de repartos ---')
    print('1. Iniciar sesión')
    print('2. Crear cuenta')
    print('3. Salir')

    #bucle de selección
    while True:
        op = input('\nSelección: ')
        try:
            if op not in ['1', '2', '3']:
                raise TypeError
            
            if op == '3':
                return 0
            
            break

        except:
            print('Introduce una selección válida.')
            continue

    #bucle para introducir la cuenta
    while True:
        email = input('\nIntroduce tu correo: ')
        password = input('Introduce tu contraseña: ')
        credentials = {'email': email, 'password': password}
        if op == '1':
            res = requests.post(f'{url}/login', json=credentials)
        if op == '2':
            res = requests.post(f'{url}/signup', json=credentials)

        try:
            token = res.json()["token"]
            break
        except:
            print(res.text)
            if res.text == 'El usuario no existe':
                print('\nCrear una cuenta:')
                op = '2'
            if res.text == 'Este usuario ya existe':
                op = input('Quiere iniciar sesión? (s/n): ')
                if op == 's':
                    op = '1'
                    continue
                else:
                    return 0

    #abrir el menú
    res = requests.get(f'{url}/is_admin', json={'email': email}).text
    if res == 'True':
        menu.menu_vendedor(url, email)
    else:
        menu.menu_usuario(url)


if __name__ == '__main__':
    main()