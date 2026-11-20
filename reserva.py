from base import Base
from cliente import Cliente
from servicio import Servicio, Reserva_sala, Alquiler_equipo, Asesoria
from excepciones import ErrorDatosReserva, ErrorDatosServicio
from logs import registrar_evento, registrar_error


class Reserva(Base):
    def __init__(self, id, estado, cliente, servicio, duracion):
        super().__init__(id, estado)
        self.set_cliente(cliente)
        self.set_servicio(servicio)
        self.set_duracion(duracion)
        self.__costo_total = 0.0
        registrar_evento(f"Reserva ID {self.get_id()} creada en estado '{self.get_estado()}'.")

    # --- validaciones ---

    def set_estado(self, estado):
        estado = self.set_texto(estado, "estado").strip().lower()
        if estado not in ["pendiente", "confirmada", "cancelada"]:
            registrar_error(f"Error al establecer el estado de reserva: {estado}.")
            raise ErrorDatosReserva("El estado debe ser 'pendiente', 'confirmada' o 'cancelada'.")
        super().set_estado(estado)

    def get_cliente(self):
        return self.__cliente

    def set_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            registrar_error(f"Error al asignar cliente en reserva ID {self.get_id()}: {cliente}.")
            raise ErrorDatosReserva("El cliente debe ser una instancia válida de Cliente.")
        self.__cliente = cliente

    def get_servicio(self):
        return self.__servicio

    def set_servicio(self, servicio):
        if not isinstance(servicio, Servicio):
            registrar_error(f"Error al asignar servicio en reserva ID {self.get_id()}: {servicio}.")
            raise ErrorDatosReserva("El servicio debe ser una instancia válida de Servicio.")
        self.__servicio = servicio

    def get_duracion(self):
        return self.__duracion

    def set_duracion(self, duracion):
        if isinstance(duracion, bool) or not isinstance(duracion, int) or duracion <= 0:
            registrar_error(f"Error al establecer duración en reserva ID {self.get_id()}: {duracion}.")
            raise ErrorDatosReserva("La duración debe ser un número entero mayor a 0.")
        self.__duracion = duracion

    def get_costo_total(self):
        return self.__costo_total

    # --- metodos de base ---

    def mostrar(self):
        print(f"""ID: {self.get_id()} \nEstado: {self.get_estado()} 
Cliente: {self.get_cliente().get_nombre()} {self.get_cliente().get_apellido()} 
Servicio: {self.get_servicio().get_nombre()} ({type(self.get_servicio()).__name__}) 
Duración: {self.get_duracion()}h \nCosto Total: ${self.get_costo_total()}""")

    def mostrar_estado(self):
        print(f"Estado de la reserva ID {self.get_id()}: {self.get_estado()}")

    def cambiar_estado(self):
        if self.get_estado() == "pendiente":
            self.confirmar()
        elif self.get_estado() == "confirmada":
            self.cancelar()
        else:
            registrar_error(f"No se puede cambiar el estado de la reserva ID {self.get_id()} porque ya está cancelada.")
            raise ErrorDatosReserva("No se puede cambiar el estado de una reserva cancelada.")

    # metodos adicionales ( confirmar, cancelar, procesar)

    def confirmar(self):
        if self.get_estado() != "pendiente":
            registrar_error(f"No se puede confirmar la reserva ID {self.get_id()}: estado actual '{self.get_estado()}'.")
            raise ErrorDatosReserva(f"Solo se pueden confirmar reservas pendientes (actual: '{self.get_estado()}').")
        if self.get_cliente().get_estado() != "activo":
            registrar_error(f"No se puede confirmar la reserva ID {self.get_id()}: cliente inactivo.")
            raise ErrorDatosReserva("No se puede confirmar la reserva porque el cliente está inactivo.")
        if self.get_servicio().get_estado() != "disponible":
            registrar_error(f"No se puede confirmar la reserva ID {self.get_id()}: servicio no disponible.")
            raise ErrorDatosReserva("No se puede confirmar la reserva porque el servicio no está disponible.")

        super().set_estado("confirmada")
        registrar_evento(f"Reserva ID {self.get_id()} confirmada exitosamente.")

    def cancelar(self):
        if self.get_estado() == "cancelada":
            registrar_error(f"La reserva ID {self.get_id()} ya se encuentra cancelada.")
            raise ErrorDatosReserva("La reserva ya está cancelada.")

        super().set_estado("cancelada")
        registrar_evento(f"Reserva ID {self.get_id()} cancelada exitosamente.")

    def procesar(self, descuento=0.0, impuesto=0.0, cantidad_equipos=1, nivel_asesoria=1):
        try:
            if isinstance(impuesto, bool):
                raise TypeError("El impuesto no puede ser un booleano.")
            impuesto = float(impuesto)
            if not (0 <= impuesto <= 1):
                raise ValueError("El impuesto debe estar entre 0 y 1.")
            if self.get_estado() == "pendiente":
                self.confirmar()
            elif self.get_estado() == "cancelada":
                raise ErrorDatosReserva("No se puede procesar una reserva cancelada.")

            servicio = self.get_servicio()

            # Llamada al calcular_costo según el servicio (delegando sus validaciones internas)
            if isinstance(servicio, Reserva_sala):
                subtotal = servicio.calcular_costo(self.get_duracion(), descuento=descuento)
            elif isinstance(servicio, Alquiler_equipo):
                subtotal = servicio.calcular_costo(cantidad_equipos, descuento=descuento, tiempo=self.get_duracion())
            elif isinstance(servicio, Asesoria):
                subtotal = servicio.calcular_costo(nivel_asesoria, descuento=descuento)
            else:
                raise ErrorDatosReserva("El tipo de servicio no se puede procesar.")

        except (ErrorDatosServicio, ErrorDatosReserva,ValueError, TypeError) as error:
            registrar_error(f"Error al procesar la reserva ID {self.get_id()}: {error}")
            raise ErrorDatosReserva(f"Fallo en el procesamiento de la reserva ID {self.get_id()}.") from error
        else:
            self.__costo_total = subtotal + (subtotal * impuesto)
            registrar_evento( f"""Reserva ID {self.get_id()} procesada con éxito. \nSubtotal: {subtotal:.2f}, 
Impuesto: {impuesto*100:.0f}%, Total: {self.__costo_total:.2f}.""")
            return self.__costo_total
        finally:
            registrar_evento(f"Finalizó el intento de procesamiento de la reserva ID {self.get_id()}.")
