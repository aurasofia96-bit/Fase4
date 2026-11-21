# Sistema Integral de Gestión de Clientes, Servicios y Reservas – Software FJ

Proyecto desarrollado para el **Componente Práctico – Fase 4** del curso **Programación (213023)** de la Universidad Nacional Abierta y a Distancia (**UNAD**).

## Descripción General

Aplicación orientada a objetos desarrollada en **Python** (sin motor de base de datos) para gestionar clientes, servicios especializados y reservas de la empresa **Software FJ**. El sistema garantiza estabilidad y tolerancia a fallos mediante excepciones personalizadas, bloques `try / except / else / finally`, encadenamiento de excepciones (`raise ... from error`) y registro de bitácora en `logs/sistema.log`.

## Estructura del Proyecto

| Módulo | Descripción |
| :--- | :--- |
| `base.py` | Clase abstracta `Base` (`ABC`) con validaciones generales, encapsulación y métodos abstractos (`mostrar`, `mostrar_estado`, `cambiar_estado`). |
| `cliente.py` | Clase `Cliente` heredada de `Base` con validación de estado, celular de 10 dígitos y correo electrónico. |
| `servicio.py` | Clase abstracta `Servicio` y tres servicios especializados (`Reserva_sala`, `Alquiler_equipo`, `Asesoria`) con polimorfismo y cálculo de costos parametrizado. |
| `reserva.py` | Clase `Reserva` que integra cliente, servicio y duración; implementa `confirmar()`, `cancelar()` y `procesar()` con encadenamiento de excepciones. |
| `excepciones.py` | Jerarquía de excepciones personalizadas (`ExcepcionBase`, `ErrorDatosBase`, `ErrorDatosCliente`, `ErrorDatosServicio`, `ErrorDatosReserva`). |
| `logs.py` | Configuración del módulo `logging` para registrar eventos (`INFO`) y errores controlados (`ERROR`) en `logs/sistema.log`. |
| `acciones.py` | Funciones auxiliares de negocio para crear y gestionar clientes, servicios y reservas de manera controlada. |
| `main.py` | Punto de entrada que ejecuta **12 simulaciones completas** (válidas e inválidas) sin detenerse ante errores. |

## Requisitos y Ejecución

- **Requisitos:** Python 3.10 o superior (solo utiliza librerías estándar: `abc`, `logging`, `os`).
- **Ejecución:**

```bash
python main.py
