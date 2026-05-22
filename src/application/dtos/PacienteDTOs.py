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