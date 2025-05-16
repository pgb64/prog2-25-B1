from typing import List, Dict, Optional
from database.db import DatabaseBase
import sqlite3

class PaqueteDB(DatabaseBase):
    def add_paquete(self, codigo_paquete: str, direccion: str, usuario_id: int, contenido: str) -> int:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                '''INSERT INTO paquetes (codigo_paquete, direccion, usuario_id, contenido) 
                VALUES (?, ?, ?, ?)''',
                (codigo_paquete, direccion, usuario_id, contenido)
            )
            self.conn.commit()
            return 201
        except sqlite3.IntegrityError:
            return 409
        except sqlite3.Error:
            return 400

    def get_paquetes(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM paquetes')
        return [
            {
                'codigo_paquete': row[0],
                'direccion': row[1],
                'usuario_id': row[2],
                'contenido': row[3]
            } for row in cursor.fetchall()
        ]

    def get_paquete_by_codigo(self, codigo_paquete: str) -> Optional[Dict]:
        """Busca un paquete por su código"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM paquetes WHERE codigo_paquete = ?', (codigo_paquete,))
        row = cursor.fetchone()
        if row:
            return {
                'codigo_paquete': row[0],
                'direccion': row[1],
                'usuario_id': row[2],
                'contenido': row[3]
            }
        return None

    def get_codigos_paquetes(self) -> List[str]:
        """Obtiene los códigos de todos los paquetes"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT codigo_paquete FROM paquetes')
        return [row[0] for row in cursor.fetchall()]

    def delete_paquete(self, codigo_paquete: str) -> int:
        """Elimina un paquete del sistema"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM paquetes WHERE codigo_paquete = ?', (codigo_paquete,))
            self.conn.commit()
            if cursor.rowcount == 0:
                return 404
            return 200
        except sqlite3.Error:
            return 400