#Clase abstracta general que representa las entidades generales del sistema.
from abc import ABC, abstractmethod
from logs import registrar_evento, registrar_error
from excepciones import ErrorDatosBase

class base(ABC):
    def __init__(self,id,estado):
        # Usamos los setters desde la base para validar de una vez
        self.set_id(id)
        self.set_estado(estado)

    # --- MÉTODOS COMUNES HEREDADOS POR TODOS ---

    def get_id(self):
        return self._id

    def set_id(self, id):
        if not isinstance(id, int) or id <= 0:
            registrar_error(f"Error al establecer el ID: {id}. Debe ser un número entero positivo.")
            raise ErrorDatosBase("El ID debe ser un número entero positivo.")
        self._id = id

    def get_estado(self):
        return self._estado

    def set_estado(self, estado):
        if not isinstance(estado, str):
            registrar_error(f"Error al establecer el estado: {estado}. Debe ser una cadena de texto.")
            raise ErrorDatosBase("El estado debe ser una cadena de texto.")
        self._estado = estado

    # --- MÉTODOS ABSTRACTOS QUE DEBEN IMPLEMENTAR LAS CLASES HIJAS ---

    @abstractmethod
    def mostrar(self):
        pass
    @abstractmethod
    def cambiar_estado(self,estado):
        pass
    @abstractmethod
    def mostrar_estado(self):
        pass