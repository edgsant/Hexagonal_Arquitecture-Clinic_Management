from abc import ABC, abstractmethod
from domain.entities.paciente import Paciente

class IRepositorioPaciente(ABC):
    """
    Puerto de salida para la persistencia de Pacientes.
    """
    
    @abstractmethod
    def guardarPaciente(self, paciente: Paciente) -> None:
        """Guarda un paciente nuevo o actualiza uno existente."""
        pass

    @abstractmethod
    def obtenerPorID(self, id: str) -> Paciente | None:
        """Recupera un paciente por su clave subrogada (UUID)."""
        pass

    @abstractmethod
    def obtenerPorDNI(self, dni: str) -> Paciente | None:
        """Busca un paciente por su clave natural de negocio (DNI)."""
        pass