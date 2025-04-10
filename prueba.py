from articulos_paquetes.articulos import *
from articulos_paquetes.paquetes import *
from database.db import Db

db=Db()

print(db.get_articulos())

controlador_ver_paquete('A113')