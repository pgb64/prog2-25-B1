import csv
import os
import bcrypt
import pandas as pd
from database.security import Security


class Db:
    """Gestor de base de datos CSV para users y sus datos personales
    
    Esta clase ahora:
    - Usa bcrypt para hashing de contraseñas
    - Archivos renombrados: users.csv y personal.csv
    - Devuelve códigos HTTP en sus operaciones:
      - 200: OK
      - 201: Creado
      - 400: Error en la solicitud
      - 404: No encontrado
      - 409: Conflicto (ya existe)
    """
    
    def __init__(self):
        self.users_csv = 'data/users.csv'
        self.personal_csv = 'data/personal.csv'
        self.articulos_csv = 'data/articulos.csv'
        self.paquetes_csv = 'data/paquetes.csv'
        self.repartidores_csv = 'data/repartidores.csv'
        self.furgonetas_csv = 'data/furgonetas.csv'
        
        os.makedirs('data', exist_ok=True)
        
        archivos_config = {
            self.users_csv: ['id', 'user', 'password', 'type'],
            self.personal_csv: ['id', 'fecha', 'dir', 'cp', 'ciudad', 'genero'],
            self.articulos_csv: ['nombre', 'codigo', 'cantidad', 'proveedor', 'descripcion'],
            self.paquetes_csv: ['nombre', 'codigo_envio', 'procedencia', 'usuario_receptor', 'enviado'],
            self.repartidores_csv: ['nombre', 'id', 'telefono', 'provincia', 'ubicacion_tiempo_real', 
                                'vehiculo', 'estado', 'envios_asignados'],
            self.furgonetas_csv: ['matricula', 'capacidad_maxima', 'provincia', 'envios_asignados', 'conductor']
        }
        
        for archivo, campos in archivos_config.items():
            if not os.path.exists(archivo) or os.path.getsize(archivo) == 0:
                with open(archivo, 'w', newline='') as f:
                    csv.writer(f).writerow(campos)
                    



    # ---- Métodos de gestión de usuarios ----
                    
    def add_user(self, user: str, password: str, tipo: str) -> int:
        """Registra un nuevo usuario con contraseña hasheada y verifica la fortaleza de la contraseña."""
        try:
            print(f"Intentando añadir usuario: {user}")  # Depuración
            # Verificar si la contraseña cumple con los requisitos de seguridad
            password_strength = Security.check_password_strength(password)
            print(f"Resultado de check_password_strength: {password_strength}")  # Depuración
            if password_strength == 401:
                print("Error: Contraseña inválida")  # Depuración
                return 401  # Contraseña inválida

            # Verificar si el usuario ya existe
            existing_user = self.get_user(username=user)
            print(f"Usuario existente: {existing_user}")  # Depuración
            if existing_user:
                print("Error: Usuario ya existe")  # Depuración
                return 409  # Conflicto: ya existe

            # Generar el nuevo ID del usuario
            users = self.get_users()
            print(f"Usuarios actuales: {users}")  # Depuración
            new_id = len(users) + 1
            print(f"Nuevo ID generado: {new_id}")  # Depuración

            # Hashear la contraseña utilizando la clase Security
            hashed_pw = Security.hash_password(password)
            print(f"Contraseña hasheada: {hashed_pw}")  # Depuración

            # Registrar el usuario en el archivo CSV
            with open(self.users_csv, 'a', newline='') as f:
                csv.writer(f).writerow([new_id, user, hashed_pw, tipo])
            print("Usuario registrado correctamente en el archivo CSV")  # Depuración

            return 201  # Usuario creado con éxito

        except Exception as e:
            print(f"Error al añadir user: {e}")  # Depuración
            return 400  # Error

    def add_data(self, user_id, **data):
        """Guarda datos personales"""
        try:
            campos = ['id','fecha','dir','cp','ciudad','genero']
            data['id'] = str(user_id)
            
            with open(self.personal_csv, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=campos)
                writer.writerow({k: data.get(k, '') for k in campos})
            return 201
        except:
            return 400

    def get_users(self):
        """Obtiene todos los users"""
        try:
            with open(self.users_csv, 'r') as f:
                return list(csv.DictReader(f))
        except:
            return []

    def get_data(self):
        """Obtiene datos personales"""
        try:
            with open(self.personal_csv, 'r') as f:
                return list(csv.DictReader(f))
        except:
            return []

    def get_user(self, user_id=None, username=None):
        """Busca un usuario
        
        Returns:
            dict: Datos del usuario o None si no existe
        """
        try:
            for user in self.get_users():
                if user_id and user['id'] == str(user_id):
                    return user
                if username and user['user'] == username:
                    return user
            return None
        except:
            return None

    def get_user_data(self, user_id):
        """Obtiene datos personales de un usuario
        
        Returns:
            dict: Datos personales o None si no existen
        """
        try:
            for data in self.get_data():
                if data['id'] == str(user_id):
                    return data
            return None
        except:
            return None

    def get_data_field(self, user_id, field):
        """Obtiene un campo específico de datos personales
        
        Returns:
            str: Valor del campo o None si no existe
        """
        data = self.get_user_data(user_id)
        return data.get(field) if data else None

    def get_by_type(self, user_type):
        """Filtra usuarios por tipo
        
        Returns:
            list: Usuarios del tipo especificado o [] si no hay
        """
        try:
            return [u for u in self.get_users() if u['type'] == user_type]
        except:
            return []

    def get_by_city(self, city):
        """Filtra usuarios por ciudad
        
        Returns:
            list: Usuarios en la ciudad o [] si no hay
        """
        try:
            results = []
            for data in self.get_data():
                if data['ciudad'].lower() == city.lower():
                    user = self.get_user(user_id=data['id'])
                    if user:
                        results.append({'user': user, 'data': data})
            return results
        except:
            return []

    def login(self, user: str, password: str):
        """Verifica las credenciales de un usuario y la validez de la contraseña."""
        
        # Obtener los datos del usuario
        user_data = self.get_user(username=user)
        if user_data is None:
            return 400  # Usuario no encontrado

        # Verificar la fortaleza de la contraseña utilizando la clase Security
        password_strength = Security.check_password_strength(password)
        if password_strength == 401:
            return 401  # Contraseña inválida (no cumple los requisitos)

        # Verificar que la contraseña coincida con la almacenada en la base de datos
        hashed_password = user_data['password']
        if not Security.verify_password(password, hashed_password):
            return 401  # Contraseña incorrecta

        return 200  # Login exitoso


    def is_admin(self, user):
        """Comprueba si un usuario es admin
        
        Returns:
            bool: True si es admin, False si no
        """
        user_data = self.login(user['user'], user['pass'])
        return user_data and user_data['type'] == 'admin'
    

    def delete_user(self, user_id):
        """Elimina un user"""
        try:
            users = self.get_users()
            updated = False
            
            with open(self.users_csv, 'w', newline='') as f:  # Cambiado a users.csv
                writer = csv.DictWriter(f, fieldnames=['id', 'user', 'password', 'type'])
                writer.writeheader()
                
                for user in users:
                    if user['id'] != str(user_id):
                        writer.writerow(user)
                    else:
                        updated = True
            
            if updated:
                self.delete_user_data(user_id)
                return 200
            return 404
        except:
            return 400


    def delete_user_data(self, user_id):
        """Elimina datos personales"""
        try:
            data_list = self.get_data()
            updated = False
            
            with open(self.personal_csv, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['id', 'fecha', 'dir', 'cp', 'ciudad', 'genero'])
                writer.writeheader()
                
                for data in data_list:
                    if data['id'] != str(user_id):
                        writer.writerow(data)
                    else:
                        updated = True
            
            return 200 if updated else 404
        except:
            return 400
    
    # ---- Métodos de gestión de artículos ----
    def add_articulo(self, nombre, codigo, cantidad, proveedor, descripcion):
        """Añade un nuevo artículo
        
        Returns:
            int: 201 si se creó, 400 si hay error
        """
        try:
            if self.get_articulo_codigo(codigo):
                return 409
                
            with open(self.articulos_csv, 'a', newline='') as f:
                csv.writer(f).writerow([nombre, codigo, cantidad, proveedor, descripcion])
            return 201
        except:
            return 400
            
    def get_articulos(self):
        """Obtiene todos los artículos
        
        Returns:
            list: Artículos o [] si hay error
        """
        try:
            with open(self.articulos_csv, 'r') as f:
                return list(csv.DictReader(f))
        except:
            return []
    
    def get_articulo_codigo(self, codigo):
        """Obtiene artículo por código
        
        Returns:
            dict: Datos del artículo o None si no existe
        """
        try:
            for articulo in self.get_articulos():
                if articulo['codigo'] == codigo:
                    return articulo
            return None
        except:
            return None

    def get_codigos_articulos(self):
        try:
            articulos = self.get_articulos()
            codigos = []
            
            for articulo in articulos:
                if 'codigo' in articulo:
                    codigos.append(articulo['codigo'])
            
            return codigos
        except:
            return []


    def delete_articulo(self, codigo):
        """Elimina un artículo del inventario
        
        Returns:
            int: 200 si se eliminó, 404 si no existe, 400 si hay error
        """
        try:
            articulos = self.get_articulos()
            updated = False
            
            with open(self.articulos_csv, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['nombre', 'codigo', 'cantidad', 'proveedor', 'descripcion'])
                writer.writeheader()
                
                for articulo in articulos:
                    if articulo['codigo'] != codigo:
                        writer.writerow(articulo)
                    else:
                        updated = True
            
            return 200 if updated else 404
        except:
            return 400
    






    # ---- Métodos de gestión de paquetes ----
    def add_paquete(self, nombre, codigo_envio, procedencia, usuario_receptor, enviado):
        """Añade un nuevo paquete
        
        Returns:
            int: 201 si se creó, 400 si hay error
        """
        try:
            if self.get_paquete_by_codigo(codigo_envio):
                return 409
                
            enviado_s = 'True' if enviado else 'False'
            with open(self.paquetes_csv, 'a') as f:
                csv.writer(f).writerow([nombre, codigo_envio, procedencia, usuario_receptor, enviado_s]) 
            return 201
        except:
            return 400
            
    def get_paquetes(self):
        """Obtiene todos los paquetes
        
        Returns:
            list: Paquetes o [] si hay error
        """
        try:
            with open(self.paquetes_csv, 'r') as f:
                paquetes = list(csv.DictReader(f))
            for paquete in paquetes:
                paquete['enviado'] = paquete['enviado'] == 'True'
            return paquetes
        except:
            return []
    
    def get_paquete_by_codigo(self, codigo_envio):
        """Obtiene paquete por código
        
        Returns:
            dict: Datos del paquete o None si no existe
        """
        try:
            for paquete in self.get_paquetes():
                if paquete['codigo_envio'] == codigo_envio:
                    return paquete
            return None
        except:
            return None
    
    def update_estado_envio(self, codigo_envio, enviado):
        """Actualiza estado de envío
        
        Returns:
            int: 200 si se actualizó, 404 si no existe, 400 si hay error
        """
        try:
            paquetes = self.get_paquetes()
            updated = False
            
            with open(self.paquetes_csv, 'w', newline='') as f:
                fieldnames = ['nombre', 'codigo_envio', 'procedencia', 'usuario_receptor', 'enviado']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

                for paquete in paquetes:
                    if paquete['codigo_envio'] == str(codigo_envio):
                        paquete['enviado'] = 'True' if enviado else 'False'
                        updated = True
                    writer.writerow(paquete)
                    
            return 200 if updated else 404
        except:
            return 400


    def get_codigos_paquetes(self, enviado=None):
        try:
            paquetes = self.get_paquetes()
            codigos = []
            
            for paquete in paquetes:
                if 'codigo_envio' in paquete:
                    if enviado is None or paquete['enviado'] == enviado:
                        codigos.append(paquete['codigo_envio'])
            
            return codigos
        except:
            return []


    def delete_paquete(self, codigo_envio):
        """Elimina un paquete del sistema
        
        Returns:
            int: 200 si se eliminó, 404 si no existe, 400 si hay error
        """
        try:
            paquetes = self.get_paquetes()
            updated = False
            
            with open(self.paquetes_csv, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['nombre', 'codigo_envio', 'procedencia', 'usuario_receptor', 'enviado'])
                writer.writeheader()
                
                for paquete in paquetes:
                    if paquete['codigo_envio'] != codigo_envio:
                        # Convertimos el booleano a string para guardarlo
                        paquete['enviado'] = 'True' if paquete['enviado'] else 'False'
                        writer.writerow(paquete)
                    else:
                        updated = True
            
            return 200 if updated else 404
        except:
            return 400

    # --- Métodos para gestión de repartidores ---
    def add_repartidor(self, nombre, telefono, provincia, vehiculo):
        """Añade un nuevo repartidor
        
        Returns:
            int: 201 si se creó, 400 si hay error
        """
        try:
            repartidores = self.get_repartidores()
            existing_ids = [int(r['id']) for r in repartidores if r['id'].isdigit()]
            new_id = max(existing_ids) + 1 if existing_ids else 1
            
            with open(self.repartidores_csv, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([nombre, str(new_id), telefono, provincia, '', vehiculo, 'disponible','0'])
            return 201
        except:
            return 400
    
    def get_repartidores(self):
        """Obtiene todos los repartidores
        
        Returns:
            list: Repartidores o [] si hay error
        """
        try:
            with open(self.repartidores_csv, 'r') as f:
                return list(csv.DictReader(f))
        except:
            return []
    
    def update_ubicacion_repartidor(self, repartidor_id, ubicacion):
        """Actualiza ubicación de repartidor
        
        Returns:
            int: 200 si se actualizó, 404 si no existe, 400 si hay error
        """
        try:
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

            return 200 if updated else 404
        except:
            return 400
        
        
    def delete_repartidor(self, repartidor_id):
        """Elimina un repartidor del sistema
        
        Returns:
            int: 200 si se eliminó, 404 si no existe, 400 si hay error
        """
        try:
            repartidores = self.get_repartidores()
            updated = False
            
            with open(self.repartidores_csv, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['nombre', 'id', 'telefono', 'provincia', 'ubicacion_tiempo_real', 'vehiculo', 'estado', 'envios_asignados'])
                writer.writeheader()
                
                for repartidor in repartidores:
                    if repartidor['id'] != str(repartidor_id):
                        writer.writerow(repartidor)
                    else:
                        updated = True
            
            return 200 if updated else 404
        except:
            return 400

    # --- Métodos para gestión de furgonetas ---
    def add_furgoneta(self, matricula, capacidad_maxima, provincia, conductor):
        """Añade una furgoneta
        
        Returns:
            int: 201 si se creó, 409 si ya existe, 400 si hay error
        """
        try:
            for f in self.get_furgonetas():
                if f['matricula'] == matricula:
                    return 409
                    
            with open(self.furgonetas_csv, 'a', newline='') as f:
                csv.writer(f).writerow([matricula, str(capacidad_maxima), provincia, '0', conductor])
            return 201
        except:
            return 400
    
    def get_furgonetas(self):
        """Obtiene todas las furgonetas
        
        Returns:
            list: Furgonetas o [] si hay error
        """
        try:
            with open(self.furgonetas_csv, 'r') as f:
                return list(csv.DictReader(f))
        except:
            return []
        
    def asignar_conductor_furgoneta(self, matricula, conductor_id):
        """Asigna conductor a furgoneta
        
        Returns:
            int: 200 si se actualizó, 404 si no existe, 400 si hay error
        """
        try:
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
            return 200 if updated else 404
        except:
            return 400


    def delete_furgoneta(self, matricula):
        """Elimina una furgoneta del sistema
        
        Returns:
            int: 200 si se eliminó, 404 si no existe, 400 si hay error
        """
        try:
            furgonetas = self.get_furgonetas()
            updated = False
            
            with open(self.furgonetas_csv, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['matricula', 'capacidad_maxima', 'provincia', 'envios_asignados', 'conductor'])
                writer.writeheader()
                
                for furgoneta in furgonetas:
                    if furgoneta['matricula'] != matricula:
                        writer.writerow(furgoneta)
                    else:
                        updated = True
            
            return 200 if updated else 404
        except:
            return 400


