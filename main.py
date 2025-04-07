from menu import Menu

def main():
    print("Iniciando sistema...")
    try:
        print(cargar_datos_iniciales())
    except Exception as e:
        print(f"Advertencia: Falló la carga inicial de datos ({e}).")

    menu_app = Menu()
    menu_app.ejecutar()

    print("Programa finalizado.")

if __name__ == "__main__":
    main()