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
        estado = self.set_texto(estado, "estado")  # Validar que sea un texto no vacío
        estado = estado.lower()
        if estado not in ["disponible", "no disponible"]:
            registrar_error(f"Error al establecer el estado: {estado}. Debe ser 'disponible' o 'no disponible'.")
            raise ErrorDatosServicio("El estado debe ser 'disponible' o 'no disponible'.")
        super().set_estado(estado)

    def cambiar_estado(self):
        if self.get_estado() == "disponible":
            self.set_estado("no disponible")
        else:
            self.set_estado("disponible")
        registrar_evento(f"El estado del servicio ID {self.get_id()} cambió exitosamente a: {self.get_estado()}")

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

    def mostrar_estado(self):
        print(f"nombre: {self.get_nombre()}, Estado: {self.get_estado()}")

    # --- MÉTODOS ABSTRACTOS QUE DEBEN IMPLEMENTAR LAS CLASES HIJAS ---
    @abstractmethod
    def calcular_costo(self, cantidad, descuento=0.0):
        pass

class Reserva_sala (Servicio):
    def __init__(self, id, estado, nombre, descripcion, capacidad, tarifa=1000.0):
        super().__init__(id, estado, nombre, descripcion, tarifa)
        self.set_capacidad(capacidad)

    def get_capacidad(self):
        return self.__capacidad

    def set_capacidad(self, capacidad):
        if not isinstance(capacidad, int) or capacidad <= 0:
            registrar_error(f"Error al establecer la capacidad: {capacidad}. Debe ser un número entero positivo.")
            raise ErrorDatosServicio("La capacidad debe ser un número entero positivo.")
        self.__capacidad = capacidad

    def mostrar(self):
        print (f"ID: {self.get_id()}, Estado: {self.get_estado()}, Nombre: {self.get_nombre()}, Descripción: {self.get_descripcion()}, Tarifa: {self.get_tarifa()}, Capacidad: {self.get_capacidad()}")

    def calcular_costo(self, cantidad, descuento=0.0): #Cantidad de horas y descuento en porcentaje (0.0 a 1.0)
        """Calcula el costo total del servicio considerando la cantidad de horas, la capacidad de la sala y el descuento aplicado.
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
                costo_base = self.get_tarifa() * cantidad * self.get_capacidad()
                costo_total = costo_base - (costo_base * descuento)
                registrar_evento(f"Se calculó el costo del servicio ID {self.get_id()} con cantidad {cantidad}, la capacidad {self.get_capacidad()} y descuento {descuento}, costo total: {costo_total}.")
                return costo_total
        finally:
            registrar_evento(f"Se intentó calcular el costo del servicio ID {self.get_id()} con cantidad {cantidad}, la capacidad {self.get_capacidad()} y descuento {descuento}.")  

class Alquiler_equipo (Servicio):
    def __init__(self, id, estado, nombre, descripcion, tarifa=5000.0, cantidad_equipos=0):
        super().__init__(id, "no disponible", nombre, descripcion, tarifa)
        self.set_cantidad_equipos(cantidad_equipos)
        self.set_estado(estado)  # Establecer el estado después de establecer la cantidad de equipos

    def set_estado(self, estado): # Se modifica para que no se pueda establecer como "disponible" si la cantidad de equipos es 0.
        estado = self.set_texto(estado, "estado")  # Validar que sea un texto no vacío
        estado = estado.lower()
        if estado not in ["disponible", "no disponible"]:
            registrar_error(f"Error al establecer el estado: {estado}. Debe ser 'disponible' o 'no disponible'.")
            raise ErrorDatosServicio("El estado debe ser 'disponible' o 'no disponible'.")
        if estado == "disponible" and self.get_cantidad_equipos() == 0:
            self.set_estado("no disponible")  # Cambiar automáticamente a "no disponible"
            registrar_error(f"Error al establecer el estado: {estado}. No se puede establecer como 'disponible' si la cantidad de equipos es 0.")
            raise ErrorDatosServicio("No se puede establecer como 'disponible' si la cantidad de equipos es 0.")
        super().set_estado(estado)

    def get_cantidad_equipos(self):
        return self.__cantidad_equipos

    def cambiar_estado(self):
        if self.get_cantidad_equipos() == 0:
            self.set_estado("no disponible")
            registrar_evento(f"El estado del servicio ID {self.get_id()} fue cambiado a 'no disponible' porque la cantidad de equipos es 0.")
        else:
            super().cambiar_estado()

    def set_cantidad_equipos(self, cantidad_equipos):
        if not isinstance(cantidad_equipos, int) or cantidad_equipos < 0:
            registrar_error(f"Error al establecer la cantidad de equipos: {cantidad_equipos}. Debe ser un número entero mayor o igual a 0.")
            raise ErrorDatosServicio("La cantidad de equipos debe ser un número entero mayor o igual a 0.")
        if cantidad_equipos == 0:
            self.set_estado("no disponible")
        self.__cantidad_equipos = cantidad_equipos

    def mostrar(self):
        print (f"ID: {self.get_id()}, Estado: {self.get_estado()}, Nombre: {self.get_nombre()}, Descripción: {self.get_descripcion()}, Tarifa: {self.get_tarifa()}, Cantidad de equipos: {self.get_cantidad_equipos()}")

    def calcular_costo(self, cantidad, descuento=0.0, tiempo=1): #Cantidad de equipos, tiempo de alquiler en horas (número entero positivo) y descuento en porcentaje (0.0 a 1.0)
        """Calcula el costo total del servicio considerando la cantidad de equipos, la tarifa y el descuento aplicado.
        cantidad: número de equipos que se desea alquilar.
        tiempo: tiempo de alquiler en horas.
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
            elif not isinstance(tiempo, int) or tiempo <= 0:
                registrar_error(f"Error al calcular el costo: tiempo {tiempo}. Debe ser un número entero positivo mayor a 0.")
                raise ErrorDatosServicio("El tiempo de alquiler debe ser un número entero positivo mayor a 0.")
            elif cantidad > self.get_cantidad_equipos():
                registrar_error(f"Error al calcular el costo: cantidad {cantidad}. No hay suficientes equipos disponibles (disponibles: {self.get_cantidad_equipos()}).")
                raise ErrorDatosServicio(f"No hay suficientes equipos disponibles. Disponibles: {self.get_cantidad_equipos()}.")
            else:
                costo_base = self.get_tarifa() * cantidad * tiempo
                costo_total = costo_base - (costo_base * descuento)
                registrar_evento(f"Se calculó el costo del servicio ID {self.get_id()} con cantidad {cantidad}, tiempo {tiempo}, tarifa {self.get_tarifa()} y descuento {descuento}, costo total: {costo_total}.")
                return costo_total
        finally:
            registrar_evento(f"Se intentó calcular el costo del servicio ID {self.get_id()} con cantidad {cantidad}, tiempo {tiempo}, tarifa {self.get_tarifa()} y descuento {descuento}.")  

class Asesoria (Servicio):
    def __init__(self, id, estado, nombre, descripcion, tarifa=2000.0, duracion=1): #Duración en horas maximo 3 horas 
        super().__init__(id, estado, nombre, descripcion, tarifa)
        self.set_duracion(duracion)

    def get_duracion(self):
        return self.__duracion

    def set_duracion(self, duracion):
        if not isinstance(duracion, int) or duracion <= 0 or duracion > 3:
            registrar_error(f"Error al establecer la duración: {duracion}. Debe ser un número entero entre 1 y 3.")
            raise ErrorDatosServicio("La duración debe ser un número entero entre 1 y 3.")
        self.__duracion = duracion

    def mostrar(self):
        print (f"ID: {self.get_id()}, Estado: {self.get_estado()}, Nombre: {self.get_nombre()}, Descripción: {self.get_descripcion()}, Tarifa: {self.get_tarifa()}, Duración: {self.get_duracion()}")

    def calcular_costo(self, nivel, descuento=0.0): # nivel de asesoría (1-básico, 2-intermedio, 3-avanzado) y descuento en porcentaje (0.0 a 1.0)
        """Calcula el costo total del servicio considerando la cantidad de horas y el descuento aplicado.
        nivel: nivel de asesoría (1-básico, 2-intermedio, 3-avanzado).
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
            elif nivel not in [1, 2, 3]:
                registrar_error(f"Error al calcular el costo: nivel {nivel}. Debe ser 1, 2 o 3.")
                raise ErrorDatosServicio("El nivel debe ser 1, 2 o 3.")
            else:
                costo_base = self.get_tarifa() * self.get_duracion() + (nivel - 1) * 500  # Aumenta $500 por cada nivel adicional
                costo_total = costo_base - (costo_base * descuento)
                registrar_evento(f"Se calculó el costo del servicio ID {self.get_id()} con duración {self.get_duracion()}, tarifa {self.get_tarifa()}, nivel {nivel} y descuento {descuento}, costo total: {costo_total}.")
                return costo_total
        finally:
            registrar_evento(f"Se intentó calcular el costo del servicio ID {self.get_id()} con duración {self.get_duracion()}, tarifa {self.get_tarifa()}, nivel {nivel} y descuento {descuento}.") 