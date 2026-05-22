from abc import ABC, abstractmethod
from domain.entities.EntityProcedimiento import EntityProcedimiento

class IRepositorioProcedimiento(ABC):
    """
    Puerto de salida (Hexagonal) para la persistencia de los Procedimientos.
    La infraestructura deberá implementar este contrato.
    """
    
    @abstractmethod
    def guardar_procedimiento(self, p: EntityProcedimiento) -> None:
        pass

    @abstractmethod
    def obtener_procedimiento_por_ID(self, id: str) -> EntityProcedimiento | None:
        pass

    @abstractmethod
    def obtener_activo_por_paciente(self, id_paciente: str) -> EntityProcedimiento | None:
        pass

    @abstractmethod
    def obtener_procedimientos_por_paciente(self, id_paciente: str) -> list[EntityProcedimiento]:
        pass

    @abstractmethod
    def obtener_procedimientos_activos(self) -> list[EntityProcedimiento]:
        pass