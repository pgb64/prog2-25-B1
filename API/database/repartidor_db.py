from typing import List, Dict, Optional, Any
from database.db import DatabaseBase, DB_NAME

class RepartidorDB(DatabaseBase):
    """
    Clase para manejar las operaciones de base de datos de repartidores.
    
    Usa métodos genéricos de DatabaseBase:
    - insert("repartidores", {...}) para añadir repartidores
    - get("repartidores") para obtener todos los repartidores
    - get("repartidores", {"id": repartidor_id}, fetch_all=False) para buscar por ID
    - delete("repartidores", {"id": repartidor_id}) para eliminar repartidores
    """    
    def __init__(self, db_name=DB_NAME):
        super().__init__(db_name)

    def update_ubicacion_repartidor(self, repartidor_id: int, ubicacion: str):
        """
        Actualiza la ubicación de un repartidor.
        Este método añade la lógica de verificación de existencia.
        """
        if not self.get("repartidores", {"id": repartidor_id}, fetch_all=False):
            return 404
        return self.update("repartidores", {"ubicacion_tiempo_real": ubicacion}, {"id": repartidor_id})