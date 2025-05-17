from typing import Optional, List, Dict, Any
from database.db import DatabaseBase, DB_NAME

class ArticuloDB(DatabaseBase):
    """
    Clase para manejar las operaciones de base de datos de artículos.
    
    Usa métodos genéricos de DatabaseBase:
    - insert("articulos", {...}) para añadir artículos
    - get("articulos") para obtener todos los artículos
    - get("articulos", {"codigo": codigo}, fetch_all=False) para buscar por código
    - delete("articulos", {"codigo": codigo}) para eliminar artículos
    """
    
    def __init__(self, db_name=DB_NAME):
        super().__init__(db_name)
    
    def get_codigos_articulos(self):
        """Obtiene los códigos de todos los artículos."""
        try:
            resultado = self.execute_query("SELECT codigo FROM articulos")
            if isinstance(resultado, tuple) and resultado[0] is None:
                return []
            
            cursor = resultado
            rows = cursor.fetchall()
            return [row['codigo'] for row in rows]
        except Exception:
            return []
