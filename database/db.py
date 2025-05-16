import sqlite3
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
DB_NAME = os.path.join(DATA_DIR, 'base_de_datos.db')

class DatabaseBase:
    def __init__(self, db_name: str = DB_NAME):
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)  
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        
        #Tabla para user_db.py
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            type TEXT NOT NULL
        )
        ''')
        
        #Tabla para user_db.py
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS personal_data (
            id INTEGER PRIMARY KEY,
            fecha TEXT,
            direccion TEXT,
            cp TEXT,
            ciudad TEXT,
            genero TEXT,
            FOREIGN KEY (id) REFERENCES users(id) ON DELETE CASCADE
        )
        ''')
        
        #Tabla para articulo_db.py
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS articulos (
            nombre TEXT NOT NULL,
            codigo TEXT PRIMARY KEY,
            cantidad INTEGER NOT NULL,
            proveedor TEXT,
            descripcion TEXT
        )
        ''')
        
        #Tabla para paquete_db.py
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS paquetes (
            codigo_paquete TEXT PRIMARY KEY,
            direccion TEXT NOT NULL,
            usuario_id INTEGER NOT NULL,
            contenido TEXT NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES users(id)
        )
        ''')
        
        #Tabla para repartidor_db.py
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS repartidores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            provincia TEXT NOT NULL,
            ubicacion_tiempo_real TEXT,
            vehiculo TEXT NOT NULL,
            estado TEXT DEFAULT 'disponible',
            envios_asignados INTEGER DEFAULT 0
        )
        ''')
        
        #Tabla para furgoneta_db.py
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS furgonetas (
            matricula TEXT PRIMARY KEY,
            capacidad_maxima INTEGER NOT NULL,
            provincia TEXT NOT NULL,
            envios_asignados INTEGER DEFAULT 0,
            conductor_id INTEGER,
            FOREIGN KEY (conductor_id) REFERENCES repartidores(id)
        )
        ''')
        self.conn.commit()

    def close(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
