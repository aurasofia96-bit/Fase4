from cliente import Cliente
from servicio import Reserva_sala, Alquiler_equipo, Asesoria
from reserva import Reserva
from excepciones import ExcepcionBase, ErrorDatosBase, ErrorDatosCliente,ErrorDatosServicio, ErrorDatosReserva
from logs import registrar_evento, registrar_error

# acciones para crear clientes ---------------------

def crear_cliente(id, estado, nombre, apellido, celular, correo, clientes):
    try:
        cliente_nuevo = Cliente(id, estado, nombre, apellido, celular, correo)
    except (ErrorDatosCliente, ExcepcionBase) as error:
        print(f"Error al crear cliente: {error}")
        registrar_error(f"Error al crear cliente ID {id}: {error}")
        return None
    else:
        clientes.append(cliente_nuevo)
        cliente_nuevo.mostrar()
        registrar_evento(f"Cliente ID {cliente_nuevo.get_id()} registrado correctamente.")
        return cliente_nuevo


# acciones para crear servicios ----------------------------

def crear_sala(id, estado, nombre, descripcion, capacidad, servicios, tarifa=1000.0):
    try:
        sala_nueva = Reserva_sala(id, estado, nombre, descripcion, capacidad, tarifa)
    except (ErrorDatosServicio, ExcepcionBase) as error:
        print(f"Error al crear sala: {error}")
        registrar_error(f"Error al crear Reserva_sala ID {id}: {error}")
        return None
    else:
        servicios.append(sala_nueva)
        sala_nueva.mostrar()
        registrar_evento(f"Servicio Reserva_sala ID {sala_nueva.get_id()} registrado correctamente.")
        return sala_nueva


def crear_equipo(id, estado, nombre, descripcion, servicios, tarifa=5000.0, cantidad_equipos=0):
    try:
        equipo_nuevo = Alquiler_equipo(id, estado, nombre, descripcion, tarifa, cantidad_equipos)
    except (ErrorDatosServicio, ExcepcionBase) as error:
        print(f"Error al crear alquiler de equipo: {error}")
        registrar_error(f"Error al crear Alquiler_equipo ID {id}: {error}")
        return None
    else:
        servicios.append(equipo_nuevo)
        equipo_nuevo.mostrar()
        registrar_evento(f"Servicio Alquiler_equipo ID {equipo_nuevo.get_id()} registrado correctamente.")
        return equipo_nuevo


def crear_asesoria(id, estado, nombre, descripcion, servicios, tarifa=2000.0, duracion=1):
    try:
        asesoria_nueva = Asesoria(id, estado, nombre, descripcion, tarifa, duracion)
    except (ErrorDatosServicio, ExcepcionBase) as error:
        print(f"Error al crear asesoría: {error}")
        registrar_error(f"Error al crear Asesoria ID {id}: {error}")
        return None
    else:
        servicios.append(asesoria_nueva)
        asesoria_nueva.mostrar()
        registrar_evento(f"Servicio Asesoria ID {asesoria_nueva.get_id()} registrado correctamente.")
        return asesoria_nueva


# acciones de reserva -------------------------------------

def crear_reserva(id, estado, cliente, servicio, duracion, reservas):
    try:
        reserva_nueva = Reserva(id, estado, cliente, servicio, duracion)
    except (ErrorDatosReserva, ExcepcionBase) as error:
        print(f"Error al crear reserva: {error}")
        registrar_error(f"Error al crear Reserva ID {id}: {error}")
        return None
    else:
        reservas.append(reserva_nueva)
        reserva_nueva.mostrar()
        registrar_evento(f"Reserva ID {reserva_nueva.get_id()} registrada correctamente.")
        return reserva_nueva


def procesar_reserva(reserva, descuento=0.0, impuesto=0.0, cantidad_equipos=1, nivel_asesoria=1):
    if reserva is None:
        print("Error: no se puede procesar una reserva inexistente.")
        registrar_error("Intento de procesar una reserva None.")
        return None
    try:
        total = reserva.procesar(descuento=descuento, impuesto=impuesto, cantidad_equipos=cantidad_equipos, nivel_asesoria=nivel_asesoria)
    except (ErrorDatosReserva, ExcepcionBase) as error:
        print(f"Error al procesar reserva: {error}")
        if error.__cause__:
            print(f" Causa: {error.__cause__}")
        return None
    else:
        reserva.mostrar()
        print(f"Total cobrado: ${total:.2f}")
        return total


def cancelar_reserva(reserva):
    if reserva is None:
        print("Error controlado: no se puede cancelar una reserva inexistente.")
        registrar_error("Intento de cancelar una reserva None.")
        return False
    try:
        reserva.cancelar()
    except (ErrorDatosReserva, ExcepcionBase) as error:
        print(f"Error controlado al cancelar reserva: {error}")
        return False
    else:
        reserva.mostrar_estado()
        return True