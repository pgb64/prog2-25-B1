# Importar los módulos necesarios
import os
import folium
import webbrowser
from mapas import sedes
from mapas import ors_api
import openrouteservice  

class MapaGestor:
    def __init__(self, centro=(40.4168, -3.7038), zoom=6, archivo="temporal/mapa_sedes.html"):
        ''' 
        Inicia el gestor de mapas con un centro y zoom por defecto
        '''
        self.centro = centro # Centro del mapa de España
        self.zoom = zoom # Zoom por defecto
        self.archivo = archivo # Archivo donde se guardará el mapa
        # Crear la carpeta si no existe
        carpeta = os.path.dirname(self.archivo)
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

    def generar_mapa_sedes(self) -> None:
        '''
        Genera un mapa con las sedes de la empresa.
        '''
        # Crea el mapa con folium
        mapa = folium.Map(location=self.centro, zoom_start=self.zoom)
        sedes.Sede.cargar_csv() # Cargar las sedes desde el csv
        
        # Añade un marcador para cada una de las sedes
        for nombre, coords in sedes.Sede.info_sedes():
            folium.Marker(
                location=coords,
                popup=nombre,
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(mapa)
        
        # Guarda el mapa en un archivo html
        mapa.save(self.archivo)

    def abrir_mapa(self) -> None:
        '''
        Abre el mapa en el navegador.
        '''
        # Ruta absoluta del archivo
        ruta_absoluta = os.path.abspath(self.archivo)
        try:
            # Intenta abrir el mapa en Firefox
            webbrowser.get('firefox').open(f"file://{ruta_absoluta}")
        except:
            # Si no se puede abrir en Firefox, abre en el navegador por defecto
            webbrowser.open(f"file://{ruta_absoluta}")

    def mostrar_mapa_sedes(self) -> None:
        '''
        Genera y muestra el mapa de las sedes.
        '''
        self.generar_mapa_sedes()
        self.abrir_mapa()

    def generar_mapa_destino(self, coords_destino):
        '''
        Genera un mapa con la ruta de la sede más cercana al destino.
        '''
        # Crea el mapa con folium
        mapa = folium.Map(location=coords_destino, zoom_start=13)
        # Carga las sedes desde el csv
        sedes.Sede.cargar_csv()
        # Añade a una lista las coordenadas de todas las sedes
        sedes_coords = [sedes.Sede.sede_coord(sede[0]) for sede in sedes.Sede.info_sedes()]

        # Instancia de OpenRouteService y obtiene la sede más cercana
        ors = ors_api.OpenRouteService()
        sede_cercana = ors.sede_mas_cercana(coords_destino, sedes.Sede.info_sedes())

        if sede_cercana is None:
            return
        # Obtener coordenadas de la sede más cercana
        coords_sede = sedes.Sede.sede_coord(sede_cercana)

        # Añadir marcadores al destino y a la sede
        folium.Marker(
            location=coords_sede,
            popup=f"Sede más cercana: {sede_cercana}",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(mapa)

        folium.Marker(
            location=coords_destino,
            popup="Destino",
            icon=folium.Icon(color='blue')
        ).add_to(mapa)

        # Obtener ruta (instrucciones)
        ruta_info = ors.obtener_ruta(coords_sede, coords_destino, incluir_pasos=True)

        if ruta_info:
            # Añadir la ruta al mapa
            try:
                # Obtener la geometría de la ruta
                geometry = ors.client.directions(
                    coordinates=[[coords_sede[1], coords_sede[0]], [coords_destino[1], coords_destino[0]]],
                    profile='driving-car',
                    geometry=True
                )['routes'][0]['geometry']

                # Decodifica la geometría de la ruta
                decoded = openrouteservice.convert.decode_polyline(geometry)['coordinates']
                puntos = [(lat, lon) for lon, lat in decoded]  # Invertir orden (por formato)
                folium.PolyLine(locations=puntos, color='black', weight=4).add_to(mapa)

            except Exception as e:
                # Captura cualquier error
                print(f"No se pudo dibujar la ruta: {e}")

            # Añadir instrucciones de la ruta
            pasos = ruta_info[2]
            instrucciones = "\n".join([f"{i+1}. {paso}" for i, paso in enumerate(pasos)])
            # Añadir los paso de la ruta al mapa
            folium.Marker(
                location=coords_destino,
                popup=f"Instrucciones:\n{instrucciones}",
                icon=folium.Icon(color='blue')
            ).add_to(mapa)

        # Guardar el mapa en un archivo html
        mapa.save(self.archivo)

    def mostrar_mapa_destino(self, coords_destino):
        '''
        Genera y muestra el mapa de la ruta al destino.
        '''
        self.generar_mapa_destino(coords_destino)
        self.abrir_mapa()