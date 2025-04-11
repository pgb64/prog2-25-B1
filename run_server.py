# Importamos el módulo Server desde el paquete sistema
from sistema import Server

# Al ejecutar el archivo se lanza el servidor
if __name__ == "__main__":
    launcher = Server()
    launcher.launch()