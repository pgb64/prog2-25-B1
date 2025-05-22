from typing import Optional, List, Dict, Any
from security import Security
from database.db import DatabaseBase, DB_NAME, AlreadyExistsError, DataNotFoundError, DataDoesntMatchError

class UserDB(DatabaseBase):
    """
    Gestiona usuarios en la base de datos.

    Esta clase implementa operaciones para crear, leer, actualizar y eliminar
    usuarios en el sistema, asi como gestionar sus datos personales.

    Atributos
    ---------
    Hereda todos los atributos de DatabaseBase.
    """

    def __init__(self, db_name=DB_NAME):
        """
        Inicializa la clase UserDB.

        Parameters
        ----------
        db_name : str, optional
            Ruta del archivo de base de datos (por defecto es DB_NAME)
        """
        super().__init__(db_name)
        self.add("users", "users_by_city", """
            SELECT u.id, u.user, u.admin, pd.fecha, pd.dir, pd.cp, pd.ciudad, pd.genero
            FROM users u
            JOIN personal_data pd ON u.id = pd.id
            WHERE pd.ciudad = ?
        """)

    def add_user(self, username: str, password: str, is_admin: bool):
        """
        Registra un nuevo usuario en el sistema.

        Verifica primero si el usuario ya existe y, si no, crea una nueva entrada
        en la tabla users con la informacion proporcionada.

        Parameters
        ----------
        username : str
            Nombre o email del usuario (debe ser unico)
        password : str
            Contraseña del usuario (se espera ya hasheada)
        is_admin : bool
            Indica si el usuario tiene privilegios de administrador

        Returns
        -------
        int
            Codigo de resultado de la operacion

        Raises
        ------
        AlreadyExistsError
            Si ya existe un usuario con el mismo nombre
        """
        existing_user = self.get("users", {"user": username}, fetch_all=False)
        if existing_user:
            raise AlreadyExistsError('Este usuario ya existe')

        return self.insert("users", {
            "user": username,
            "password": password, #no es necesario que password sea hasheado porque la API ya pasa un hash como parámetro
            "admin": is_admin
        })

    def get_user(self, user_id: Optional[int] = None, username: Optional[str] = None):
        """
        Busca un usuario por su ID o nombre.

        Permite buscar un usuario ya sea por su ID numerico o por su
        nombre de usuario, devolviendo sus datos si se encuentra.

        Parameters
        ----------
        user_id : int, optional
            ID numerico del usuario a buscar
        username : str, optional
            Nombre del usuario a buscar

        Returns
        -------
        dict or None
            Diccionario con los datos del usuario si existe, None en caso contrario

        Notes
        -----
        Se debe proporcionar al menos uno de los parametros de busqueda.
        """
        conditions = {}
        if user_id is not None:
            conditions["id"] = user_id
        elif username is not None:
            conditions["user"] = username
        else:
            return None

        user_data = self.get("users", conditions, fetch_all=False)
        if user_data:
            return {
                'id': user_data['id'],
                'user': user_data['user'],
                'password': user_data['password'],
                'admin': user_data['admin']
            }
        return None

    def get_users(self):
        """
        Recupera todos los usuarios registrados.

        Obtiene una lista completa de los usuarios almacenados en la
        base de datos con todos sus datos (excepto datos personales).

        Returns
        -------
        list
            Lista de diccionarios, cada uno con la informacion de un usuario
        """
        users = self.get("users")
        return [{'id': u['id'], 'user': u['user'], 'password': u['password'], 'admin': u['admin']} for u in users]

    def add_personal_data(self, user_id: int, fecha: str, direccion: str, cp: str, ciudad: str, genero: str):
        """
        Agrega datos personales para un usuario existente.

        Los datos personales se almacenan en una tabla separada vinculada
        al usuario mediante su ID.

        Parameters
        ----------
        user_id : int
            ID del usuario al que pertenecen los datos
        fecha : str
            Fecha de nacimiento
        direccion : str
            Direccion postal completa
        cp : str
            Codigo postal
        ciudad : str
            Ciudad de residencia
        genero : str
            Genero del usuario

        Returns
        -------
        int
            Codigo de resultado de la operacion

        Notes
        -----
        Si el usuario ya tiene datos personales, este metodo podria causar un error.
        """
        return self.insert("personal_data", {
            "id": user_id,
            "fecha": fecha,
            "dir": direccion,
            "cp": cp,
            "ciudad": ciudad,
            "genero": genero
        })

    def get_personal_data(self, user_id: int):
        """
        Obtiene los datos personales de un usuario especifico.

        Busca en la tabla personal_data los datos asociados al ID de usuario.

        Parameters
        ----------
        user_id : int
            ID del usuario cuyos datos se quieren obtener

        Returns
        -------
        dict or None
            Diccionario con los datos personales si existen, None en caso contrario
        """
        data = self.get("personal_data", {"id": user_id}, fetch_all=False)
        if data:
            return {
                'id': data['id'],
                'fecha': data['fecha'],
                'dir': data['dir'],
                'cp': data['cp'],
                'ciudad': data['ciudad'],
                'genero': data['genero']
            }
        return None

    def get_data_field(self, user_id: int, field: str):
        """
        Obtiene un campo especifico de los datos personales.

        Util para recuperar solo un campo concreto como la ciudad o el CP.

        Parameters
        ----------
        user_id : int
            ID del usuario
        field : str
            Nombre del campo a recuperar

        Returns
        -------
        Any
            Valor del campo solicitado o None si no existe
        """
        data = self.get_personal_data(user_id)
        return data.get(field) if data else None

    def get_users_by_type(self, user_type: bool):
        """
        Filtra usuarios segun su tipo (admin o normal).

        Parameters
        ----------
        user_type : bool
            True para administradores, False para usuarios normales

        Returns
        -------
        list
            Lista de usuarios que coinciden con el tipo especificado
        """
        users = self.get("users", {"admin": user_type})
        return [{'id': u['id'], 'user': u['user'], 'password': u['password'], 'admin': u['admin']} for u in users]

    def get_users_by_city(self, city: str):
        """
        Busca usuarios que viven en una ciudad determinada

        Utiliza una consulta personalizada para unir las tablas users y personal_data
        y filtrar por ciudad.

        Parameters
        ----------
        city : str
            Nombre de la ciudad para filtrar

        Returns
        -------
        list
            Lista de usuarios con sus datos personales que viven en la ciudad especificada
        """
        rows = self.execute_custom_query("users", "users_by_city", (city,))
        return [{
            'user': {'id': r['id'], 'user': r['user'], 'admin': r['admin']},
            'data': {'id': r['id'], 'fecha': r['fecha'], 'dir': r['dir'],
                    'cp': r['cp'], 'ciudad': r['ciudad'], 'genero': r['genero']}} for r in rows]

    def is_admin(self, email: int):
        """
        Verifica si un usuario tiene privilegios de administrador.

        Parameters
        ----------
        user_id : int
            ID del usuario a verificar

        Returns
        -------
        bool
            True si el usuario es administrador, False en caso contrario
        """
        user = self.get_user(username=email)
        return user is not None and user['admin'] == True

    def delete_user(self, user_id: int):
        """
        Elimina un usuario y sus datos asociados de la base de datos.

        Debido a la restriccion CASCADE en la tabla personal_data, al eliminar
        un usuario tambien se eliminaran sus datos personales automaticamente.

        Parameters
        ----------
        user_id : int
            ID del usuario a eliminar

        Returns
        -------
        int
            Codigo de resultado de la operacion

        Raises
        ------
        DataNotFoundError
            Si el usuario no existe
        """
        return self.delete("users", {"id": user_id})