class Furgoneta:
    """
    Clase que representa una furgoneta utilizada para el reparto de envíos.
    """

    def __init__(self, matricula, capacidad_maxima, provincia):
        """
        Inicializa una furgoneta con sus características principales.

        :param matricula: Matrícula del vehículo
        :param capacidad_maxima: Capacidad máxima de carga en kg
        :param provincia: Provincia en la que opera
        """
        self.matricula = matricula
        self.capacidad_maxima = capacidad_maxima
        self.provincia = provincia
        self.envios_asignados = []

    def asignar_envio(self, envio):
        """Asigna un envío a la furgoneta si tiene capacidad disponible."""
        self.envios_asignados.append(envio)

    def obtener_envios(self):
        """Devuelve la lista de envíos asignados a la furgoneta."""
        return self.envios_asignados
