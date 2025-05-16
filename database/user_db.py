from typing import Optional, List, Dict
from database.security import Security
from database.db import DatabaseBase
import sqlite3

class UserDB(DatabaseBase):
    def add_user(self, username: str, password: str, user_type: str) -> int:
        try:
            if Security.check_password_strength(password) == 401:
                return 401
            if self.get_user(username=username):
                return 409
            hashed_pw = Security.hash_password(password)
            cursor = self.conn.cursor()
            cursor.execute(
                'INSERT INTO users (username, password, type) VALUES (?, ?, ?)',
                (username, hashed_pw, user_type)
            )
            self.conn.commit()
            return 201
        except sqlite3.Error as e:
            print(f"Error al añadir usuario: {e}")
            return 400

    def get_user(self, user_id: Optional[int] = None, username: Optional[str] = None) -> Optional[Dict]:
        cursor = self.conn.cursor()
        if user_id is not None:
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        elif username is not None:
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        else:
            return None
        user = cursor.fetchone()
        if user:
            return {'id': user[0], 'user': user[1], 'password': user[2], 'type': user[3]}
        return None

    def get_users(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users')
        return [{'id': row[0], 'user': row[1], 'password': row[2], 'type': row[3]} for row in cursor.fetchall()]

    def login(self, username: str, password: str) -> int:
        user = self.get_user(username=username)
        if not user:
            return 400
        if Security.check_password_strength(password) == 401:
            return 401
        if not Security.verify_password(password, user['password']):
            return 401
        return 200

    def add_personal_data(self, user_id: int, fecha: str, direccion: str, cp: str, ciudad: str, genero: str) -> int:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                '''INSERT INTO personal_data (id, fecha, direccion, cp, ciudad, genero) 
                VALUES (?, ?, ?, ?, ?, ?)''',
                (user_id, fecha, direccion, cp, ciudad, genero)
            )
            self.conn.commit()
            return 201
        except sqlite3.Error:
            return 400

    def get_personal_data(self, user_id: int) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM personal_data WHERE id = ?', (user_id,))
        data = cursor.fetchone()
        if data:
            return {
                'id': data[0],
                'fecha': data[1],
                'dir': data[2],
                'cp': data[3],
                'ciudad': data[4],
                'genero': data[5]
            }
        return None

    def get_data_field(self, user_id: int, field: str) -> Optional[str]:
        """Obtiene un campo específico de datos personales"""
        data = self.get_personal_data(user_id)
        if data:
            return data.get(field)
        return None

    def get_users_by_type(self, user_type: str) -> List[Dict]:
        """Filtra usuarios por tipo"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE type = ?', (user_type,))
        return [{'id': row[0], 'user': row[1], 'password': row[2], 'type': row[3]} for row in cursor.fetchall()]

    def get_users_by_city(self, city: str) -> List[Dict]:
        """Filtra usuarios por ciudad, devolviendo datos de usuario y personales."""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT u.id, u.username, u.type, pd.fecha, pd.direccion, pd.cp, pd.ciudad, pd.genero
            FROM users u
            JOIN personal_data pd ON u.id = pd.id
            WHERE pd.ciudad = ?
        ''', (city,))
        results = []
        for row in cursor.fetchall():
            results.append({
                'user': {'id': row[0], 'username': row[1], 'type': row[2]},
                'data': {'id': row[0], 'fecha': row[3], 'dir': row[4], 'cp': row[5], 'ciudad': row[6], 'genero': row[7]}
            })
        return results

    def is_admin(self, user_id: int) -> bool:
        """Comprueba si un usuario es admin"""
        user = self.get_user(user_id=user_id)
        return user is not None and user['type'] == 'admin'

    def delete_user(self, user_id: int) -> int:
        """Elimina un usuario y sus datos personales (gracias a ON DELETE CASCADE)"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            self.conn.commit()
            if cursor.rowcount == 0:
                return 404
            return 200
        except sqlite3.Error:
            return 400