# Excepciones personalizadas
class ExcepcionBase(Exception):
    """Clase base para todas las excepciones personalizadas."""
    pass

class ClienteInvalidoError(ExcepcionBase):
    """Se lanza cuando los datos de un cliente no cumplen con las validaciones."""    
    pass

