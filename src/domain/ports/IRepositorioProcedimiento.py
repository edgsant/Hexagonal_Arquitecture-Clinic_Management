from abc import ABC, abstractmethod
from domain.entities.procedimiento import Procedimiento

class IRepositorioProcedimiento(ABC):
    """
    Puerto de salida (Hexagonal) para la persistencia de los Procedimientos.
    La infraestructura deberá implementar este contrato.
    """
    
    @abstractmethod
    def guardarProcedimiento(self, p: Procedimiento) -> None:
        pass

    @abstractmethod
    def obtenerProcedimientoPorID(self, id: str) -> Procedimiento | None:
        pass

    @abstractmethod
    def obtenerActivoPorPaciente(self, idPaciente: str) -> Procedimiento | None:
        pass

    @abstractmethod
    def obtenerProcedimientosPorPaciente(self, idPaciente: str) -> list[Procedimiento]:
        pass

    @abstractmethod
    def obtenerProcedimientosActivos(self) -> list[Procedimiento]:
        pass