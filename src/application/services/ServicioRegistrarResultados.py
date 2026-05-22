from domain.ports import IRepositorioProcedimiento, IRepositorioUsuario
from domain.entities import EntityAnalitica
from domain.entities.EntityProcedimiento import EstadoProcedimiento
from application.dtos.AnaliticaDTOs import RegistrarResultadosRequestDTO, AnaliticaResponseDTO

class ServicioRegistrarResultados:
    """
    Caso de Uso: Registrar Resultados Analítica (CU05).
    Encuentra la analítica pendiente y delega el registro de biomarcadores a la entidad.
    """
    def __init__(self, repo_procedimiento: IRepositorioProcedimiento, repo_usuario: IRepositorioUsuario):
        self._repo_procedimiento = repo_procedimiento
        self._repo_usuario = repo_usuario

    def registrar_resultados(self, peticion: RegistrarResultadosRequestDTO) -> AnaliticaResponseDTO:
        # 1. Recuperamos y validamos el Agregado
        procedimiento = self._repo_procedimiento.obtener_por_id(peticion.procedimiento_id)
        if not procedimiento:
            raise ValueError("Procedimiento no encontrado.")
            
        if procedimiento.estado != EstadoProcedimiento.ACTIVO:
            raise ValueError("No se puede modificar un procedimiento que ya está finalizado.")

        # 2. Recuperamos al Especialista (Analista Clínico)
        usuario = self._repo_usuario.obtener_por_especialista_id(peticion.especialista_id)
        if not usuario:
            raise ValueError("Especialista no autorizado o no encontrado.")
        analista = usuario.obtener_datos()

        # 3. Buscamos la analítica concreta dentro de las pruebas pendientes del procedimiento
        analitica_encontrada = None
        for prueba in procedimiento.obtener_pruebas_pendientes():
            # Comprobamos que sea una analítica y que el ID coincida
            if isinstance(prueba, EntityAnalitica) and prueba.id == peticion.analitica_id:
                analitica_encontrada = prueba
                break
                
        if not analitica_encontrada:
            raise ValueError("La analítica no existe en este procedimiento o ya fue completada.")

        # 4. MUTACIÓN: Usamos el método rico del Dominio (Puro DDD)
        # La entidad se encarga de asignar los campos y marcarse como completada
        analitica_encontrada.registrar_resultados(
            psa=peticion.psa,
            leucocitos=peticion.leucocitos,
            hemoglobina=peticion.hemoglobina,
            hematocrito=peticion.hematocrito,
            plaquetas=peticion.plaquetas,
            creatinina=peticion.creatinina,
            glucosa=peticion.glucosa,
            colesterol=peticion.colesterol,
            observaciones=peticion.observaciones,
            analista=analista
        )

        # 5. Guardamos el Agregado modificado
        self._repo_procedimiento.guardar(procedimiento)

        # 6. Devolvemos confirmación
        return AnaliticaResponseDTO(
            analitica_id=analitica_encontrada.id,
            analista_id=analista.id,
            pendiente=analitica_encontrada.pendiente,
            psa=analitica_encontrada.psa,
            leucocitos=analitica_encontrada.leucocitos,
            hemoglobina=analitica_encontrada.hemoglobina,
            hematocrito=analitica_encontrada.hematocrito,
            plaquetas=analitica_encontrada.plaquetas,
            creatinina=analitica_encontrada.creatinina,
            glucosa=analitica_encontrada.glucosa,
            colesterol=analitica_encontrada.colesterol,
            observaciones=analitica_encontrada.observaciones
        )