from typing import Optional, List, Dict
from database.db import DatabaseBase
import sqlite3

class FurgonetaDB(DatabaseBase):
    def add_furgoneta(self, matricula: str, capacidad_maxima: int, provincia: str, conductor_id: Optional[int] = None) -> int:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                '''INSERT INTO furgonetas (matricula, capacidad_maxima, provincia, conductor_id) 
                VALUES (?, ?, ?, ?)''',
                (matricula, capacidad_maxima, provincia, conductor_id)
            )
            self.conn.commit()
            return 201
        except sqlite3.IntegrityError:
            return 409
        except sqlite3.Error:
            return 400

    def get_furgonetas(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM furgonetas')
        return [
            {
                'matricula': row[0],
                'capacidad_maxima': row[1],
                'provincia': row[2],
                'envios_asignados': row[3],
                'conductor_id': row[4]
            } for row in cursor.fetchall()
        ]

    def get_furgoneta_by_matricula(self, matricula: str) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM furgonetas WHERE matricula = ?', (matricula,))
        row = cursor.fetchone()
        if row:
            return {
                'matricula': row[0],
                'capacidad_maxima': row[1],
                'provincia': row[2],
                'envios_asignados': row[3],
                'conductor_id': row[4]
            }
        return None

    def asignar_conductor_furgoneta(self, matricula: str, conductor_id: Optional[int]) -> int:
        """Asigna conductor a furgoneta"""
        try:
            if not self.get_furgoneta_by_matricula(matricula):
                return 404 
            cursor = self.conn.cursor()
            cursor.execute(
                'UPDATE furgonetas SET conductor_id = ? WHERE matricula = ?',
                (conductor_id, matricula)
            )
            self.conn.commit()
            return 200
        except sqlite3.Error:
            return 400

    def delete_furgoneta(self, matricula: str) -> int:
        """Elimina una furgoneta del sistema"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM furgonetas WHERE matricula = ?', (matricula,))
            self.conn.commit()
            if cursor.rowcount == 0:
                return 404
            return 200
        except sqlite3.Error:
            return 400