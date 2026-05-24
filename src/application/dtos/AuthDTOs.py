from dataclasses import dataclass

@dataclass(frozen=True)
class LoginRequestDTO:
    """DTO de entrada con los datos que envía Flask."""
    identificador: str
    password: str # En texto plano

    def __post_init__(self):
        if not isinstance(self.identificador, str): raise TypeError("El campo 'identificador' debe ser un string.")
        if not isinstance(self.password, str): raise TypeError("El campo 'password' debe ser un string.")
        
        if not self.identificador.strip(): raise ValueError("El campo 'identificador' es obligatorio.")
        if not self.password.strip(): raise ValueError("El campo 'password' es obligatorio.")


@dataclass(frozen=True)
class LoginResponseDTO:
    """DTO de salida para generar el JWT."""
    usuario_id: str
    especialista_id: str
    rol: str

    def __post_init__(self):
        if not isinstance(self.usuario_id, str) or not self.usuario_id.strip():
            raise ValueError("El campo 'usuario_id' debe ser un string válido.")
        if not isinstance(self.especialista_id, str) or not self.especialista_id.strip():
            raise ValueError("El campo 'especialista_id' debe ser un string válido.")
        if not isinstance(self.rol, str) or not self.rol.strip():
            raise ValueError("El campo 'rol' debe ser un string válido.")