from abc import ABC, abstractmethod
from domain.entities.paciente import Paciente

class IRepositorioPaciente(ABC):
    """
    Puerto de salida para la persistencia de Pacientes.
    """
    
    @abstractmethod
    def guardar(self, paciente: Paciente) -> None:
        """Guarda un paciente nuevo o actualiza uno existente."""
        pass

    @abstractmethod
    def obtener_por_id(self, id: str) -> Paciente | None:
        """Recupera un paciente por su clave subrogada (UUID)."""
        pass

    @abstractmethod
    def obtener_por_dni(self, dni: str) -> Paciente | None:
        """Busca un paciente por su clave natural de negocio (DNI)."""
        pass