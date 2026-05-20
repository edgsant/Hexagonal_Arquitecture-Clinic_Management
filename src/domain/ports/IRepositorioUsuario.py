from abc import ABC, abstractmethod
from domain.entities.usuario import Usuario

class IRepositorioUsuario(ABC):
    """Puerto de salida para recuperar usuarios."""
    
    @abstractmethod
    def guardar(self, usuario: Usuario) -> None:
        pass

    @abstractmethod
    def obtener_por_id(self, id: str) -> Usuario | None:
        pass

    @abstractmethod
    def obtener_por_correo(self, correo: str) -> Usuario | None:
        """Solo busca por el identificador único de negocio (email)."""
        pass