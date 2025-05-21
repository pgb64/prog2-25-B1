import openrouteservice
from geopy.geocoders import Nominatim
from sedes import Sede

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


    def obtener_coords(self, direccion: str) -> tuple | None:
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

    def intentar_ruta(self, coord_origen : tuple, coord_destino : tuple, incluir_pasos : bool = False) -> dict:
        '''
        Intenta obtener la ruta entre dos coordenadas.
        Parámetros:
        -----------
        coord_origen : tuple
            Coordenadas de origen (latitud, longitud)
        coord_destino : tuple
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
            'coordinates': [coord_origen, coord_destino], # Coordenadas de origen y destino
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
    
    @staticmethod
    def obtener_provincia_por_cp(codigo_postal):
        """
        Dada un código postal de 5 dígitos de España, devuelve la provincia a la que pertenece.

        Args:
            codigo_postal (str): El código postal de 5 dígitos (ej. "03560").

        Returns:
            str: El nombre de la provincia o "Provincia no encontrada" si el código no es válido.
        """

        if not isinstance(codigo_postal, str) or len(codigo_postal) != 5 or not codigo_postal.isdigit():
            return "Código postal no válido. Debe ser una cadena de 5 dígitos."

        prefijo = codigo_postal[:2]

        provincias = {
            "01": "Álava",
            "02": "Albacete",
            "03": "Alicante",
            "04": "Almería",
            "05": "Ávila",
            "06": "Badajoz",
            "07": "Islas Baleares",
            "08": "Barcelona",
            "09": "Burgos",
            "10": "Cáceres",
            "11": "Cádiz",
            "12": "Castellón",
            "13": "Ciudad Real",
            "14": "Córdoba",
            "15": "A Coruña",
            "16": "Cuenca",
            "17": "Girona",
            "18": "Granada",
            "19": "Guadalajara",
            "20": "Gipuzkoa",
            "21": "Huelva",
            "22": "Huesca",
            "23": "Jaén",
            "24": "León",
            "25": "Lleida",
            "26": "La Rioja",
            "27": "Lugo",
            "28": "Madrid",
            "29": "Málaga",
            "30": "Murcia",
            "31": "Navarra",
            "32": "Ourense",
            "33": "Asturias",
            "34": "Palencia",
            "35": "Las Palmas",
            "36": "Pontevedra",
            "37": "Salamanca",
            "38": "Santa Cruz de Tenerife",
            "39": "Cantabria",
            "40": "Segovia",
            "41": "Sevilla",
            "42": "Soria",
            "43": "Tarragona",
            "44": "Teruel",
            "45": "Toledo",
            "46": "Valencia",
            "47": "Valladolid",
            "48": "Vizcaya",
            "49": "Zamora",
            "50": "Zaragoza",
            "51": "Ceuta",
            "52": "Melilla"
        }

        return provincias.get(prefijo, "Provincia no encontrada")






    def obtener_ruta(self, origen_coords: tuple, destino_coords: tuple, incluir_pasos=False) -> tuple | None:
        '''
        Obtiene la ruta entre dos coordenadas.
        Parámetros:
        -----------
        origen_coords : tuple
            Coordenadas de origen (latitud, longitud)
        destino_coords : tuple
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
        if origen_coords is None or destino_coords is None:
            # Si las coordenadas son inválidas
            print("Coordenadas de origen o destino no válidas para la ruta.")
            return None
        
        # Se invierte el orden de las coordenadas para la API (cambio imprescindible)
        origen = [origen_coords[1], origen_coords[0]]
        destino = [destino_coords[1], destino_coords[0]]

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

    def buscar_punto_valido(self, coord : tuple, radio_grados : float=0.001, pasos : int=5) -> tuple | None:
        '''
        Busca un punto válido en un radio de 0.001 grados alrededor de las coordenadas dadas.
        Parámetros:
        -----------
        coord : tuple
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
        lon0, lat0 = coord

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

    @staticmethod
    def mostrar_ruta(info):
        if info is not None:
            distancia, duracion, instrucciones = info

            pasos = ""
            for i, instruccion in enumerate(instrucciones):
                pasos += f"{i + 1}. {instruccion}\n"
            return f'''\nINFORMACIÓN DE LA RUTA
--------------------------
- Distancia: {distancia}
- Duración: {duracion}
- Instrucciones:
--------------------------
{pasos}'''

    def sede_mas_cercana(self, coords: tuple, lista_sedes: list[tuple]) -> str | None:
        """
        Devuelve el nombre de la sede más cercana usando distancia Manhattan aproximada.

        Parámetros
        ----------
        coords : tuple
            Coordenadas (latitud, longitud) del usuario.
        lista_sedes : list of tuples
            Lista con tuplas (nombre_sede, (lat, lon)).

        Returns
        -------
        str | None
            Nombre de la sede más cercana o None si la lista está vacía.
        """
        if not lista_sedes:
            lista_sedes = [sede[0] for sede in Sede.info_sedes()]

        sede_cercana = None
        distancia_min = None

        for nombre, (lat, lon) in lista_sedes:
            dist = abs(coords[0] - lat) + abs(coords[1] - lon)  
            if distancia_min is None or dist < distancia_min:
                distancia_min = dist
                sede_cercana = nombre

        return sede_cercana


if __name__ == "__main__":
    
    ors = OpenRouteService()
    coords = ors.obtener_coords("ruperto chapí 39, novelda")
    print(coords)
    
    Sede.cargar_csv() # Si no se pone devuelve None
    sede = ors.sede_mas_cercana(coords, Sede.info_sedes())
    print(f"La sede más cercana es: {sede}")

    #Ruta de sede a la coordenada
    cord_sede = Sede.sede_coord(sede)
    ruta = ors.obtener_ruta(coords, cord_sede, incluir_pasos=True)
    print(ruta)
    print(OpenRouteService.mostrar_ruta(ruta))

