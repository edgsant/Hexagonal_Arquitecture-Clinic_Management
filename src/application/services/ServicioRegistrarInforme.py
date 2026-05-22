import uuid
from domain.ports import IRepositorioProcedimiento
from domain.ports.IRepositorioUsuario import IRepositorioUsuario # Necesario para sacar al Especialista
from domain.entities import (
    EntityInformeInicial, 
    EntityConsulta, 
    EntitySolicitud, 
    EntityAnalitica, 
)
from domain.entities.EntityProcedimiento import EstadoProcedimiento
from application.dtos.InformeDTOs import RegistrarInformeRequestDTO, InformeResponseDTO

class ServicioRegistrarInforme:
    """
    Caso de Uso: Registrar Informe Inicial (CU04).
    Orquesta la creación del informe, la consulta y la solicitud de analítica.
    """
    def __init__(self, repo_procedimiento: IRepositorioProcedimiento, repo_usuario: IRepositorioUsuario):
        self._repo_procedimiento = repo_procedimiento
        self._repo_usuario = repo_usuario

    def registrar_informe(self, peticion: RegistrarInformeRequestDTO) -> InformeResponseDTO:
        # 1. Recuperamos el Agregado (Procedimiento)
        procedimiento = self._repo_procedimiento.obtener_por_id(peticion.procedimiento_id)
        if not procedimiento:
            raise ValueError("Procedimiento no encontrado.")
            
        if procedimiento.estado != EstadoProcedimiento.ACTIVO:
            raise ValueError("No se pueden añadir informes a un procedimiento finalizado.")

        # 2. Recuperamos al Especialista (Autor)
        usuario = self._repo_usuario.obtener_por_especialista_id(peticion.especialista_id)
        if not usuario:
            raise ValueError("Especialista no autorizado o no encontrado.")
        autor = usuario.obtener_datos() # Obtenemos el EntityEspecialista real

        # 3. CREACIÓN DEL ÁRBOL DE ENTIDADES (Generamos UUIDs para todo)
        
        # A) El Informe Inicial
        nuevo_informe = EntityInformeInicial(
            id=str(uuid.uuid4()),
            fecha=peticion.fecha,
            antecedentes=peticion.antecedentes,
            sintomas=peticion.sintomas,
            antecedentes_familiares=peticion.antecedentes_familiares,
            exploracion_fisica=peticion.exploracion_fisica,
            autor=autor
        )

        # B) La Prueba (Analítica que nace pendiente por defecto)
        nueva_analitica = EntityAnalitica(
            id=str(uuid.uuid4()),
            fecha=peticion.fecha,
            especialistas=[autor] # El urólogo/médico que la pide
        )

        # C) La Solicitud (Apunta a la prueba creada)
        nueva_solicitud = EntitySolicitud(
            id=str(uuid.uuid4()),
            fecha_prevista=peticion.fecha, # O una fecha futura
            prueba=nueva_analitica
        )

        # D) La Consulta (Añadimos la solicitud dentro)
        nueva_consulta = EntityConsulta(
            id=str(uuid.uuid4()),
            fecha=peticion.fecha,
            especialistas=[autor]
        )
        nueva_consulta.registrar_solicitud(nueva_solicitud)

        # 4. MUTACIÓN DEL AGREGADO (Ensamblamos las piezas)
        procedimiento.vincular_informe(nuevo_informe)
        procedimiento.registrar_acto_clinico(nueva_consulta)
        procedimiento.registrar_acto_clinico(nueva_analitica)

        # 5. GUARDAMOS EL ESTADO GLOBAL
        self._repo_procedimiento.guardar(procedimiento)

        # 6. RETORNAMOS EL DTO DE ÉXITO
        return InformeResponseDTO(
            informe_id=nuevo_informe.id,
            procedimiento_id=procedimiento.id,
            fecha=nuevo_informe.fecha,
            mensaje="Informe, consulta y solicitud de analítica registrados correctamente."
        )