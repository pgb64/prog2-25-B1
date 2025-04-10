
class Repartidor():
    """
    Clase que representa a un repartidor en el sistema de distribución de envíos.

    Atributos
    ----------
    nombre : str
        Nombre del repartidor.
    id : int
        Identificador único del repartidor.
    telefono : str
        Número de teléfono de contacto.
    provincia : str
        Provincia en la que opera.
    ubicacion_tiempo_real : str
        Ubicación actual del repartidor.
    vehiculo : Furgoneta
        Vehículo asociado al repartidor.
    estado : str
        Estado actual del repartidor ('disponible', 'en reparto', 'descanso', 'no disponible').
    envios_asignados : list
        Lista de envíos asignados al repartidor.

    Métodos
    -------
    actualizar_ubicacion(nueva_ubicacion: str) -> None
        Actualiza la ubicación del repartidor.
    
    cambiar_estado(nuevo_estado: str) -> None
        Cambia el estado del repartidor si el estado es válido.
    
    asignar_envio(envio) -> None
        Asigna un envío al repartidor si está disponible.
    
    finalizar_envio(envio) -> None
        Marca un envío como completado y actualiza el estado.
    
    obtener_estado() -> str
        Devuelve el estado actual del repartidor.
    
    distribuir_envios(repartidores: List['Repartidor'], envios: List) -> None
        Método estático que distribuye los envíos entre repartidores disponibles.
    """


    def __init__(self, nombre, id, telefono, provincia, ubicacion_tiempo_real, vehiculo):
        """
        Inicializa un repartidor con la información básica.

        Parámetros
        ----------
        nombre : str
            Nombre del repartidor.
        id : int
            Identificador único del repartidor.
        telefono : str
            Número de teléfono de contacto.
        provincia : str
            Provincia en la que opera.
        ubicacion_tiempo_real : str
            Ubicación actual del repartidor.
        vehiculo : Furgoneta
            Vehículo asociado al repartidor.
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
        """
        Actualiza la ubicación en tiempo real del repartidor.

        Parámetros
        ----------
        nueva_ubicacion : str
            Nueva ubicación del repartidor.
        """
        self.ubicacion_tiempo_real = nueva_ubicacion

    def cambiar_estado(self, nuevo_estado):
        """
        Cambia el estado del repartidor.

        Parámetros
        ----------
        nuevo_estado : str
            El nuevo estado a asignar al repartidor.

        Raises
        ------
        ValueError
            Si el estado no es uno de los permitidos.
        """
        estados_validos = ["disponible", "en reparto", "descanso", "no disponible"]
        if nuevo_estado in estados_validos:
            self.estado = nuevo_estado
        else:
            raise ValueError("Estado no válido")

    def asignar_envio(self, envio):
        """
        Asigna un envío al repartidor si está disponible.

        Parámetros
        ----------
        envio : object
            El envío a ser asignado.
        """
        if self.estado == "disponible":
            self.envios_asignados.append(envio)
            self.vehiculo.asignar_envio(envio)
            self.cambiar_estado("en reparto")
        else:
            print(f"El repartidor {self.nombre} no está disponible.")

    def finalizar_envio(self, envio):
        """
        Marca un envío como completado.

        Parámetros
        ----------
        envio : object
            El envío que se ha completado.
        """
        if envio in self.envios_asignados:
            self.envios_asignados.remove(envio)
            self.vehiculo.envios_asignados.remove(envio)
            if not self.envios_asignados:
                self.cambiar_estado("disponible")

    def obtener_estado(self):
        """
        Devuelve el estado actual del repartidor.

        Returns
        -------
        str
            Estado actual del repartidor.
        """
        return self.estado

    @staticmethod
    def distribuir_envios(repartidores, envios):
        """
        Distribuye los envíos entre los repartidores disponibles con furgoneta.

        Parámetros
        ----------
        repartidores : list of Repartidor
            Lista de objetos Repartidor.
        envios : list
            Lista de envíos a asignar.
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
