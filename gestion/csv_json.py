from abc import ABC, abstractmethod
import csv

class Archivo(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self):
        pass

class CSV(Archivo):
    def __init__(self, clase, list=[], ruta=None, sep=','):
        if ruta:
            self.ruta = ruta
        else:
            self.ruta = f'{clase}.csv'
        self.list = list
        self.sep = sep

    def read(self):
        with open(self.ruta, 'r') as file:
            i = 0
            for row in csv.reader(file):
                for value in row.split(self.sep):
                    self.list[i].append(value)
                    i += 1

    def write(self):
        with open(self.ruta, 'w') as file:
            writer = csv.writer(file)
            writer.writerows()

class JSON(Archivo):
    def __init__(self, clase, ruta):
        if ruta:
            self.ruta = ruta
        else:
            self.ruta = f'{clase}.json'