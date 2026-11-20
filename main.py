from acciones import (
    crear_cliente,
    crear_sala,
    crear_equipo,
    crear_asesoria,
    crear_reserva,
    procesar_reserva,
    cancelar_reserva,
)
from logs import registrar_evento


def main():
    print("=== SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ ===\n")
    registrar_evento("=== Inicio de ejecución del sistema Software FJ ===")

    # Listas que guardaran los objetos
    clientes = []
    servicios = []
    reservas = []

    # ---------------------------------------------------------
    # Simulacion 1 (Válida): Registro de clientes válidos
    # ---------------------------------------------------------
    print("--- Simulación 1: Registro de clientes válidos ---")
    c1 = crear_cliente(1, "activo", "Ana", "Gómez", 3001234567, "ana.gomez@correo.com", clientes)
    c2 = crear_cliente(2, "inactivo", "Carlos", "Pérez", 3109876543, "carlos.perez@correo.com", clientes)
    print()

    # ---------------------------------------------------------
    # Simulacion 2 (Inválida): Registro de cliente con datos erróneos
    # ---------------------------------------------------------
    print("--- Simulación 2: Registro de cliente con celular y correo inválidos ---")
    crear_cliente(3, "activo", "Luis", "Torres", 12345, "correo_invalido", clientes)
    print()

    # ---------------------------------------------------------
    # Simulacion 3 (Válida): Creación de los 3 servicios especializados
    # ---------------------------------------------------------
    print("--- Simulación 3: Creación de servicios especializados ---")
    s_sala = crear_sala(101, "disponible", "Sala Ejecutiva", "Sala con proyector", 10, servicios, 1500.0)
    s_equipo = crear_equipo(102, "disponible", "Portátil Pro", "Equipo de alto rendimiento", servicios, 5000.0, 5)
    s_asesoria = crear_asesoria(103, "disponible", "Asesoría POO", "Revisión de arquitectura", servicios, 2500.0, 2)
    s_no_disp = crear_sala(104, "no disponible", "Sala Mantenimiento", "Cerrada temporalmente", 8, servicios, 1000.0)
    print()

    # ---------------------------------------------------------
    # Simulacion 4 (Inválida): Servicio con tarifa negativa
    # --------------------------------------------------------
    print("--- Simulación 4: Creación de sala con tarifa negativa ---")
    crear_sala(105, "disponible", "Sala Error", "Tarifa inválida", 5, servicios, tarifa=-500.0)
    print()

    # ---------------------------------------------------------
    # Simulacion 5 (Inválida): Equipo disponible con stock en 0
    # ---------------------------------------------------------
    print("--- Simulación 5: Alquiler de equipo disponible sin inventario ---")
    crear_equipo(106, "disponible", "Tablet", "Sin unidades disponibles", servicios, tarifa=3000.0, cantidad_equipos=0)
    print()

    # ---------------------------------------------------------
    # Simulacion 6 (Inválida): Asesoría con duración mayor a 3 horas
    # ---------------------------------------------------------
    print("--- Simulación 6: Asesoría con duración fuera de rango ---")
    crear_asesoria(107, "disponible", "Asesoría Extendida", "Supera límite permitido", servicios, tarifa=2000.0, duracion=5)
    print()

    # ---------------------------------------------------------
    # Simulacion 7 (Válida): Reserva y procesamiento de Sala (descuento + IVA)
    # ---------------------------------------------------------
    print("--- Simulación 7: Reserva exitosa de Sala (10% descuento, 19% impuesto) ---")
    r1 = crear_reserva(201, "pendiente", c1, s_sala, 3, reservas)
    procesar_reserva(r1, descuento=0.10, impuesto=0.19)
    print()

    # ---------------------------------------------------------
    # Simulacion 8 (Válida): Reserva y procesamiento de Alquiler de Equipos
    # ---------------------------------------------------------
    print("--- Simulación 8: Reserva exitosa de Alquiler de Equipos (parámetros opcionales) ---")
    r2 = crear_reserva(202, "pendiente", c1, s_equipo, 2, reservas)
    procesar_reserva(r2, cantidad_equipos=3)
    print()

    # ---------------------------------------------------------
    # Simulacion 9 (Válida): Reserva y procesamiento de Asesoría nivel 3
    # ---------------------------------------------------------
    print("--- Simulación 9: Reserva exitosa de Asesoría nivel 3 ---")
    r3 = crear_reserva(203, "pendiente", c1, s_asesoria, 2, reservas)
    procesar_reserva(r3, descuento=0.05, impuesto=0.19, nivel_asesoria=3)
    print()

    # ---------------------------------------------------------
    # Simulacion 10 (Inválida): Procesamiento fallido por cliente inactivo
    # ---------------------------------------------------------
    print("--- Simulación 10: Reserva fallida por cliente inactivo ---")
    r4 = crear_reserva(204, "pendiente", c2, s_sala, 2, reservas)
    procesar_reserva(r4)
    print()

    # ---------------------------------------------------------
    # Simulacion 11 (Inválida): Procesamiento fallido por servicio no disponible
    # ---------------------------------------------------------
    print("--- Simulación 11: Reserva fallida por servicio no disponible ---")
    r5 = crear_reserva(205, "pendiente", c1, s_no_disp, 1, reservas)
    procesar_reserva(r5)
    print()

    # ---------------------------------------------------------
    # Simulacion 12 (Inválida): Exceso de equipos + cancelación e intento de reproceso
    # ---------------------------------------------------------
    print("--- Simulación 12: Exceso de equipos y procesamiento de reserva cancelada ---")
    r6 = crear_reserva(206, "pendiente", c1, s_equipo, 2, reservas)
    procesar_reserva(r6, cantidad_equipos=20)  # Solo hay 5 disponibles

    r7 = crear_reserva(207, "pendiente", c1, s_asesoria, 1, reservas)
    cancelar_reserva(r7)
    procesar_reserva(r7)  # Falla porque ya está cancelada
    print()

    # Resumen final del sistema
    print("=== RESUMEN FINAL DEL SISTEMA ===")
    print(f"Clientes registrados: {len(clientes)}")
    print(f"Servicios registrados: {len(servicios)}")
    print(f"Reservas registradas: {len(reservas)}")
    registrar_evento("=== Fin de ejecución estable del sistema Software FJ ===")


if __name__ == "__main__":
    main()