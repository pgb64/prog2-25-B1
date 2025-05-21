from typing import Optional, List, Dict, Any
from security import Security 
from database.db import DatabaseBase, DB_NAME, AlreadyExistsError, DataNotFoundError, DataDoesntMatchError

class UserDB(DatabaseBase):
    def __init__(self, db_name=DB_NAME):
        super().__init__(db_name)
        self.add("users", "users_by_city", """
            SELECT u.id, u.user, u.admin, pd.fecha, pd.dir, pd.cp, pd.ciudad, pd.genero
            FROM users u
            JOIN personal_data pd ON u.id = pd.id
            WHERE pd.ciudad = ?
        """)

    def add_user(self, username: str, password: str, is_admin: bool):
        """Añade un nuevo usuario a la base de datos"""
                
        existing_user = self.get("users", {"user": username}, fetch_all=False)
        if existing_user:
            raise AlreadyExistsError('Este usuario ya existe')
                
        return self.insert("users", {
            "user": username,
            "password": password, #no es necesario que password sea hasheado porque la API ya pasa un hash como parámetro
            "admin": is_admin
        })

    def get_user(self, user_id: Optional[int] = None, username: Optional[str] = None):
        """Obtiene un usuario por ID o username"""
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
        """Obtiene todos los usuarios"""
        users = self.get("users")
        return [{'id': u['id'], 'user': u['user'], 'password': u['password'], 'admin': u['admin']} for u in users]

    def add_personal_data(self, user_id: int, fecha: str, direccion: str, cp: str, ciudad: str, genero: str):
        """Añade datos personales a un usuario"""
        return self.insert("personal_data", {
            "id": user_id,
            "fecha": fecha,
            "dir": direccion,
            "cp": cp,
            "ciudad": ciudad,
            "genero": genero
        })

    def get_personal_data(self, user_id: int):
        """Obtiene datos personales de un usuario"""
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
        """Obtiene un campo específico de datos personales"""
        data = self.get_personal_data(user_id)
        return data.get(field) if data else None

    def get_users_by_type(self, user_type: bool):
        """Filtra usuarios por tipo"""
        users = self.get("users", {"admin": user_type})
        return [{'id': u['id'], 'user': u['user'], 'password': u['password'], 'admin': u['admin']} for u in users]

    def get_users_by_city(self, city: str):
        """Filtra usuarios por ciudad usando consulta personalizada"""
        rows = self.execute_custom_query("users", "users_by_city", (city,))
        return [{
            'user': {'id': r['id'], 'user': r['user'], 'admin': r['admin']},
            'data': {'id': r['id'], 'fecha': r['fecha'], 'dir': r['dir'],
                    'cp': r['cp'], 'ciudad': r['ciudad'], 'genero': r['genero']}} for r in rows]

    def is_admin(self, user_id: int):
        """Comprueba si un usuario es admin"""
        user = self.get_user(user_id=user_id)
        return user is not None and user['admin'] == True

    def delete_user(self, user_id: int):
        """Elimina un usuario y sus datos personales"""
        return self.delete("users", {"id": user_id})