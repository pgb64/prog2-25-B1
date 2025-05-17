import sqlite3
import os
from typing import Dict, List, Any, Tuple, Union

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
DB_NAME = os.path.join(DATA_DIR, 'base_de_datos.db')

class DatabaseBase:
    _custom_queries = {}
    
    def __init__(self, db_name: str = DB_NAME):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
    
    def add(self, table: str, query_name: str, query_string: str):
        self._custom_queries.setdefault(table, {})[query_name] = query_string
    
    def execute_query(self, query: str, params: Tuple = (), commit: bool = False):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            if commit:
                self.conn.commit()
                return cursor.rowcount
            return cursor
        except sqlite3.IntegrityError as e:
            print(f"Error de integridad: {e}")
            return None, 409
        except sqlite3.Error as e:
            return None, 400
    
    def get(self, table: str, conditions: Dict = None, fetch_all: bool = True):
        """Obtiene registros de una tabla"""
        query = f"SELECT * FROM {table}"
        params = []
        
        if conditions:
            clauses = [f"{col} = ?" for col in conditions]
            query += " WHERE " + " AND ".join(clauses)
            params = list(conditions.values())
        
        try:
            resultado = self.execute_query(query, tuple(params))
            if isinstance(resultado, tuple) and resultado[0] is None:
                return [] if fetch_all else {}
            cursor = resultado 
            
            if fetch_all:
                rows = cursor.fetchall()
                return [dict(row) for row in rows] if rows else []
            else:
                row = cursor.fetchone()
                return dict(row) if row else {}
        except Exception as e:
            print(f"Error en get: {e}")
            return [] if fetch_all else {}
    
    def insert(self, table: str, data: Dict):
        """Inserta un registro y retorna el código de estado"""
        cols = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        query = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
        
        resultado = self.execute_query(query, tuple(data.values()), commit=True)
        
        if isinstance(resultado, tuple):
            return resultado[1]
        return 201
    
    def update(self, table: str, data: Dict, conditions: Dict):
        """Actualiza registros y retorna el código de estado"""
        if not data:
            return 304 #ESTE CODIGO ES PARA NO MODIFICAR NADA
        
        set_clause = ", ".join([f"{col} = ?" for col in data.keys()])
        where_clause = " AND ".join([f"{col} = ?" for col in conditions.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        
        params = list(data.values()) + list(conditions.values())
        resultado = self.execute_query(query, tuple(params), commit=True)
        if isinstance(resultado, tuple):
            return resultado[1]
        return 404 if resultado == 0 else 200
    
    def delete(self, table: str, conditions: Dict):
        """Elimina registros y retorna el código de estado"""
        where_clause = " AND ".join([f"{col} = ?" for col in conditions.keys()])
        query = f"DELETE FROM {table} WHERE {where_clause}"
        
        resultado = self.execute_query(query, tuple(conditions.values()), commit=True)
        
        if isinstance(resultado, tuple):
            return resultado[1]
        return 404 if resultado == 0 else 200
    
    def execute_custom_query(self, table: str, query_name: str, params: Tuple = (), fetch_all: bool = True):
        """Ejecuta una consulta personalizada registrada previamente"""
        table_queries = self._custom_queries.get(table, {})
        if query_name not in table_queries:
            print(f"Consulta '{query_name}' no encontrada para tabla '{table}'")
            return [] if fetch_all else {}
            
        resultado = self.execute_query(table_queries[query_name], params)
        if isinstance(resultado, tuple) and resultado[0] is None:
            return [] if fetch_all else {}
        
        cursor = resultado
        
        if fetch_all:
            rows = cursor.fetchall()
            return [dict(row) for row in rows] if rows else []
        else:
            row = cursor.fetchone()
            return dict(row) if row else {}

    def create_tables(self):
        tables = [
            '''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                user TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL, 
                type TEXT NOT NULL)''',
                
            '''CREATE TABLE IF NOT EXISTS personal_data (
                id INTEGER PRIMARY KEY, 
                fecha TEXT,
                dir TEXT, 
                cp TEXT,
                ciudad TEXT, 
                genero TEXT,
                FOREIGN KEY (id) REFERENCES users(id) ON DELETE CASCADE)''',
                
            '''CREATE TABLE IF NOT EXISTS articulos (
                nombre TEXT NOT NULL, 
                codigo TEXT PRIMARY KEY, 
                cantidad INTEGER NOT NULL,
                proveedor TEXT, 
                descripcion TEXT)''',
                
            '''CREATE TABLE IF NOT EXISTS paquetes (
                codigo_paquete TEXT PRIMARY KEY, 
                direccion TEXT NOT NULL, 
                usuario INTEGER NOT NULL, 
                contenido TEXT NOT NULL,
                origen TEXT,
                destino TEXT,
                FOREIGN KEY (usuario) REFERENCES users(id))''',
                
            '''CREATE TABLE IF NOT EXISTS repartidores (
                nombre TEXT NOT NULL,
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                telefono TEXT NOT NULL, 
                provincia TEXT NOT NULL, 
                ubicacion_tiempo_real TEXT,
                vehiculo TEXT NOT NULL, 
                estado TEXT DEFAULT 'disponible',
                envios_asignados INTEGER DEFAULT 0)''',
                
            '''CREATE TABLE IF NOT EXISTS furgonetas (
                matricula TEXT PRIMARY KEY, 
                capacidad_maxima INTEGER NOT NULL,
                provincia TEXT NOT NULL, 
                envios_asignados INTEGER DEFAULT 0,
                conductor INTEGER, 
                FOREIGN KEY (conductor) REFERENCES repartidores(id))'''
        ]
        cursor = self.conn.cursor()
        for sql in tables:
            cursor.execute(sql)
        self.conn.commit()

    def close(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

class AlreadyExistsError(Exception):
    pass