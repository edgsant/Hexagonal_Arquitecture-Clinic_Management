from dataclasses import dataclass

@dataclass(frozen=True)
class ProcedimientoResponseDTO:
    """DTO de salida con el resumen del procedimiento recién creado o consultado."""
    id_procedimiento: str
    estado: str
    paciente_id: str
    paciente_nombre_completo: str

    def __post_init__(self):
        if not isinstance(self.id_procedimiento, str) or not self.id_procedimiento.strip():
            raise ValueError("El campo 'id_procedimiento' debe ser un string válido.")
        if not isinstance(self.estado, str) or not self.estado.strip():
            raise ValueError("El campo 'estado' debe ser un string válido.")
        if not isinstance(self.paciente_id, str) or not self.paciente_id.strip():
            raise ValueError("El campo 'paciente_id' debe ser un string válido.")
        if not isinstance(self.paciente_nombre_completo, str) or not self.paciente_nombre_completo.strip():
            raise ValueError("El campo 'paciente_nombre_completo' debe ser un string válido.")