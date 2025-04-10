class Furgoneta:
    """
    Clase que representa una furgoneta utilizada para el reparto de envíos.

    Atributos
    ----------
    matricula : str
        Matrícula del vehículo.
    conductor : Repartidor
        Repartidor que conduce la furgoneta.
    capacidad_maxima : float
        Capacidad máxima de carga en kilogramos.
    provincia : str
        Provincia en la que opera la furgoneta.
    envios_asignados : list
        Lista de envíos asignados a esta furgoneta.

    Métodos
    -------
    asignar_envio(envio) -> None
        Asigna un envío a la furgoneta.
    
    obtener_envios() -> List
        Devuelve la lista de envíos asignados.
    """

    def __init__(self, matricula, conductor, capacidad_maxima, provincia):
        """
        Inicializa una furgoneta con sus características principales.

        Parámetros
        ----------
        matricula : str
            Matrícula del vehículo.
        conductor : Repartidor
            Repartidor que conduce la furgoneta.
        capacidad_maxima : float
            Capacidad máxima de carga en kilogramos.
        provincia : str
            Provincia en la que opera.
        """
        self.matricula = matricula
        self.capacidad_maxima = capacidad_maxima
        self.provincia = provincia
        self.envios_asignados = []
        self.conductor = conductor

    def asignar_envio(self, envio):
        """
        Asigna un envío a la furgoneta.

        Parámetros
        ----------
        envio : object
            El envío a asignar a la furgoneta.
        """
        self.envios_asignados.append(envio)

    def obtener_envios(self):
        """
        Devuelve la lista de envíos asignados a la furgoneta.

        Returns
        -------
        list
            Lista de envíos asignados.
        """
        return self.envios_asignados
