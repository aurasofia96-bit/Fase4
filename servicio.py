from abc import abstractmethod
from base import Base
from excepciones import ErrorDatosServicio
from logs import registrar_evento, registrar_error

# Clase abstracta Servicio
class Servicio(Base):
    def __init__(self, id, estado, nombre, descripcion, tarifa):
        super().__init__(id, estado)
        self.set_nombre(nombre)
        self.set_descripcion(descripcion)
        self.set_tarifa(tarifa)
        
    # --- MÉTODOS COMUNES HEREDADOS POR TODOS ---

    def set_estado(self, estado): # Se modifica para estados de servicios: disponible, no disponible.
        estado_minuscula = estado.lower()
        if estado_minuscula not in ["disponible", "no disponible"]:
            registrar_error(f"Error al establecer el estado: {estado}. Debe ser 'disponible' o 'no disponible'.")
            raise ErrorDatosServicio("El estado debe ser 'disponible' o 'no disponible'.")
        self._estado = estado_minuscula

    def cambiar_estado(self):
        if self._estado == "disponible":
            self.set_estado("no disponible")
        else:
            self.set_estado("disponible")
        registrar_evento(f"El estado del servicio ID {self._id} cambió exitosamente a: {self._estado}")

    def get_nombre(self):
        return self.__nombre

    def set_nombre(self, nombre):
        self.__nombre = self.set_texto(nombre, "nombre")

    def get_descripcion(self):
        return self.__descripcion
    
    def set_descripcion(self, descripcion):
        self.__descripcion = self.set_texto(descripcion, "descripcion")

    def get_tarifa(self):
        return self.__tarifa

    def set_tarifa(self, tarifa):
        try:
            tarifa_float = float(tarifa)
        except (ValueError, TypeError) as error:
            registrar_error(f"Error al establecer la tarifa: {tarifa}. Debe ser un número.")
            raise ErrorDatosServicio("La tarifa debe ser un número.") from error
        else:
            if tarifa_float <= 0:
                registrar_error(f"Error al establecer la tarifa: {tarifa}. Debe ser un número mayor a 0.")
                raise ErrorDatosServicio("La tarifa debe ser un número mayor a 0.")
            self.__tarifa = tarifa_float

    # --- MÉTODOS ABSTRACTOS QUE DEBEN IMPLEMENTAR LAS CLASES HIJAS ---
    @abstractmethod
    def calcular_costo(self, cantidad, descuento=0.0):
        pass

class Reserva_sala (Servicio):
    def __init__(self, id, estado, nombre, descripcion, tarifa, capacidad):
        super().__init__(id, estado, nombre, descripcion, tarifa)
        self.set_capacidad(capacidad)

    def set_capacidad(self, capacidad):
        if not isinstance(capacidad, int) or capacidad <= 0:
            registrar_error(f"Error al establecer la capacidad: {capacidad}. Debe ser un número entero positivo.")
            raise ErrorDatosServicio("La capacidad debe ser un número entero positivo.")
        self.__capacidad = capacidad

    def mostrar(self):
        print (f"ID: {self._id}, Estado: {self.get_estado()}, Nombre: {self.get_nombre()}, Descripción: {self.get_descripcion()}, Tarifa: {self.get_tarifa()}, Capacidad: {self.__capacidad}")
    
    def mostrar_estado(self):
        print (f"nombre: {self.get_nombre()}, Estado: {self.get_estado()}")

    def calcular_costo(self, cantidad, descuento=0.0): #Cantidad de horas y descuento en porcentaje (0.0 a 1.0)
        """Calcula el costo total del servicio considerando la cantidad y el descuento.
        cantidad: número de horas que se desea reservar.
        descuento: porcentaje de descuento a aplicar (0.0 a 1.0)."""
        try:
            descuento = float(descuento)
        except (ValueError, TypeError) as error:
            registrar_error(f"Error al calcular el costo: descuento {descuento}. Debe ser un número entre 0 y 1.")
            raise ErrorDatosServicio("El descuento debe ser un número entre 0 y 1.") from error
        else:
            if not (0 <= descuento <= 1):
                registrar_error(f"Error al calcular el costo: descuento {descuento}. Debe ser un número entre 0 y 1.")
                raise ErrorDatosServicio("El descuento debe ser un número entre 0 y 1.")
            elif not isinstance(cantidad, int) or cantidad <= 0:
                registrar_error(f"Error al calcular el costo: cantidad {cantidad}. Debe ser un número entero mayor a 0.")
                raise ErrorDatosServicio("La cantidad debe ser un número entero mayor a 0.")
            else:
                costo_base = self.get_tarifa() * cantidad
                costo_total = costo_base - (costo_base * descuento)
                registrar_evento(f"Se calculó el costo del servicio ID {self._id} con cantidad {cantidad} y descuento {descuento}, costo total: {costo_total}.")
                return costo_total

class Alquiler_equipo (Servicio):
    pass

class Asesoria (Servicio):
    pass
