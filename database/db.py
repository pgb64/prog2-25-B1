import csv, bcrypt, os
from dotenv import load_dotenv
import pandas as pd


class DB:
    
    users = 'data/users.csv'
    personal = 'data/personal.csv'
    users_data = pd.read_csv(users)
    personal_data = pd.read_csv(personal)

    def restore(self):
        # Crear archivos si no existen
        with open(self.users, 'a+') as f: pass
        with open(self.personal, 'a+') as f: pass
        
        # Inicializar cabeceras
        for archivo, column in [
            (self.users, ['id','user','password','type']),
            (self.personal, ['id','fecha','dir','cp','ciudad','genero'])
        ]:
            with open(archivo, 'r+', newline='') as f:
                if not f.read(1):
                    csv.writer(f).writerow(column)

        print('CSVs restaurados.')



    def get_user_data(self, id):
        return self.users_data.loc[self.users_data['id'] == id].to_dict()
    
    def get_all_users_data(self):
        return self.users_data.to_dict(orient='records')
    
    def get_user_info(self, id):
        return self.personal_data.loc[self.personal_data['id'] == id].to_dict(orient='records') 
    
    def get_all_users_info(self):
        return self.personal_data.to_dict(orient='records')
    
    def get_user_data(self, user):
        for u in self.get_all_users_data():
            if u['user'] == user:
                return u

    # Mejorar lógica de aquí (clave primaria)
    def add_user(self, user, password, type):
        # Obtener el nuevo id como el máximo id + 1
        new_id = self.users_data['id'].max() + 1
        
        # Crear el nuevo usuario
        new_user = {
            'id': new_id,
            'user': user,
            'password': password,
            'type': type
        }

        # Agregar el nuevo usuario al DataFrame
        update = pd.DataFrame([new_user])
        self.users_data = pd.concat([self.users_data, update], ignore_index=True)
        update.to_csv(self.users, mode='a', header=False, index=False)


    @classmethod
    def get_all_usernames(cls):
        return [username for username in cls.users_data['user']]
    
    @classmethod
    def get_user_hash(cls, username):
        if username in cls.get_all_usernames(cls):
            return cls.get_user_data(username)['password']



class Security:
    
    @staticmethod
    def hash_password(password):
        KEY = Security.get_key().encode('utf-8')
        hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.hashpw(KEY, bcrypt.gensalt()))
        return hash.decode('utf-8')
    
    @staticmethod
    def verify_password(password, hash):
        return bcrypt.checkpw(password.encode(), hash.encode())
    

    



        




