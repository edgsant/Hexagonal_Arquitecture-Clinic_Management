from dataclasses import dataclass

@dataclass(frozen=True)
class ProcedimientoResponseDTO:
    """DTO de salida con el resumen del procedimiento recién creado."""
    id_procedimiento: str
    estado: str
    paciente_id: str
    paciente_nombre_completo: str