import uuid # Librería nativa de Python para generar IDs únicos
from domain.ports import IRepositorioPaciente
from domain.entities import EntityPaciente
from application.dtos.PacienteDTOs import RegistrarPacienteRequestDTO, PacienteResponseDTO

class ServicioRegistrarPaciente:
    """
    Caso de Uso: Registrar Paciente (CU02).
    Gestiona la creación de un nuevo paciente validando que no exista previamente.
    """

    def __init__(self, repo_paciente: IRepositorioPaciente):
        self._repo_paciente = repo_paciente

    def registrar_paciente(self, peticion: RegistrarPacienteRequestDTO) -> PacienteResponseDTO:
        # 1. Validación de campos obligatorios básicos
        if not peticion.dni:
            raise ValueError("El DNI es un campo obligatorio.")
            
        # 2. Regla de negocio / Infraestructura: Evitar duplicados
        if self._repo_paciente.obtener_por_dni(peticion.dni):
            raise ValueError(f"Ya existe un paciente registrado con el DNI: {peticion.dni}")
            
        # 3. Generación de identidad
        # Creamos un UUID v4 (estándar de la industria) y lo pasamos a string
        nuevo_id = str(uuid.uuid4())
            
        # 4. Instanciación de la entidad (El Dominio se autovalida al nacer)
        nuevo_paciente = EntityPaciente(
            id=nuevo_id,
            dni=peticion.dni,
            nombre=peticion.nombre,
            apellidos=peticion.apellidos,
            fecha_nacimiento=peticion.fecha_nacimiento,
            direccion=peticion.direccion,
            telefono=peticion.telefono
        )
        
        # 5. Persistencia a través del puerto
        self._repo_paciente.guardar_paciente(nuevo_paciente)
        
        # 6. Mapeo al DTO de salida para devolver a la web de forma segura
        return PacienteResponseDTO(
            id=nuevo_paciente.id,
            dni=nuevo_paciente.dni,
            nombre_completo=f"{nuevo_paciente.nombre} {nuevo_paciente.apellidos}",
            fecha_nacimiento=nuevo_paciente.fecha_nacimiento,
            direccion=nuevo_paciente.direccion,
            telefono=nuevo_paciente.telefono
        )