import csv

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
        """Inicializa los archivos CSV
        Crea los archivos si no existen y establece las cabeceras necesarias.
        """
        self.usuarios_csv = 'data/usuarios.csv'
        self.datos_csv = 'data/datos_personales.csv'
        
        # Crear archivos si no existen
        with open(self.usuarios_csv, 'a+') as f: pass
        with open(self.datos_csv, 'a+') as f: pass
        
        # Inicializar cabeceras
        for archivo, campos in [
            (self.usuarios_csv, ['id','user','pass','type']),
            (self.datos_csv, ['id','fecha','dir','cp','ciudad','genero'])
        ]:
            with open(archivo, 'r+', newline='') as f:
                if not f.read(1):
                    csv.writer(f).writerow(campos)

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
