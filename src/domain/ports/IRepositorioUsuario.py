from abc import ABC, abstractmethod
from domain.entities.EntityUsuario import EntityUsuario

class IRepositorioUsuario(ABC):
    """Puerto de salida para recuperar usuarios."""
    
    @abstractmethod
    def obtener_por_email_o_username(self, identificador: str) -> EntityUsuario | None:
        """Solo busca por el identificador único de negocio (email o username)."""
        pass

    @abstractmethod
    def guardar_usuario(self, usuario: EntityUsuario) -> None:
        pass

    @abstractmethod
    def obtener_por_id(self, id: str) -> EntityUsuario | None:
        pass

    