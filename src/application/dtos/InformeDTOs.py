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

    def __post_init__(self):
        # Tipos
        if not isinstance(self.procedimiento_id, str): raise TypeError("El campo 'procedimiento_id' debe ser un string.")
        if not isinstance(self.especialista_id, str): raise TypeError("El campo 'especialista_id' debe ser un string.")
        if not isinstance(self.fecha, date): raise TypeError("El campo 'fecha' debe ser de tipo datetime.date.")
        if not isinstance(self.antecedentes, str): raise TypeError("El campo 'antecedentes' debe ser un string.")
        if not isinstance(self.sintomas, str): raise TypeError("El campo 'sintomas' debe ser un string.")
        if not isinstance(self.antecedentes_familiares, str): raise TypeError("El campo 'antecedentes_familiares' debe ser un string.")
        if not isinstance(self.exploracion_fisica, str): raise TypeError("El campo 'exploracion_fisica' debe ser un string.")

        # No nulos
        if not self.procedimiento_id.strip(): raise ValueError("El campo 'procedimiento_id' no puede estar vacío.")
        if not self.especialista_id.strip(): raise ValueError("El campo 'especialista_id' no puede estar vacío.")
        # Nota: Los campos de texto clínicos opcionales pueden estar vacíos en el formulario web, 
        # pero deben ser strings (ej. "" si el paciente no tiene antecedentes). No se lanza ValueError si están vacíos.


@dataclass(frozen=True)
class InformeResponseDTO:
    """Lo que devolvemos para confirmar la creación."""
    informe_id: str
    procedimiento_id: str
    fecha: date
    mensaje: str

    def __post_init__(self):
        if not isinstance(self.informe_id, str) or not self.informe_id.strip():
            raise ValueError("El campo 'informe_id' debe ser un string válido.")
        if not isinstance(self.procedimiento_id, str) or not self.procedimiento_id.strip():
            raise ValueError("El campo 'procedimiento_id' debe ser un string válido.")
        if not isinstance(self.fecha, date):
            raise TypeError("El campo 'fecha' debe ser de tipo datetime.date.")
        if not isinstance(self.mensaje, str) or not self.mensaje.strip():
            raise ValueError("El campo 'mensaje' debe ser un string válido.")