from typing import Optional, List, Dict
from database.db import DatabaseBase
import sqlite3

class ArticuloDB(DatabaseBase):
    def add_articulo(self, nombre: str, codigo: str, cantidad: int, proveedor: str, descripcion: str) -> int:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                '''INSERT INTO articulos (nombre, codigo, cantidad, proveedor, descripcion) 
                VALUES (?, ?, ?, ?, ?)''', #Los signos de interrogacion son marcadores de posicion
                # y se reemplazan luego por los valores de la tupla de abajo en orden que aparecen, es pr seguridad
                (nombre, codigo, cantidad, proveedor, descripcion)
            )
            self.conn.commit()
            return 201
        except sqlite3.IntegrityError:
            return 409
        except sqlite3.Error:
            return 400

    def get_articulos(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM articulos')
        return [
            {
                'nombre': row[0],
                'codigo': row[1],
                'cantidad': row[2],
                'proveedor': row[3],
                'descripcion': row[4]
            } for row in cursor.fetchall()
        ]

    def get_articulo_by_codigo(self, codigo: str) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM articulos WHERE codigo = ?', (codigo,))
        row = cursor.fetchone()
        if row:
            return {
                'nombre': row[0],
                'codigo': row[1],
                'cantidad': row[2],
                'proveedor': row[3],
                'descripcion': row[4]
            }
        return None

    def get_codigos_articulos(self) -> List[str]:
        """Obtiene los códigos de todos los artículos"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT codigo FROM articulos')
        return [row[0] for row in cursor.fetchall()]

    def delete_articulo(self, codigo: str) -> int:
        """Elimina un artículo del inventario"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM articulos WHERE codigo = ?', (codigo,))
            self.conn.commit()
            if cursor.rowcount == 0:
                return 404
            return 200
        except sqlite3.Error:
            return 400