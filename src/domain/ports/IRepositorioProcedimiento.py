from abc import ABC, abstractmethod
from domain.entities.procedimiento import Procedimiento

class IRepositorioProcedimiento(ABC):
    """
    Puerto de salida (Hexagonal) para la persistencia de los Procedimientos.
    La infraestructura deberá implementar este contrato.
    """
    
    @abstractmethod
    def guardar(self, procedimiento: Procedimiento) -> None:
        pass

    @abstractmethod
    def obtener_por_id(self, id: str) -> Procedimiento | None:
        pass

    @abstractmethod
    def obtener_activo_por_paciente(self, paciente_id: str) -> Procedimiento | None:
        pass

    @abstractmethod
    def obtener_todos_por_paciente(self, paciente_id: str) -> list[Procedimiento]:
        pass

    @abstractmethod
    def obtener_todos_activos(self) -> list[Procedimiento]:
        pass