import requests
import menu

def main():
    url = 'https://ruukha.pythonanywhere.com'

    #inicio
    print('--- Gestión de repartos ---')
    print('1. Iniciar sesión')
    print('2. Crear cuenta')

    #bucle de selección
    while True:
        op = input('Selección: ')
        try:
            if op not in ['1', '2']:
                raise TypeError
            op = int(op)
            break
        except:
            print('Introduce una selección válida.')
            continue

    #bucle para introducir la cuenta
    while True:
        email = input('Introduce tu correo: ')
        password = input('Introduce tu contraseña: ')
        credentials = {'email': email, 'password': password}
        if op == 1:
            res = requests.post(f'{url}/login', json=credentials)
        if op == 2:
            res = requests.post(f'{url}/signup', json=credentials)

        try:
            token = res.json()["token"]
            break
        except Exception as e:
            print(res.text)
            if res.text == 'Este usuario ya existe':
                op = input('Quiere iniciar sesión? (s/n): ')
                if op == 's':
                    op = 1
                    continue
                else:
                    break

    #abrir el menú
    if requests.get(f'{url}/is_admin', json={'email': email}):
        menu.menu_vendedor(url, email)
    else:
        menu.menu_usuario(url)


if __name__ == '__main__':
    main()