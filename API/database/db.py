import sqlite3
import os
from typing import Dict, List, Any, Tuple, Union, Optional

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
DB_NAME = os.path.join(DATA_DIR, 'base_de_datos.db')

class DatabaseBase:
    """
    Clase base para operaciones de base de datos.
    
    Proporciona funciones comunes para realizar operaciones CRUD en la 
    base de datos SQLite.
    
    Atributos
    ---------
    _custom_queries : Dict
        Diccionario con consultas personalizadas
    conn : sqlite3.Connection
        Conexion a la base de datos
    """
    _custom_queries = {}
    
    def __init__(self, db_name: str = DB_NAME):
        """
        Inicializa la conexión a la base de datos.
        
        Parameters
        ----------
        db_name : str, optional
            Ruta del archivo de BD (por defecto es DB_NAME)
        """
        os.makedirs(DATA_DIR, exist_ok=True)
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
    
    def add(self, table: str, query_name: str, query_string: str) -> None:
        """
        Registra una consulta personalizada.
        
        Parameters
        ----------
        table : str
            Nombre de la tabla
        query_name : str
            Identificador de la consulta
        query_string : str
            Consulta SQL 
        """
        self._custom_queries.setdefault(table, {})[query_name] = query_string
    
    def execute_query(self, query: str, params: Tuple = (), commit: bool = False) -> Union[sqlite3.Cursor, int]:
        """
        Ejecuta una consulta SQL.
        
        Parameters
        ----------
        query : str
            Consulta SQL a ejecutar
        params : Tuple, optional
            Parametros para la consulta
        commit : bool, optional
            Si hay que hacer commit (por defecto False)
        
        Returns
        -------
        Union[sqlite3.Cursor, int]
            Cursor o numero de filas afectadas
        """
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        if commit:
            self.conn.commit()
            return cursor.rowcount
        return cursor
    
    def get(self, table: str, conditions: Optional[Dict] = None, fetch_all: bool = True) -> Union[List[Dict], Dict]:
        """
        Obtiene registros de una tabla.
        
        Permite buscar registros en una tabla opcionalmente filtrando 
        por condiciones especificadas.
        
        Parameters
        ----------
        table : str
            Nombre de la tabla
        conditions : Dict, optional
            Condiciones para filtrar (por defecto None)
        fetch_all : bool, optional
            Si se obtienen todos los resultados o solo uno
        
        Returns
        -------
        Union[List[Dict], Dict]
            Lista de diccionarios o un solo diccionario
        """
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
    
    def insert(self, table: str, data: Dict) -> int:
        """
        Inserta un registro en una tabla.
        
        Parameters
        ----------
        table : str
            Tabla donde insertar
        data : Dict
            Datos a insertar como diccionario
        
        Returns
        -------
        int
            Codigo de estado (0 = exito)
            
        Raises
        ------
        IntegrityError
            Si hay conflicto de clave unica
        """
        cols = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        query = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
        
        resultado = self.execute_query(query, tuple(data.values()), commit=True)
        
        if isinstance(resultado, tuple):
            return resultado[1]
        return 0  # 201
    
    def update(self, table: str, data: Dict, conditions: Dict) -> int:
        """
        Actualiza registros en una tabla.
        
        Parameters
        ----------
        table : str
            Tabla a actualizar
        data : Dict
            Datos a actualizar
        conditions : Dict
            Condiciones para el WHERE
        
        Returns
        -------
        int
            Codigo de estado (0 = exito, 304 = sin cambios)
        
        Raises
        ------
        DataNotFoundError
            Si no se encontro ningun registro con esas condiciones
        """
        if not data:
            return 304  #ESTE CODIGO ES PARA NO MODIFICAR NADA
        
        set_clause = ", ".join([f"{col} = ?" for col in data.keys()])
        where_clause = " AND ".join([f"{col} = ?" for col in conditions.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        
        params = list(data.values()) + list(conditions.values())
        resultado = self.execute_query(query, tuple(params), commit=True)
        if isinstance(resultado, tuple):
            return resultado[1]
        if resultado == 0:
            raise DataNotFoundError  #404
        return 0  #200
    
    def delete(self, table: str, conditions: Dict) -> int:
        """
        Elimina registros de una tabla.
        
        Parameters
        ----------
        table : str
            Tabla donde eliminar
        conditions : Dict
            Condiciones para el WHERE
        
        Returns
        -------
        int
            Codigo de estado (200 = exito)
        
        Raises
        ------
        DataNotFoundError
            Si no se encontraros registros a eliminar
        """
        where_clause = " AND ".join([f"{col} = ?" for col in conditions.keys()])
        query = f"DELETE FROM {table} WHERE {where_clause}"
        
        resultado = self.execute_query(query, tuple(conditions.values()), commit=True)
        
        if isinstance(resultado, tuple):
            return resultado[1]
        if resultado == 0:
            raise DataNotFoundError('El repartidor no existe')
        return 200
    
    def execute_custom_query(self, table: str, query_name: str, params: Tuple = (), fetch_all: bool = True) -> Union[List[Dict], Dict]:
        """
        Ejecuta una consulta personalizada registrada.
        
        Parameters
        ----------
        table : str
            Tabla asociada a la consulta
        query_name : str
            Nombre de la consulta
        params : Tuple, optional
            Parametros para la consulta
        fetch_all : bool, optional
            Si se obtienen todos los resultados o solo uno
        
        Returns
        -------
        Union[List[Dict], Dict]
            Lista de diccionarios o un solo diccionario
        """
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

    def create_tables(self) -> None:
        """
        Crea las tablas si no existen.
        
        Crea la estructura basica de las tablas para la aplicacion.
        """
        tables = [
            '''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                user TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL, 
                admin BOOLEAN NOT NULL DEFAULT 0)''',
                
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

    def close(self) -> None:
        """
        Cierra la conexion a la base de datos.
        
        Es importante llamar a este metodo al finalizar
        para liberar recursos.
        """
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()


class AlreadyExistsError(Exception):
    """Error que se produce cuando se intenta crear algo que ya existe."""
    pass

class DataNotFoundError(Exception):
    """Error que se produce cuando no se encuentra un dato buscado."""
    pass

class DataDoesntMatchError(Exception):
    """Error que se produce cuando los datos no coinciden."""
    pass