#Clase abstracta general que representa las entidades generales del sistema.
from abc import ABC, abstractmethod
class base(ABC):
    def __init__(self,id,estado):
        self.id = id
        self.estado = estado
        
    @abstractmethod
    def mostrar(self):
        pass
    @abstractmethod
    def cambiar_estado(self,estado):
        pass
    @abstractmethod
    def mostrar_estado(self):
        pass