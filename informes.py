import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class Informe:
    """
    Atributos
    ---------
    df: pd.DataFrame
                
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

    def get_data(self, v_ind: str, v_dep: str, df: pd.DataFrame | None = None):
        if df == None:
            df = self.df
        data_ind = []
        data_dep = []
        try:
            for i in df[v_ind]:
                data_ind.append(i)
            for i in df[v_dep]:
                data_dep.append(i)
        except KeyError as error:
            print(f'{error} is not a key in the given DataFrame')
        return data_dep, data_ind
    
    def grafico(self, v_ind: str, v_dep: str, tipo: str = 'barplot', df: pd.DataFrame | None = None):
        data_dep, data_ind = self.get_data(v_ind, v_dep, df)
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