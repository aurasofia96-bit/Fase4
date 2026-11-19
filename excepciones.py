# Excepciones personalizadas
class ExcepcionBase(Exception):
    """Clase base para todas las excepciones personalizadas."""
    pass

class ErrorDatosBase(ExcepcionBase):
    """Se lanza cuando los datos de una entidad base no cumplen con las validaciones."""
    pass

class ErrorDatosCliente(ExcepcionBase):
    """Se lanza cuando los datos de un cliente no cumplen con las validaciones."""    
    pass

class ErrorDatosServicio(ExcepcionBase):
    """Se lanza cuando los datos de un servicio no cumplen con las validaciones."""
    pass