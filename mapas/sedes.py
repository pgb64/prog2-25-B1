import pickle

class Sede:

    @staticmethod
    def convertir_coords(coord):
        lat_str, lon_str = coord.strip("() ").split(",")
        return (float(lat_str), float(lon_str))

    def __init__(self, nombre, provincia, coords):
        self.nombre = nombre
        self.provincia = provincia
        self.coords = self.convertir_coords(coords)

    def __str__(self):
        return (f"\nInformación de la sede\n"
                "--------------------------\n"
                f"- Nombre: {self.nombre} \n"
                f"- Provincia: {self.provincia} \n"
                f"- Coordenadas: {self.coords}")

    def __repr__(self):
        return f"{self.nombre} ({self.provincia}) --> {self.coords}"

def guardar_sedes_pickle(sedes, archivo):
    with open(archivo, "wb") as f:
        pickle.dump(sedes, f)

def cargar_sedes_pickle(archivo):
    with open(archivo, "rb") as f:
        return pickle.load(f)

