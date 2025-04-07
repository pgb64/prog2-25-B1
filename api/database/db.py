import csv
import os

class Db:
    """Gestor de base de datos CSV para usuarios y sus datos personales (Esta bastante crudo esto, segun me pidais puedo añadir nuevos metodos)
    
    Esta clase proporciona una interfaz para gestionar usuarios y sus datos personale almacenados en archivos CSV. Usa dos archivos principales:
    - usuarios.csv: Contiene credenciales y tipo de usuario
    - datos_personales.csv: Almacena información personal de los usuarios
    
    Attributes
    ----------
    usuarios_csv : str
        Ruta al archivo CSV de usuarios (data/usuarios.csv)
    datos_csv : str
        Ruta al archivo CSV de datos personales (data/datos_personales.csv)
    """
    
    def __init__(self):
        """Inicializa todos los archivos CSV necesarios"""
        # Rutas de los archivos
        self.usuarios_csv = 'data/usuarios.csv'
        self.datos_csv = 'data/datos_personales.csv'
        self.articulos_csv = 'data/articulos.csv'
        self.paquetes_csv = 'data/paquetes.csv'
        self.repartidores_csv = 'data/repartidores.csv'
        self.furgonetas_csv = 'data/furgonetas.csv'
        
        os.makedirs('data', exist_ok=True)
        
        # Archivos CSV y sus cabeceras
        archivos_config = {
            self.usuarios_csv: ['id', 'user', 'pass', 'type'],
            self.datos_csv: ['id', 'fecha', 'dir', 'cp', 'ciudad', 'genero'],
            self.articulos_csv: ['nombre', 'codigo', 'cantidad', 'proveedor', 'descripcion'],
            self.paquetes_csv: ['nombre', 'codigo_envio', 'procedencia', 'usuario_receptor', 'enviado'],
            self.repartidores_csv: ['nombre', 'id', 'telefono', 'provincia', 'ubicacion_tiempo_real', 
                                'vehiculo', 'estado', 'envios_asignados'],
            self.furgonetas_csv: ['matricula', 'capacidad_maxima', 'provincia', 'envios_asignados', 'conductor']
        }
        
        # Bucle para inicializar los archivos CSV
        for archivo, campos in archivos_config.items():
            if not os.path.exists(archivo) or os.path.getsize(archivo) == 0:
                with open(archivo, 'w', newline='') as f:
                    csv.writer(f).writerow(campos)
                    
                    
# ---- Métodos de gestion de usuarios ----
                    
    def add_user(self, user, password, tipo):
        """Registra un nuevo usuario en el sistema
        
        Parameters
        ----------
        user : str
            Nombre de usuario para registrar
        password : str
            Contraseña del usuario
        tipo : str
            Tipo de usuario (admin/repartidor/cliente)
        
        Returns
        -------
        int
            ID asignado al nuevo usuario
        """
        users = self.get_users()
        new_id = len(users) + 1
        with open(self.usuarios_csv, 'a', newline='') as f:
            csv.writer(f).writerow([new_id, user, password, tipo])
        return new_id

    def add_data(self, user_id, **data):
        """Guarda datos personales de un usuario
        
        Parameters
        ----------
        user_id : int
            ID del usuario al que pertenecen los datos
        **data : dict
            Datos personales a almacenar puesto con el **data para dar flexibilidad (Habria que cambiar los campos solo)
        """
        campos = ['id','fecha','dir','cp','ciudad','genero']
        data['id'] = str(user_id)
        
        with open(self.datos_csv, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=campos)
            writer.writerow({k: data.get(k, '') for k in campos})

    def get_users(self):
        """Obtiene todos los usuarios registrados
        
        Returns
        -------
        list
            Lista de diccionarios con la información de cada usuario, con las claves: 'id', 'user', 'pass', 'type'
        """
        with open(self.usuarios_csv, 'r') as f:
            return list(csv.DictReader(f))

    def get_data(self):
        """Obtiene todos los datos personales almacenados
        Returns
        -------
        list
            Lista de diccionarios con los datos personales, con las claves: 'id', 'fecha', 'dir', 'cp', 'ciudad', 'genero'
        """
        with open(self.datos_csv, 'r') as f:
            return list(csv.DictReader(f))

    def get_user(self, user_id=None, username=None):
        """Busca un usuari
        
        Parameters
        ----------
        user_id : int
            ID del usuario a buscar
        username : str
            Nombre de usuario a buscar
        
        Returns
        -------
        dict or None
            Diccionario con los datos del usuario si se encuentra,
            None en caso contrario
        """
        for user in self.get_users():
            if user_id and user['id'] == str(user_id):
                return user
            if username and user['user'] == username:
                return user
        return None

    def get_user_data(self, user_id):
        """Obtiene los datos personales de un usuario específico
        Parameters
        ----------
        user_id : int
            ID del usuario cuyos datos se buscan  
        Returns
        -------
        dict or None
            Diccionario con los datos personales si existen,
            None en caso contrario
        """
        for data in self.get_data():
            if data['id'] == str(user_id):
                return data
        return None

    def get_data_field(self, user_id, field):
        """Obtiene un campo específico de los datos personales de un usuario
        
        Parameters
        ----------
        user_id : int
            ID del usuario
        field : str
            Nombre del campo a recuperar
        Returns
        -------
        str or None
            Valor del campo si existe,
            None en caso contrario
        """
        data = self.get_user_data(user_id)
        if data and field in data:
            return data[field]
        return None

    def get_by_type(self, user_type):
        """Filtra usuarios por tipo (admin/repartidor/cliente)
        
        Parameters
        ----------
        user_type : str
            Tipo de usuario a filtrar
        Returns
        -------
        list[dict]
            Lista de usuarios que coinciden con el tipo especificado
        """
        return [u for u in self.get_users() if u['type'] == user_type]

    def get_by_city(self, city):
        """Filtra usuarios por ciudad de residencia
        
        Parameters
        ----------
        city : str
            Ciudad por la que filtrar (búsqueda no sensible a mayúsculas)
        Returns
        -------
        list[dict]
            Lista de diccionarios con estructura:
            {'user': datos_usuario, 'data': datos_personales}
        """
        results = []
        for data in self.get_data():
            if data['ciudad'].lower() == city.lower():
                user = self.get_user(user_id=data['id'])
                results.append({'user': user, 'data': data})
        return results

    def login(self, user, password):
        """Valida credenciales de acceso
        
        Parameters
        ----------
        user : str
            Nombre de usuario
        password : str
            Contraseña
        Returns
        -------
        dict or None
            Datos del usuario si las credenciales son válidas,
            None en caso contrario
        """
        user_data = self.get_user(username=user)
        if user_data and user_data['pass'] == password:
            return user_data
        return None

    def is_admin(self, user):
        """Comprueba si un usuario tiene privilegios de administrador
        
        Parameters
        ----------
        user : dict
            Diccionario con los datos del usuario
            (debe contener 'user' y 'pass')
        
        Returns
        -------
        bool
            True si el usuario es administrador,
            False en caso contrario
        """
        user_data = self.login(user['user'], user['pass'])
        return user_data and user_data['type'] == 'admin'
    
# ---- Métodos de gestion de articulos ----
    def add_articulo(self, nombre, codigo, cantidad, proveedor, descripcion):
        """Añade un nuevo articulo al sistema"""
        with open(self.articulos_csv, 'a', newline='') as f:
            csv.writer(f).writerow([nombre, codigo, cantidad, proveedor, descripcion])
            
    def get_articulos(self):
        """Obtiene todos los articulos"""
        with open(self.articulos_csv, 'r') as f:
            return list(csv.DictReader(f))
    
    def get_articulo_codigo(self, codigo):
        """Obtiene un articulo especifico por su codigo"""
        for articulo in self.get_articulos(): #Sacamos los articulos con la funcion para obtenerlos todos
            if articulo['codigo'] == codigo:
                return articulo
        return None
    
    

# ---- Métodos de gestion de paquetes ----
    def add_paquete(self, nombre, codigo_envio, procedencia, usuario_receptor, enviado):
        """Registramos un nuevo paquete (El tema booleano me ha dado muchos problemas al leerlo luego 
        asi que lo guardo como string, si alguien sabe como hacerlo mejor que me lo diga)"""
        if  enviado:   
            enviado_s = 'True'
        else:
            enviado_s = 'False'
        with open(self.paquetes_csv, 'a') as f:
            csv.writer(f).writerow([nombre, codigo_envio, procedencia, usuario_receptor, enviado_s]) 
            
    def get_paquetes(self):
        """Obtiene los paquetes ya registrados"""
        with open(self.paquetes_csv, 'r') as f:
            paquetes = list(csv.DictReader(f))
        #Convertimos enviado a booleano
        for paquete in paquetes:
            paquete['enviado'] = paquete['enviado'] == 'True'
        return paquetes
    
    def get_paquete_by_codigo(self, codigo_envio):
        """Obtiene un paquete especifico por su codigo"""
        for paquete in self.get_paquetes():
            if paquete['codigo_envio'] == codigo_envio:
                return paquete
        return None
    
    def update_estado_envio(self, codigo_envio, enviado):
        """ACtualiz el estado de un envio de paquete"""
        paquetes = self.get_paquetes()
        updated = False
        
        with open(self.paquetes_csv, 'w', newline='') as f:
            # Corregido: pasar una lista de fieldnames en lugar de intentar indexar
            fieldnames = ['nombre', 'codigo_envio', 'procedencia', 'usuario_receptor', 'enviado']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for paquete in paquetes:
                if paquete['codigo_envio'] == str(codigo_envio):
                    paquete['enviado'] = 'True' if enviado else 'False'
                    updated = True
                writer.writerow(paquete)
        return updated
            

# --- Metodos para gestion de repartidores ---
    def add_repartidor(self, nombre, telefono, provincia, vehiculo):
        """Añade un nuevo repartidor a la base de dato """
        repartidores = self.get_repartidores()
        
        # Generar nuevo ID
        existing_ids = [int(r['id']) for r in repartidores if r['id'].isdigit()]
        new_id = max(existing_ids) + 1 if existing_ids else 1
        
        with open(self.repartidores_csv, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([nombre, str(new_id), telefono, provincia, '', vehiculo, 'disponible','0'])
        return new_id
    
    def get_repartidores(self):
        """Obtiene todos los repartidoress"""
        with open(self.repartidores_csv, 'r')as f:
            return list(csv.DictReader(f))
    
    def update_ubicacion_repartidor(self, repartidor_id, ubicacion):
        """Actualiza la ubicacion en tiempo real de un repartidor"""
        repartidores = self.get_repartidores()
        updated = False

        with open(self.repartidores_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['nombre', 'id', 'telefono', 'provincia', 'ubicacion_tiempo_real', 'vehiculo', 'estado', 'envios_asignados'])
            writer.writeheader()

            for repartidor in repartidores:
                if repartidor['id'] == str(repartidor_id):
                    repartidor['ubicacion_tiempo_real'] = ubicacion
                    updated = True
                writer.writerow(repartidor)

        return updated

# --- Metodos para la clase Furgonetas ---
    def add_furgoneta(self, matricula, capacidad_maxima, provincia, conductor):
        """Añade una furgoneta a la base de datos"""
        with open(self.furgonetas_csv, 'a', newline='') as f:
            csv.writer(f).writerow([matricula, str(capacidad_maxima), provincia, '0', conductor])
    
    def get_furgonetas(self):
        """Obtiene la informacion de todas las furgonetas"""
        with open(self.furgonetas_csv, 'r') as f:
            return list(csv.DictReader(f))
        
    def asignar_conductor_furgoneta(self,matricula, conductor_id):
        """Asignaa un conductor a una furgoneta ya registrada """
        furgonetas = self.get_furgonetas()
        updated = False
        
        with open(self.furgonetas_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['matricula', 'capacidad_maxima', 'provincia', 'envios_asignados', 'conductor'])
            writer.writeheader()
            
            for furgoneta in furgonetas:
                if furgoneta['matricula'] == matricula:
                    furgoneta['conductor'] = str(conductor_id)
                    updated = True
                writer.writerow(furgoneta)
        return updated
