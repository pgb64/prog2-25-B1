from typing import List, Dict, Optional, Any
from database.db import DatabaseBase, DB_NAME  # Eliminada la importación de DatabaseError

class PaqueteDB(DatabaseBase):
    """
    Clase para manejar las operaciones de base de datos de paquetes.
    
    Usa métodos genéricos de DatabaseBase:
    - insert("paquetes", {...}) para añadir paquetes
    - get("paquetes") para obtener todos los paquetes
    - get("paquetes", {"codigo_paquete": codigo}, fetch_all=False) para buscar por código
    - delete("paquetes", {"codigo_paquete": codigo}) para eliminar paquetes
    """
    
    def __init__(self, db_name=DB_NAME):  # Usamos DB_NAME como valor por defecto
        super().__init__(db_name)

    def get_paquetes(self):
        """Obtiene todos los paquetes"""
        return self.get("paquetes")

    def get_paquete_by_codigo(self, codigo_paquete: str):
        """Busca un paquete por su código"""
        return self.get("paquetes", {"codigo_paquete": codigo_paquete}, fetch_all=False)

    def get_codigos_paquetes(self):
        """Obtiene los códigos de todos los paquetes."""
        try:
            resultado = self.execute_query("SELECT codigo_paquete FROM paquetes")
            if isinstance(resultado, tuple) and resultado[0] is None:
                return []
            
            cursor = resultado
            rows = cursor.fetchall()
            return [row['codigo_paquete'] for row in rows]
        except Exception:
            return []

    def delete_paquete(self, codigo_paquete: str):
        """Elimina un paquete del sistema"""
        return self.delete("paquetes", {"codigo_paquete": codigo_paquete})