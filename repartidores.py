
class Repartidor():
    """
    Clase que representa a un repartidor en el sistema de distribución de envíos.
    """

    def __init__(self, nombre, id, telefono, provincia, ubicacion_tiempo_real, vehiculo):
        """
        Inicializa un repartidor con la información básica.

        :param nombre: Nombre del repartidor
        :param id: Identificador único del repartidor
        :param telefono: Número de teléfono de contacto
        :param provincia: Provincia en la que opera
        :param ubicacion_tiempo_real: Ubicación en tiempo real
        :param vehiculo: Instancia de la clase Furgoneta asociada al repartidor
        """
        self.nombre = nombre
        self.id = id
        self.telefono = telefono
        self.provincia = provincia
        self.ubicacion_tiempo_real = ubicacion_tiempo_real
        self.vehiculo = vehiculo
        self.estado = "disponible"  # Puede ser "disponible", "en reparto", "descanso", "no disponible"
        self.envios_asignados = []

    def actualizar_ubicacion(self, nueva_ubicacion):
        """Actualizar la ubicación en tiempo real del repartidor."""
        self.ubicacion_tiempo_real = nueva_ubicacion

    def cambiar_estado(self, nuevo_estado):
        """Cambiar el estado del repartidor, verificando que sea válido."""
        estados_validos = ["disponible", "en reparto", "descanso", "no disponible"]
        if nuevo_estado in estados_validos:
            self.estado = nuevo_estado
        else:
            raise ValueError("Estado no válido")

    def asignar_envio(self, envio):
        """Asignar un envío al repartidor si está disponible."""
        if self.estado == "disponible":
            self.envios_asignados.append(envio)
            self.vehiculo.asignar_envio(envio)
            self.cambiar_estado("en reparto")
        else:
            print(f"El repartidor {self.nombre} no está disponible.")

    def finalizar_envio(self, envio):
        """Marcar un envío como completado y actualizar el estado del repartidor."""
        if envio in self.envios_asignados:
            self.envios_asignados.remove(envio)
            self.vehiculo.envios_asignados.remove(envio)
            if not self.envios_asignados:
                self.cambiar_estado("disponible")

    def obtener_estado(self):
        """Obtener el estado actual del repartidor."""
        return self.estado

    @staticmethod
    def distribuir_envios(repartidores, envios):
        """
        Distribuye los envíos entre los repartidores disponibles con furgoneta.

        :param repartidores: Lista de objetos Repartidor
        :param envios: Lista de envíos a asignar
        """
        repartidores_disponibles = []
        for r in repartidores:
            if r.estado == "disponible" and isinstance(r.vehiculo, Furgoneta):
                repartidores_disponibles.append(r)

        if not repartidores_disponibles:
            print("No hay repartidores con furgoneta disponibles en este momento.")
            return

        for i, envio in enumerate(envios):
            repartidor = repartidores_disponibles[i % len(repartidores_disponibles)]
            repartidor.asignar_envio(envio)
            print(f"Envío {envio} asignado a {repartidor.nombre} con furgoneta {repartidor.vehiculo.matricula}.")
