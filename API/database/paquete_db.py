from typing import List, Dict, Any
from database.db import DatabaseBase, DB_NAME, DataNotFoundError

class PaqueteDB(DatabaseBase):
    """
    Gestiona la informacion de paquetes en la base de datos.
    
    Incluye metodos para registro, busqueda y seguimento de paquetes.
    """
    
    def __init__(self, db_name: str = DB_NAME):
        """
        Inicializa la clase PaqueteDB.
        
        Parameters
        ----------
        db_name : str, optional
            Ruta de la base de datos (por defecto es DB_NAME)
        """
        super().__init__(db_name)

    def get_paquetes(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los paquetes del sistema.
        
        Returns
        -------
        List[Dict[str, Any]]
            Lista con todos los paquetes
        """
        return self.get("paquetes")

    def get_paquete_by_codigo(self, codigo_paquete: str) -> Dict[str, Any]:
        """
        Busca un paquete por su codigo unico.
        
        Parameters
        ----------
        codigo_paquete : str
            Codigo del paquete a buscar
        
        Returns
        -------
        Dict[str, Any]
            Datos del paquete o diccionario vacio si no se encuentra
        """
        return self.get("paquetes", {"codigo_paquete": codigo_paquete}, fetch_all=False)

    def get_codigos_paquetes(self) -> List[str]:
        """
        Obtiene la lista de todos los codigos de paquete.
        
        Returns
        -------
        List[str]
            Lista con los codigos de paquetes
        """
        try:
            resultado = self.execute_query("SELECT codigo_paquete FROM paquetes")
            if isinstance(resultado, tuple) and resultado[0] is None:
                return []
            
            cursor = resultado
            rows = cursor.fetchall()
            return [row['codigo_paquete'] for row in rows]
        except Exception:
            return []

    def delete_paquete(self, codigo_paquete: str) -> int:
        """
        Elimina un paquete del sistema.
        
        Parameters
        ----------
        codigo_paquete : str
            Codigo del paquete a eliminar
        
        Returns
        -------
        int
            Codigo de resultado
        
        Raises
        ------
        DataNotFoundError
            Si no se encuentra el paquete
        """
        return self.delete("paquetes", {"codigo_paquete": codigo_paquete})