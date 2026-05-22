from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class RegistrarInformeRequestDTO:
    """Lo que envía el Frontend (Flask/React)."""
    procedimiento_id: str
    especialista_id: str  # Extraído del JWT en Flask
    fecha: date
    antecedentes: str
    sintomas: str
    antecedentes_familiares: str
    exploracion_fisica: str

@dataclass(frozen=True)
class InformeResponseDTO:
    """Lo que devolvemos para confirmar la creación."""
    informe_id: str
    procedimiento_id: str
    fecha: date
    mensaje: str