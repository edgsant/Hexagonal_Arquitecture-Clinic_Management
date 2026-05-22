from dataclasses import dataclass

@dataclass(frozen=True)
class RegistrarResultadosRequestDTO:
    """DTO de entrada: Todos los datos que rellenará el Analista en su pantalla."""
    procedimiento_id: str
    analitica_id: str
    especialista_id: str # Extraído del token de sesión
    psa: str
    leucocitos: str
    hemoglobina: str
    hematocrito: str
    plaquetas: str
    creatinina: str
    glucosa: str
    colesterol: str
    observaciones: str

@dataclass(frozen=True)
class AnaliticaResponseDTO:
    """DTO de salida: Devuelve el estado actualizado de la analítica."""
    analitica_id: str
    analista_id: str
    pendiente: bool
    psa: str
    leucocitos: str
    hemoglobina: str
    hematocrito: str
    plaquetas: str
    creatinina: str
    glucosa: str
    colesterol: str
    observaciones: str