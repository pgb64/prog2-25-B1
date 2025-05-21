import pandas as pd
import pickle as pkl
import os
import csv

class Sede:
    # Atributos de clase
    sedes = []
    _csv_path = "mapas/sedes.csv"       # Archivo csv
    _pkl_mod = "mapas/sedes_copia.pkl"    # Archivo pickle


    def __init__(self, nombre : str, provincia : str, coords : str):
        '''
        Inicializa una sede con nombre, provincia y coordenadas.
        Parámetros:
        -----------
        nombre : str
            Nombre de la sede.
        provincia : str
            Provincia de la sede.
        coords : str
            Coordenadas de la sede en formato "(lat, lon)".
        '''
        self.nombre = nombre
        self.provincia = provincia
        self.coords = self.convertir_coords(coords)


    @staticmethod
    def convertir_coords(coord : str) -> tuple:
        '''
        Convierte una cadena de coordenadas en formato "(lat, lon)"
        a una tupla de floats (lat, lon).

        Parámetros:
        -----------
        coord : str
            Cadena de coordenadas en formato "(lat, lon)".
        
        Return:
        -------
        tuple
            Tupla de floats (lat, lon).
        '''
        lat, lon = coord.strip("() ").split(",")
        return (float(lat), float(lon))

    def __str__(self) -> str:
        """Devuelve una representación en cadena de la sede."""
        return (f"\nInformación de la sede\n"
                "--------------------------\n"
                f"- Nombre: {self.nombre} \n"
                f"- Provincia: {self.provincia} \n"
                f"- Coordenadas: {self.coords}")

    def __repr__(self) -> str:
        """Devuelve la información esencial de la sede."""
        return f"{self.nombre} ({self.provincia}) --> {self.coords}"

    @classmethod
    def cargar_csv(cls) -> None:
        """Carga todas las sedes desde el CSV a la lista en la clase."""
        # Comprobar si el archivo csv existe
        if not os.path.exists(cls._csv_path):
            print(f"Archivo CSV '{cls._csv_path}' no encontrado.")
            cls.sedes = []
            return False
        df = pd.read_csv(cls._csv_path)
        # Añadir sedes a la lista
        cls.sedes = [cls(row['nombre'], row['provincia'], row['coords']) for _, row in df.iterrows()]
        return True

    @classmethod
    def _guardar_csv(cls) -> None:
        """Guarda la lista de sedes actualizada en el archivo CSV."""
        with open(cls._csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["provincia", "nombre", "coords"])
            for sede in cls.sedes:
                coords_str = f"({sede.coords[0]}, {sede.coords[1]})"
                writer.writerow([sede.provincia, sede.nombre, coords_str])

    @classmethod
    def guardar_pickle(cls) -> None:
        """Guarda la lista en pickle como copia rápida."""
        with open(cls._pkl_mod, "wb") as f:
            pkl.dump(cls.sedes, f)

    @classmethod
    def agregar_sede(cls, nombre : str, provincia : str, coords : str) -> None:
        """Añade sede modificando el csv y actualiza memoria y pickle."""
        # Carga csv actual
        cls.cargar_csv()

        # Comprobar si la sede ya existe
        for sede in cls.sedes:
            if sede.nombre == nombre and sede.provincia == provincia:
                print("La sede ya existe.")
                return False
            
        # Añadir en memoria
        nueva_sede = cls(nombre, provincia, coords)
        cls.sedes.append(nueva_sede)
        # Guardar en csv
        cls._guardar_csv()
        # Guardar en pickle
        cls.guardar_pickle()
        print(f"Sede añadida: {nueva_sede}")
        return True

    @classmethod
    def quitar_sede(cls, nombre : str, provincia : str) -> None:
        """Elimina sede modificando el csv y actualiza memoria y pickle."""
        cls.cargar_csv()
        inicial_len = len(cls.sedes)
        cls.sedes = [s for s in cls.sedes if not (s.nombre == nombre and s.provincia == provincia)]
        if len(cls.sedes) == inicial_len:
            print("No se encontró la sede para eliminar.")
            return False
        # Guardar csv actualizado
        cls._guardar_csv()
        # Guardar en pickle
        cls.guardar_pickle()
        print(f"Sede eliminada: {nombre} ({provincia})")
        return True

    @classmethod
    def mostrar_sedes(cls) -> str:
        """Devuelve un texto con la información de todas las sedes."""
        if not cls.sedes:
            return "No hay sedes cargadas."
        info = ""
        for sede in cls.sedes:
            info += str(sede) + "\n"
        return info

    @classmethod
    def info_sedes(cls)-> list[tuple]:
        '''
        Devuelve una lista de tuplas con el nombre y las coordenadas de cada sede.
        Return:
        -------
        list[tuple]
            Lista de tuplas con el nombre y las coordenadas de cada sede.
        '''
        return [(sede.nombre, sede.coords) for sede in cls.sedes]
    
    @classmethod
    def sede_coord(cls, sede : str) -> tuple:
        '''
        Devuelve las coordenadas de una sede dada.
        Parámetros:
        -----------
        sede : str
            Nombre de la sede.
        
        Return:
        -------
        tuple
            Coordenadas de la sede en formato (lat, lon).
        '''
        for s in cls.sedes:
            if s.nombre == sede:
                return s.coords
        return None
    

if __name__ == "__main__":
    # Probar el pkl
    Sede.cargar_csv()
    Sede.guardar_pickle()