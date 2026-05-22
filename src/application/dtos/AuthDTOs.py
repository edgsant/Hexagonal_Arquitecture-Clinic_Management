from dataclasses import dataclass

@dataclass(frozen=True)
class LoginRequestDTO:
    """DTO de entrada con los datos que envía Flask."""
    identificador: str
    password: str # En texto plano

@dataclass(frozen=True)
class LoginResponseDTO:
    """DTO de salida para generar el JWT."""
    usuario_id: str
    especialista_id: str
    rol: str