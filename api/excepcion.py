class Except(Exception):
    not_foud = 404
    bad_request = 400
    

    def data_not_found(self, info):
        return f'Error: {info}', self.not_foud
    
    def invalid_user(self, info):
        return f'Error: {info}', self.bad_request
    
    def invalid_password(self, info):
        return f'Error: {info}', self.bad_request
  
    
    


    
# Prueba de la clase Except
if __name__ == '__main__':
    try:
        raise Except('No se encontraron datos')
    
    except Except as e:
        print(e)
        print(e.data_not_found())
        