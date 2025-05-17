from typing import Optional, List, Dict, Any
from database.db import DatabaseBase, DB_NAME

class FurgonetaDB(DatabaseBase):
    """
    Clase para manejar las operaciones de base de datos de furgonetas.
    
    Usa métodos genéricos de DatabaseBase:
    - insert("furgonetas", {...}) para añadir
    - get("furgonetas") para obtener todas
    - get("furgonetas", {"matricula": matricula}, fetch_all=False) para buscar por matrícula
    - delete("furgonetas", {"matricula": matricula}) para eliminar
    """
    
    def __init__(self, db_name=DB_NAME):
        super().__init__(db_name)

    def asignar_conductor_furgoneta(self, matricula: str, conductor_id: Optional[int]):
        """
        Asigna un conductor a una furgoneta.
        Este método añade la lógica de verificación de existencia.
        """
        if not self.get("furgonetas", {"matricula": matricula}, fetch_all=False):
            return 404
        return self.update("furgonetas", {"conductor": conductor_id}, {"matricula": matricula})