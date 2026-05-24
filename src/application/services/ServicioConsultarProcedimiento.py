from domain.ports import IRepositorioProcedimiento
from domain.entities import EntityProcedimiento
from application.dtos.ProcedimientoDTOs import ProcedimientoResponseDTO

class ServicioConsultarProcedimiento:
    """
    Caso de Uso: Consultar Procedimiento (CU06 / RF04).
    Orquesta las consultas de los expedientes clínicos y su mapeo seguro a DTOs.
    """

    def __init__(self, repo_procedimiento: IRepositorioProcedimiento):
        # Protegemos la dependencia siguiendo el estándar del proyecto
        self._repo_procedimiento = repo_procedimiento

    def consultar_procedimiento(self, id_procedimiento: str) -> ProcedimientoResponseDTO:
        """Devuelve el detalle completo de un procedimiento por su ID (CU06)."""
        # 1. Búsqueda a través del puerto
        procedimiento = self._repo_procedimiento.obtener_por_id(id_procedimiento)
        if not procedimiento:
            raise ValueError(f"No se encontró ningún procedimiento clínico con el ID: {id_procedimiento}")

        # 2. Recuperamos la entidad paciente asociada para construir el DTO
        paciente = procedimiento.paciente

        # 3. Mapeamos al DTO seguro para la capa de presentación (Flask)
        return ProcedimientoResponseDTO(
            id_procedimiento=procedimiento.id,
            estado=procedimiento.estado.value,  # Extraemos el string del Enum (ACTIVO/FINALIZADO)
            paciente_id=paciente.id,
            paciente_nombre_completo=f"{paciente.nombre} {paciente.apellidos}"
        )

    def consultar_procedimientos_paciente(self, id_paciente: str) -> list[ProcedimientoResponseDTO]:
        """RF04: Permite consultar el historial completo de procedimientos de un paciente."""
        # 1. Recuperamos la lista de entidades
        procedimientos = self._repo_procedimiento.obtener_procedimientos_por_paciente(id_paciente)
        
        # 2. Transformamos la lista de entidades en una lista de DTOs limpios utilizando una list comprehension
        return [
            ProcedimientoResponseDTO(
                id_procedimiento=p.id,
                estado=p.estado.value,
                paciente_id=p.paciente.id,
                paciente_nombre_completo=f"{p.paciente.nombre} {p.paciente.apellidos}"
            )
            for p in procedimientos
        ]

    def consultar_procedimiento_activo_paciente(self, id_paciente: str) -> ProcedimientoResponseDTO:
        """Busca si el paciente tiene un tratamiento en curso actual."""
        # 1. Búsqueda del procedimiento activo
        procedimiento_activo = self._repo_procedimiento.obtener_activo_por_paciente(id_paciente)
        if not procedimiento_activo:
            raise ValueError(f"El paciente con ID {id_paciente} no tiene ningún procedimiento activo actualmente.")

        paciente = procedimiento_activo.paciente

        # 2. Mapeamos al DTO seguro
        return ProcedimientoResponseDTO(
            id_procedimiento=procedimiento_activo.id,
            estado=procedimiento_activo.estado.value,
            paciente_id=paciente.id,
            paciente_nombre_completo=f"{paciente.nombre} {paciente.apellidos}"
        )