from abc import ABC, abstractmethod
from domain.entities.EntityPaciente import EntityPaciente

class IRepositorioPaciente(ABC):
    """
    Puerto de salida para la persistencia de Pacientes.
    """
    
    @abstractmethod
    def guardar_paciente(self, paciente: EntityPaciente) -> None:
        """Guarda un paciente nuevo o actualiza uno existente."""
        pass

    @abstractmethod
    def obtener_por_id(self, id: str) -> EntityPaciente | None:
        """Recupera un paciente por su clave subrogada (UUID)."""
        pass

    @abstractmethod
    def obtener_por_dni(self, dni: str) -> EntityPaciente | None:
        """Busca un paciente por su clave natural de negocio (DNI)."""
        pass