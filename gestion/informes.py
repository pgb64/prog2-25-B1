import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import csv_json as cj

class Informe:
    """
    Atributos
    ---------
    df: pd.DataFrame
        Conjunto ordenado de los datos de los cuales se quiere obtener estadísticas

    Métodos
    -------
    __init__()
        Construye una instancia con el DataFrame deseado

    get_data()
        Obtiene una lista con los valores pedidos

    grafico()
        Crea un grafico con los valores pedidos
    """
    def __init__(self, df):
        self.df = df

    def texto(self, valor1: str, valor2: str, df: pd.DataFrame | None = None):
        if df == None:
            df = self.df
        try:
            for i in df[valor1]:
                print(df[i][valor2])
        except KeyError as error:
            print(f'{error} is not a key in the given data')

    def get_data(self, valor: str, df: pd.DataFrame | None = None):
        if df == None:
            df = self.df
        try:
            data = df[valor].to_numpy().tolist()
        except KeyError as error:
            print(f'{error} is not a key in the given DataFrame')
        return data
    
    def grafico(self, v_ind: str, v_dep: str, tipo: str = 'barplot', df: pd.DataFrame | None = None, csv: str | None = None):
        if csv and not df:
            ccsv = cj.CSV(csv)
            df = ccsv.get_df()
        data_ind = self.get_data(v_ind, df)
        data_dep = self.get_data(v_dep, df)
        supported_types = ['plot', 'scatter', 'hist']
        if tipo in supported_types:
            if tipo == 'plot':
                plt.plot(data_ind, data_dep)
            if tipo == 'scatter':
                plt.scatter(data_ind, data_dep)
            if tipo == 'hist':
                plt.hist(data_ind, data_dep)
        else:
            print(f"Error: tipo debería de ser uno de los siguientes: {supported_types}")