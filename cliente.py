from base import Base
from excepciones import ErrorDatosCliente
from logs import registrar_evento, registrar_error

class Cliente(Base):
    def __init__(self,id,estado,nombre,apellido,celular, correo):
        super().__init__(id,estado)
        self.set_nombre(nombre)
        self.set_apellido(apellido)
        self.set_celular(celular)
        self.set_correo(correo)

    def set_estado(self, estado): # Se modifica para estados para clientes: activo, inactivo.
        estado = self.set_texto(estado, "estado")
        estado = estado.lower()
        if estado not in ["activo", "inactivo"]:
            registrar_error(f"Error al establecer el estado: {estado}. Debe ser 'activo' o 'inactivo'.")
            raise ErrorDatosCliente("El estado debe ser 'activo' o 'inactivo'.")
        super().set_estado(estado)

    def mostrar(self):
        print(f"ID: {self.get_id()}, Estado: {self.get_estado()}, Nombre: {self.get_nombre()}, Apellido: {self.get_apellido()}, Celular: {self.get_celular()}, Correo: {self.get_correo()}")

    def mostrar_estado(self):
        print(f"Estado del cliente {self.get_nombre()} {self.get_apellido()}: {self.get_estado()}")

    def cambiar_estado(self):
        if self.get_estado() == "activo":
            super().set_estado("inactivo")
        else:
            super().set_estado("activo")
        registrar_evento(f"El estado del cliente ID {self.get_id()} cambió exitosamente a: {self.get_estado()}")

    def get_nombre(self):
        return self.__nombre

    def set_nombre(self, nombre):
        self.__nombre = self.set_texto(nombre, "nombre")

    def get_apellido(self):
        return self.__apellido

    def set_apellido(self, apellido):
        self.__apellido = self.set_texto(apellido, "apellido")

    def get_celular(self):
        return self.__celular

    def set_celular(self, celular):
        if not isinstance(celular, int) or not str(celular).isdigit() or len(str(celular)) != 10:
            registrar_error(f"Error al establecer el celular: {celular}. Debe ser un número entero de 10 dígitos.")
            raise ErrorDatosCliente("El celular debe ser un número entero de 10 dígitos.")
        self.__celular = celular

    def get_correo(self):
        return self.__correo

    def set_correo(self, correo):
        correo = self.set_texto(correo, "correo")
        if "@" not in correo or "." not in correo:
            registrar_error(f"Error al establecer el correo: {correo}. Debe ser un correo electrónico válido.")
            raise ErrorDatosCliente("El correo debe ser un correo electrónico válido.")
        self.__correo = correo