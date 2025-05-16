from typing import List, Dict, Optional
from database.db import DatabaseBase
import sqlite3

class RepartidorDB(DatabaseBase):
    def add_repartidor(self, nombre: str, telefono: str, provincia: str, vehiculo: str) -> int:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                '''INSERT INTO repartidores (nombre, telefono, provincia, vehiculo) 
                VALUES (?, ?, ?, ?)''',
                (nombre, telefono, provincia, vehiculo)
            )
            self.conn.commit()
            return 201
        except sqlite3.Error:
            return 400

    def get_repartidores(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM repartidores')
        return [
            {
                'id': row[0],
                'nombre': row[1],
                'telefono': row[2],
                'provincia': row[3],
                'ubicacion_tiempo_real': row[4],
                'vehiculo': row[5],
                'estado': row[6],
                'envios_asignados': row[7]
            } for row in cursor.fetchall()
        ]

    def get_repartidor_by_id(self, repartidor_id: int) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM repartidores WHERE id = ?', (repartidor_id,))
        row = cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'nombre': row[1],
                'telefono': row[2],
                'provincia': row[3],
                'ubicacion_tiempo_real': row[4],
                'vehiculo': row[5],
                'estado': row[6],
                'envios_asignados': row[7]
            }
        return None
        
    def update_ubicacion_repartidor(self, repartidor_id: int, ubicacion: str) -> int:
        """Actualiza ubicación de repartidor"""
        try:
            if not self.get_repartidor_by_id(repartidor_id):
                return 404
            cursor = self.conn.cursor()
            cursor.execute(
                'UPDATE repartidores SET ubicacion_tiempo_real = ? WHERE id = ?',
                (ubicacion, repartidor_id)
            )
            self.conn.commit()
            if cursor.rowcount == 0:
                return 404
            return 200
        except sqlite3.Error:
            return 400

    def delete_repartidor(self, repartidor_id: int) -> int:
        """Elimina un repartidor del sistema"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM repartidores WHERE id = ?', (repartidor_id,))
            self.conn.commit()
            if cursor.rowcount == 0:
                return 404
            return 200
        except sqlite3.Error:
            return 400