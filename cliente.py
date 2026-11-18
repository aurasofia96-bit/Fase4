from base import base
from excepciones import ErrorDatosCliente
from logs import registrar_evento, registrar_error

class cliente(base):
    def __init__(self,id,estado,nombre,apellido,celular, correo):
        super().__init__(id,estado)
        self.set_nombre(nombre)
        self.set_apellido(apellido)
        self.set_celular(celular)
        self.set_correo(correo)

    def set_estado(self, estado): # Se modifica para estados para clientes: activo, inactivo.
        estado_minuscula = estado.lower()
        if estado_minuscula not in ["activo", "inactivo"]:
            registrar_error(f"Error al establecer el estado: {estado}. Debe ser 'activo' o 'inactivo'.")
            raise ErrorDatosCliente("El estado debe ser 'activo' o 'inactivo'.")
        self._estado = estado_minuscula

    def mostrar(self):
        print(f"ID: {self._id}, Estado: {self._estado}, Nombre: {self.__nombre}, Apellido: {self.__apellido}, Celular: {self.__celular}, Correo: {self.__correo}")

    def mostrar_estado(self):
        print(f"Estado del cliente {self.__nombre} {self.__apellido}: {self._estado}")

    def cambiar_estado(self):
        if self._estado == "activo":
            self.set_estado("inactivo")
        else:
            self.set_estado("activo")
        registrar_evento(f"El estado del cliente ID {self._id} cambió exitosamente a: {self._estado}")

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
        if "@" not in correo or "." not in correo:
            registrar_error(f"Error al establecer el correo: {correo}. Debe ser un correo electrónico válido.")
            raise ErrorDatosCliente("El correo debe ser un correo electrónico válido.")
        self.__correo = correo