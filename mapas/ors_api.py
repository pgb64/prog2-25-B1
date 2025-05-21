import openrouteservice
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

class OpenRouteService:
    '''
    Clase que interactúa con la API de OpenRouteService para obtener rutas e información.
    '''
    API_KEY = '5b3ce3597851110001cf6248aa6fb35f15ad4099b71f6bb634b0985e'

    def __init__(self):
        '''
        Inicia el cliente de ORS y el geolocalizador (Nominatim).
        '''
        try:
            # Cliente de ORS (concetado a la api)
            self.client = openrouteservice.Client(key=self.API_KEY)
            # Cliente de geolocalización (módulo Nominatim de geopy)
            self.geolocator = Nominatim(user_agent="reparto-simulador")
        except Exception as e:
            # Si surge algún error no se para el flujo de la ejecución
            print(f"Error al inicializar el cliente: {e}")
            raise


    def obtener_cords(self, direccion: str) -> tuple | None:
        '''
        Obtiene la latitud y longitud a partir de una dirección pasado como string.

        Parámetros:
        -----------
        direccion : str
            Dirección que se desea geolocalizar
        '''
        try:
            # Intentar geolocalizar la dirección
            location = self.geolocator.geocode(direccion, timeout=10)
            if location:
                # Si se encuentra la dirección, devuelve una tupla de las coordenadas
                return (location.latitude, location.longitude)
        
            print(f"No se encontraron coordenadas para '{direccion}'.")

        except Exception as e:
            print(f"Error inesperado al obtener coordenadas para '{direccion}': {e}")
        
        return None

    def intentar_ruta(self, cord_origen : tuple, cord_destino : tuple, incluir_pasos : bool = False) -> dict:
        '''
        Intenta obtener la ruta entre dos coordenadas.
        Parámetros:
        -----------
        cord_origen : tuple
            Coordenadas de origen (latitud, longitud)
        cord_destino : tuple
            Coordenadas de destino (latitud, longitud)
        incluir_pasos : bool
            Si se deben incluir los pasos de la ruta en las instrucciones

        Returns:
        --------
        dict
            Resultado de la ruta: distancia, duración, instrucciones, etc.  
        None
            Si no se encuentra la ruta o hay un error.
        '''
        # Diccionario con los parametros para la ruta
        parametros_ruta = {
            'coordinates': [cord_origen, cord_destino], # Coordenadas de origen y destino
            'profile': 'driving-car', # Conducción en vehículo
            'instructions': incluir_pasos, # Instrucciones de la ruta
            'geometry': False, # No se devuelve la geometría de la ruta
            'language': 'es' # Idioma de las instrucciones (español)
        }

        # Devuelve el resultado de la ruta: distancia, duración, instrucciones, etc.
        return self.client.directions(**parametros_ruta)

    @staticmethod
    def mostrar_tiempo(minutos: int | float) -> str:
        ''' 
        Convierte el tiempo en minutos a un formato más amigable para el usuario.

        Parámetros:
        -----------
        minutos : int | float
            Tiempo en minutos que se desea mostrar
        
        Returns:
        --------
        str
            Tiempo legible
        '''
        # Separar en minutos y horas
        minutos = int(round(minutos))
        horas = minutos // 60
        resto_minutos = minutos % 60

        # Posibles formatos de tiempo
        if horas > 0 and resto_minutos > 0:
            return f"{horas}h {resto_minutos}min"
        
        elif horas > 0:
            return f"{horas}h"
        
        else:
            return f"{resto_minutos}min"

    @staticmethod
    def mostrar_distancia(km: float) -> str:
        '''
        Convierte la distancia en km a un formato más amigable para el usuario.

        Parámetros:
        -----------
        km : float
            Distancia en km que se desea mostrar
        Returns:
        --------
        str
            Distancia legible
        '''
        # Distancias cortas con solo metros
        if km >= 1:
            return f"{km} km"
        else:
            metros = int(km * 1000)
            return f"{metros} m"


    def obtener_ruta(self, origen_cords: tuple, destino_cords: tuple, incluir_pasos=False) -> tuple | None:
        '''
        Obtiene la ruta entre dos coordenadas.
        Parámetros:
        -----------
        origen_cords : tuple
            Coordenadas de origen (latitud, longitud)
        destino_cords : tuple
            Coordenadas de destino (latitud, longitud)
        incluir_pasos : bool
            Si se deben incluir los pasos de la ruta en las instrucciones

        Returns:
        --------
        tuple
            Distancia de la ruta (km), duración (min), instrucciones
        None
            Si no se encuentra la ruta o hay un error.
        '''
        if origen_cords is None or destino_cords is None:
            # Si las coordenadas son inválidas
            print("Coordenadas de origen o destino no válidas para la ruta.")
            return None
        
        # Se invierte el orden de las coordenadas para la API (cambio imprescindible)
        origen = [origen_cords[1], origen_cords[0]]
        destino = [destino_cords[1], destino_cords[0]]

        try:
            # Intenta obtener la ruta entre las coordenadas
            ruta = self.intentar_ruta(origen, destino, incluir_pasos)

        except openrouteservice.exceptions.ApiError as e:
            if "2010" in str(e):
                print("No se encontró ningún punto válido, buscando otro cercano...")
                # Nueva posición aproximada
                origen = self.buscar_punto_valido(origen)
                destino = self.buscar_punto_valido(destino)

                if origen is None or destino is None:
                    # Si no se encuentra un punto válido
                    print("No se pudo encontrar un punto válido cercano.")
                    return None

                try:
                    # Vuelve a intentar obtener la ruta con los nuevos puntos
                    ruta = self.intentar_ruta(origen, destino, incluir_pasos)

                except Exception as e2:
                    print(f"Error inesperado tras buscar puntos válidos: {e2}")
                    return None
            else:
                print(f"Error inesperado en la API: {e}")
                return None
            
        except Exception as e:
            # Captura cualquier otro error inesperado
            print(f"Error : {e}")
            return None

        if ruta and ruta.get('routes'):
            # Ruta principal y la información
            ruta_principal = ruta['routes'][0]
            summary = ruta_principal['summary']

            # Distancia y duración de la ruta
            distancia = OpenRouteService.mostrar_distancia(summary['distance'] / 1000) 
            duracion = OpenRouteService.mostrar_tiempo(summary['duration'] / 60)

            # Rellenar la lista de instrucciones
            lista_instrucciones = []
            if incluir_pasos and 'segments' in ruta_principal:
                for segment in ruta_principal['segments']:
                    for instruction in segment['steps']:
                        lista_instrucciones.append(instruction["instruction"])

            return (distancia, duracion, lista_instrucciones)

        print('No se han encontrado rutas válidas.')
        return None

    def buscar_punto_valido(self, cord : tuple, radio_grados : float=0.001, pasos : int=5) -> tuple | None:
        '''
        Busca un punto válido en un radio de 0.001 grados alrededor de las coordenadas dadas.
        Parámetros:
        -----------
        cord : tuple
            Coordenadas (latitud, longitud) que se desea validar
        radio_grados : float
            Radio en grados para buscar un punto válido
        pasos : int
            Número de pasos en cada dirección para buscar un punto válido
        Returns:
        --------
        tuple
            Coordenadas válidas (latitud, longitud)
        None
            Si no se encuentra un punto válido
        '''
        lon0, lat0 = cord

        # Se busca un punto válido en un radio de 0.001 grados
        for dx in range(-pasos, pasos + 1):
            for dy in range(-pasos, pasos + 1):

                # Nueva posición aproximada
                prueba = [lon0 + dx * radio_grados, lat0 + dy * radio_grados]
                try:
                    # Se intenta obtener la ruta con la nueva posición
                    self.client.directions(coordinates=[prueba, prueba], profile='driving-car', geometry=False)
                    return prueba
                
                # Si no se encuentra un punto válido
                except openrouteservice.exceptions.ApiError as e:
                    if "2010" in str(e):
                        continue
                    else:
                        raise
        return None

