def menu():
    print("Bienvenido al sistema!")
    print('-' * 30)
    print("1. Activar servidor")
    print("2. Crear usuario")
    print("3. Iniciar sesión")
    print("4. Salir")
    print('-' * 30)
    option = input("Seleccione una opción: ")

    match option:
        case "1":
            print("Activando servidor...")
            pass
        case "2":
            print("Crear usuario seleccionado.")
            print('-' * 30)
            username = input("Ingrese el nombre de usuario: ")
            password = input("Ingrese la contraseña: ")

            if username:
                print("El usuario ya existe.")
                return
            if len(password) < 8:
                print("La contraseña debe tener al menos 8 caracteres.")
                return
            print("Usuario creado con éxito.")
    
        case "3":
            print("Iniciar sesión seleccionado.")
        case "4":
            print("Saliendo del sistema...")
            exit()
        case _:
            print("Opción no válida. Intente de nuevo.")



menu()