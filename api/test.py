import requests
from api.servidor import Server, server
from api.excepcion import Except

if __name__ == '__main__':

    response = requests.get('http://127.0.0.1:5000')
    print(response.status_code)
    print(response.text)


    print('---------------------------------------------')
    server = Server()
    print(server.path)
    print('---------------------------------------------')
    print(Server.get_state(Server.path))
