import uuid
from domain.ports.IRepositorioPaciente import IRepositorioPaciente
from domain.ports.IRepositorioProcedimiento import IRepositorioProcedimiento
from domain.entities.EntityProcedimiento import EntityProcedimiento
from application.dtos.ProcedimientoDTOs import ProcedimientoResponseDTO

class ServicioCrearProcedimiento:
    """
    Caso de Uso: Crear Procedimiento (CU03).
    Abre un nuevo expediente para un paciente, garantizando que no haya otro activo.
    """

    def __init__(self, repo_paciente: IRepositorioPaciente, repo_procedimiento: IRepositorioProcedimiento):
        # Protegemos las dependencias
        self._repo_paciente = repo_paciente
        self._repo_procedimiento = repo_procedimiento

    def crear_procedimiento(self, id_paciente: str) -> ProcedimientoResponseDTO:
        # 1. Comprobamos que el paciente existe (Línea <<use>> Paciente)
        paciente = self._repo_paciente.obtener_por_id(id_paciente)
        if not paciente:
            raise ValueError(f"No existe ningún paciente con el ID: {id_paciente}")

        # 2. REGLA DE NEGOCIO: Validar que no haya un procedimiento activo 
        procedimiento_activo = self._repo_procedimiento.obtener_activo_por_paciente(id_paciente)
        if procedimiento_activo:
            raise ValueError("El paciente ya tiene un procedimiento clínico activo.")

        # 3. Generamos la nueva identidad para el procedimiento
        nuevo_id_procedimiento = str(uuid.uuid4())

        # 4. Instanciamos la entidad (Cumpliendo estrictamente su contrato DDD)
        # Le pasamos el ID nuevo y el objeto paciente completo que recuperamos en el paso 1
        nuevo_procedimiento = EntityProcedimiento(
            id=nuevo_id_procedimiento,
            paciente=paciente
        )

        # 5. Lo persistimos a través del puerto
        self._repo_procedimiento.guardar_procedimiento(nuevo_procedimiento)

        # 6. Mapeamos al DTO seguro para Flask
        return ProcedimientoResponseDTO(
            id_procedimiento=nuevo_procedimiento.id,
            estado=nuevo_procedimiento.estado.value, # Extraemos el string del Enum
            paciente_id=paciente.id,
            paciente_nombre_completo=f"{paciente.nombre} {paciente.apellidos}"
        )