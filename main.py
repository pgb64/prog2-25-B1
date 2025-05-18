import subprocess
import os
import requests
import menu

def main():
    print('--- Gestión de repartos ---')
    print('1. Iniciar sesión')
    print('2. Crear cuenta')
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
    while True:
        email = input('Introduce tu correo: ')
        password = input('Introduce tu contraseña: ')
        credentials = {'email': email, 'password': password}
        if op == 1:
            res = requests.post('https://ruukha.pythonanywhere.com/login', json=credentials)
        if op == 2:
            res = requests.post('https://ruukha.pythonanywhere.com/signup', json=credentials)

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


if __name__ == '__main__':
    main()