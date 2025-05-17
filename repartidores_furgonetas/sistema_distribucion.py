from typing import List, Dict, Optional
from furgonetas import Furgoneta
from repartidores import Repartidor

class SistemaDistribucion:
    """
    Clase que representa el sistema de gestión de repartidores y furgonetas.
    """

    def __init__(self):
        self.repartidores: Dict[int, Repartidor] = {}
        self.furgonetas: Dict[str, Furgoneta] = {}

    def add_furgoneta(self, matricula: str, capacidad_maxima: float, provincia: str, conductor: Repartidor) -> None:
        """
        Añade una nueva furgoneta al sistema.

        Parámetros
        ----------
        matricula : str
            Matrícula única del vehículo.
        capacidad_maxima : float
            Capacidad máxima de carga.
        provincia : str
            Provincia en la que opera.
        conductor : Repartidor
            Conductor asignado.
        """
        if matricula not in self.furgonetas:
            self.furgonetas[matricula] = Furgoneta(matricula, conductor, capacidad_maxima, provincia)
            conductor.vehiculo = self.furgonetas[matricula]
        else:
            print(f"La furgoneta con matrícula {matricula} ya existe.")

    def delete_furgoneta(self, matricula: str) -> None:
        """
        Elimina una furgoneta del sistema.

        Parámetros
        ----------
        matricula : str
            Matrícula del vehículo a eliminar.
        """
        if matricula in self.furgonetas:
            del self.furgonetas[matricula]
        else:
            print(f"No se encontró la furgoneta con matrícula {matricula}.")

    def asignar_conductor_furgoneta(self, matricula: str, conductor_id: int) -> None:
        """
        Asigna un conductor a una furgoneta existente.

        Parámetros
        ----------
        matricula : str
            Matrícula de la furgoneta.
        conductor_id : int
            ID del repartidor a asignar.
        """
        furgoneta = self.furgonetas.get(matricula)
        conductor = self.repartidores.get(conductor_id)
        if furgoneta and conductor:
            furgoneta.conductor = conductor
            conductor.vehiculo = furgoneta
        else:
            print("Furgoneta o repartidor no encontrados.")

    def get_furgonetas(self) -> List[Furgoneta]:
        """
        Devuelve todas las furgonetas registradas.

        Returns
        -------
        list
            Lista de objetos Furgoneta.
        """
        return list(self.furgonetas.values())

    def add_repartidor(self, nombre: str, telefono: str, provincia: str, vehiculo: Optional[Furgoneta]) -> None:
        """
        Agrega un nuevo repartidor al sistema.

        Parámetros
        ----------
        nombre : str
            Nombre del repartidor.
        telefono : str
            Teléfono de contacto.
        provincia : str
            Provincia de operación.
        vehiculo : Furgoneta or None
            Furgoneta asignada, si aplica.
        """
        nuevo_id = max(self.repartidores.keys(), default=0) + 1
        repartidor = Repartidor(nombre, nuevo_id, telefono, provincia, "", vehiculo)
        self.repartidores[nuevo_id] = repartidor
        if vehiculo:
            vehiculo.conductor = repartidor

    def delete_repartidor(self, repartidor_id: int) -> None:
        """
        Elimina un repartidor del sistema.

        Parámetros
        ----------
        repartidor_id : int
            ID del repartidor.
        """
        if repartidor_id in self.repartidores:
            del self.repartidores[repartidor_id]
        else:
            print(f"No existe repartidor con ID {repartidor_id}.")

    def update_ubicacion_repartidor(self, repartidor_id: int, ubicacion: str) -> None:
        """
        Actualiza la ubicación de un repartidor.

        Parámetros
        ----------
        repartidor_id : int
            ID del repartidor.
        ubicacion : str
            Nueva ubicación.
        """
        repartidor = self.repartidores.get(repartidor_id)
        if repartidor:
            repartidor.actualizar_ubicacion(ubicacion)
        else:
            print(f"No existe repartidor con ID {repartidor_id}.")

    def get_repartidores(self) -> List[Repartidor]:
        """
        Devuelve todos los repartidores registrados.

        Returns
        -------
        list
            Lista de objetos Repartidor.
        """
        return list(self.repartidores.values())
