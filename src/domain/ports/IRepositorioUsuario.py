from abc import ABC, abstractmethod
from domain.entities.usuario import Usuario

class IRepositorioUsuario(ABC):
    """Puerto de salida para recuperar usuarios."""
    
    @abstractmethod
    def obtenerPorEmailOUsername(self, identificador: str) -> Usuario | None:
        """Solo busca por el identificador único de negocio (email o username)."""
        pass

    @abstractmethod
    def guardarUsuario(self, usuario: Usuario) -> None:
        pass

    @abstractmethod
    def obtenerPorId(self, id: str) -> Usuario | None:
        pass

    