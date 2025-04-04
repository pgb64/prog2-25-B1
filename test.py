from api import server
import requests
url = server.path
ruta = server.path + '/get_all_data_public'

response = requests.get(ruta)

code = response.status_code


todo = response.json()
data = todo.get('data')


print(response)
print(code)
print(todo)
print(data)
