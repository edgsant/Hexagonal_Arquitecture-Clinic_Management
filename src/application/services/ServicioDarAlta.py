from domain.ports import IRepositorioProcedimiento
from domain.entities import EntityProcedimiento
from application.dtos.ProcedimientoDTOs import ProcedimientoResponseDTO

class ServicioDarAlta:
    """
    Caso de Uso: Dar de Alta / Finalizar Procedimiento (CU07).
    Orquesta la finalización de un expediente clínico delegando las reglas en el dominio.
    """

    def __init__(self, repo_procedimiento: IRepositorioProcedimiento):
        # Protegemos la dependencia siguiendo el estándar del proyecto
        self._repo_procedimiento = repo_procedimiento

    def finalizar_procedimiento(self, id_procedimiento: str) -> ProcedimientoResponseDTO:
        """CU07: Finaliza el procedimiento clínico (da de alta al paciente)."""
        
        procedimiento = self._repo_procedimiento.obtener_por_id(id_procedimiento)
        if not procedimiento:
            raise ValueError(f"No se encontró ningún procedimiento clínico con el ID: {id_procedimiento}")

        # 2. REGLA DE NEGOCIO: Delegamos en la entidad de dominio la mutación de estado y sus validaciones
        # (El dominio comprobará internamente contratos como que no esté ya FINALIZADO o que no tenga pruebas pendientes)
        try:
            procedimiento.finalizar() 
        except Exception as error:
            # Si el dominio deniega el alta, burbujeamos el error semántico hacia el adaptador (Blueprint)
            raise ValueError(str(error))

        # 3. Persistimos el estado actualizado del Aggregate Root utilizando el método correcto del puerto
        self._repo_procedimiento.guardar_procedimiento(procedimiento)

        # 4. Recuperamos el paciente asociado para estructurar el DTO de respuesta
        paciente = procedimiento.paciente

        # 5. Mapeamos al DTO seguro para Flask
        return ProcedimientoResponseDTO(
            id_procedimiento=procedimiento.id,
            estado=procedimiento.estado.value,  # Extraemos el string del Enum (que ahora será "FINALIZADO")
            paciente_id=paciente.id,
            paciente_nombre_completo=f"{paciente.nombre} {paciente.apellidos}"
        )