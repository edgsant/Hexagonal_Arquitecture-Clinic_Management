from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class RegistrarPacienteRequestDTO:
    """DTO de entrada: Lo que el usuario rellena en el formulario web."""
    dni: str
    nombre: str
    apellidos: str
    fecha_nacimiento: date
    direccion: str
    telefono: str

    def __post_init__(self):
        # 1. Comprobación de tipos estrictos
        if not isinstance(self.dni, str): raise TypeError("El campo 'dni' debe ser un string.")
        if not isinstance(self.nombre, str): raise TypeError("El campo 'nombre' debe ser un string.")
        if not isinstance(self.apellidos, str): raise TypeError("El campo 'apellidos' debe ser un string.")
        if not isinstance(self.fecha_nacimiento, date): raise TypeError("El campo 'fecha_nacimiento' debe ser de tipo datetime.date.")
        if not isinstance(self.direccion, str): raise TypeError("El campo 'direccion' debe ser un string.")
        if not isinstance(self.telefono, str): raise TypeError("El campo 'telefono' debe ser un string.")

        # 2. Comprobación de no nulos / no vacíos
        if not self.dni.strip(): raise ValueError("El campo 'dni' no puede estar vacío.")
        if not self.nombre.strip(): raise ValueError("El campo 'nombre' no puede estar vacío.")
        if not self.apellidos.strip(): raise ValueError("El campo 'apellidos' no puede estar vacío.")
        if not self.direccion.strip(): raise ValueError("El campo 'direccion' no puede estar vacío.")
        if not self.telefono.strip(): raise ValueError("El campo 'telefono' no puede estar vacío.")


@dataclass(frozen=True)
class PacienteResponseDTO:
    """DTO de salida: Lo que devolvemos a la web tras crearlo o consultarlo."""
    id: str
    dni: str
    nombre: str
    apellidos: str
    fecha_nacimiento: date
    direccion: str
    telefono: str

    def __post_init__(self):
        if not isinstance(self.id, str) or not self.id.strip(): raise ValueError("El campo 'id' debe ser un string válido.")
        if not isinstance(self.dni, str) or not self.dni.strip(): raise ValueError("El campo 'dni' debe ser un string válido.")
        if not isinstance(self.nombre, str) or not self.nombre.strip(): raise ValueError("El campo 'nombre' debe ser un string válido.")
        if not isinstance(self.apellidos, str) or not self.apellidos.strip(): raise ValueError("El campo 'apellidos' debe ser un string válido.")
        if not isinstance(self.fecha_nacimiento, date): raise TypeError("El campo 'fecha_nacimiento' debe ser de tipo datetime.date.")
        if not isinstance(self.direccion, str) or not self.direccion.strip(): raise ValueError("El campo 'direccion' debe ser un string válido.")
        if not isinstance(self.telefono, str) or not self.telefono.strip(): raise ValueError("El campo 'telefono' debe ser un string válido.")