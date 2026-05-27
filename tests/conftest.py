import pytest
from unittest.mock import Mock, MagicMock
from datetime import date
from werkzeug.security import generate_password_hash

# ============ DTOs Fixtures ============

@pytest.fixture
def datos_paciente_request():
    """Fixture para RegistrarPacienteRequestDTO (sin id)."""
    return {
        "dni": "12345678A",
        "nombre": "Alejandro",
        "apellidos": "Sanz",
        "fecha_nacimiento": date(1985, 10, 12),
        "direccion": "Calle de la Salud 4",
        "telefono": "611223344"
    }

@pytest.fixture
def datos_paciente():
    """Fixture para PacienteResponseDTO (con id)."""
    return {
        "id": "pac-456-uuid",
        "dni": "12345678A",
        "nombre": "Alejandro",
        "apellidos": "Sanz",
        "fecha_nacimiento": date(1985, 10, 12),
        "direccion": "Calle de la Salud 4",
        "telefono": "611223344"
    }

@pytest.fixture
def datos_informe_validos():
    """Fixture con el cuerpo clínico real y estructurado para registrar un informe."""
    return {
        "procedimiento_id": "proc-999",
        "especialista_id": "esp-urologo-1",
        "fecha": date(2026, 5, 25),
        "antecedentes": "Paciente con historial previo de litiasis renal en 2022, tratado exitosamente.",
        "sintomas": "Presenta dolor lumbar agudo irradiado a fosa ilíaca derecha acompañado de disuria.",
        "antecedentes_familiares": "Padre diagnosticado con hiperplasia benigna de próstata a los 60 años.",
        "exploracion_fisica": "Abdomen blando y depresible. Puñopercusión renal derecha francamente positiva."
    }

@pytest.fixture
def datos_analitica_validos():
    return {
        "procedimiento_id": "proc-999",
        "analitica_id": "an-888",
        "especialista_id": "esp-analista-1",
        "psa": "1.4 ng/mL",
        "leucocitos": "6.5 x10^3/µL",
        "hemoglobina": "14.2 g/dL",
        "hematocrito": "42.5 %",
        "plaquetas": "250 x10^3/µL",
        "creatinina": "0.9 mg/dL",
        "glucosa": "95 mg/dL",
        "colesterol": "185 mg/dL",
        "observaciones": "Todos los parámetros bioquímicos y hematológicos se encuentran estables y dentro del rango de normalidad médica."
    }

@pytest.fixture
def datos_analitica_response():
    return {
        "analitica_id": "an-888",
        "analista_id": "esp-analista-1",
        "pendiente": False,
        "psa": "1.4 ng/mL",
        "leucocitos": "6.5 x10^3/µL",
        "hemoglobina": "14.2 g/dL",
        "hematocrito": "42.5 %",
        "plaquetas": "250 x10^3/µL",
        "creatinina": "0.9 mg/dL",
        "glucosa": "95 mg/dL",
        "colesterol": "185 mg/dL",
        "observaciones": "Resultados validados y enviados a presentación."
    }

# ============ Domain Entities Mocks ============

@pytest.fixture
def paciente_mock():
    """Mock de EntityPaciente para tests de servicios."""
    from domain.entities.EntityPaciente import EntityPaciente
    paciente = MagicMock(spec=EntityPaciente)
    paciente.id = "pac-456-uuid"
    paciente.dni = "12345678A"
    paciente.nombre = "Alejandro"
    paciente.apellidos = "Sanz"
    paciente.fecha_nacimiento = date(1985, 10, 12)
    paciente.direccion = "Calle de la Salud 4"
    paciente.telefono = "611223344"
    return paciente

@pytest.fixture
def especialista_mock():
    """Mock de EntityEspecialista (médico/urólogo)."""
    from domain.entities.EntityEspecialista import EntityEspecialista
    especialista = MagicMock(spec=EntityEspecialista)
    especialista.id = "esp-urologo-1"
    especialista.nombre = "Dr. Juan"
    especialista.apellidos = "García"
    especialista.especialidad = "Urología"
    return especialista

@pytest.fixture
def usuario_mock(especialista_mock):
    """Mock de EntityUsuario con credenciales válidas."""
    from domain.entities.EntityUsuario import EntityUsuario
    usuario = MagicMock(spec=EntityUsuario)
    usuario.id = "user-uuid-1"
    usuario.email = "juan.garcia@clinica.es"
    usuario.username = "urologo_usuario"
    usuario.password_hash = generate_password_hash("PasswordSegura123")
    
    # Métodos del usuario
    usuario.validar_credenciales = MagicMock(return_value=True)
    usuario.obtener_datos = MagicMock(return_value=especialista_mock)
    
    return usuario

@pytest.fixture
def procedimiento_mock(paciente_mock):
    """Mock de EntityProcedimiento (expediente clínico activo)."""
    from domain.entities.EntityProcedimiento import EntityProcedimiento, EstadoProcedimiento
    procedimiento = MagicMock(spec=EntityProcedimiento)
    procedimiento.id = "proc-999"
    procedimiento.paciente = paciente_mock
    
    # Estado del procedimiento (Enum real)
    procedimiento.estado = EstadoProcedimiento.ACTIVO
    
    # Métodos del procedimiento
    procedimiento.obtener_pruebas_pendientes = MagicMock(return_value=[])
    procedimiento.vincular_informe = MagicMock()
    procedimiento.registrar_acto_clinico = MagicMock()
    procedimiento.finalizar = MagicMock()
    
    return procedimiento

@pytest.fixture
def analitica_mock():
    """Mock de EntityAnalitica (prueba dentro de un procedimiento)."""
    from domain.entities.EntityAnalitica import EntityAnalitica
    analitica = MagicMock(spec=EntityAnalitica)
    analitica.id = "an-888"
    analitica.pendiente = True
    analitica.psa = ""
    analitica.leucocitos = ""
    analitica.hemoglobina = ""
    analitica.hematocrito = ""
    analitica.plaquetas = ""
    analitica.creatinina = ""
    analitica.glucosa = ""
    analitica.colesterol = ""
    analitica.observaciones = ""
    
    # Método para registrar resultados
    def registrar_resultados_side_effect(**kwargs):
        analitica.psa = kwargs.get("psa", "")
        analitica.leucocitos = kwargs.get("leucocitos", "")
        analitica.hemoglobina = kwargs.get("hemoglobina", "")
        analitica.hematocrito = kwargs.get("hematocrito", "")
        analitica.plaquetas = kwargs.get("plaquetas", "")
        analitica.creatinina = kwargs.get("creatinina", "")
        analitica.glucosa = kwargs.get("glucosa", "")
        analitica.colesterol = kwargs.get("colesterol", "")
        analitica.observaciones = kwargs.get("observaciones", "")
        analitica.pendiente = False
    
    analitica.registrar_resultados = MagicMock(side_effect=registrar_resultados_side_effect)
    
    return analitica

# ============ Repository Mocks ============

@pytest.fixture
def repo_paciente_mock():
    """Mock de IRepositorioPaciente."""
    repo = MagicMock()
    repo.obtener_por_id = MagicMock(return_value=None)
    repo.obtener_por_dni = MagicMock(return_value=None)
    repo.guardar_paciente = MagicMock()
    return repo

@pytest.fixture
def repo_usuario_mock():
    """Mock de IRepositorioUsuario."""
    repo = MagicMock()
    repo.obtener_por_email_o_username = MagicMock(return_value=None)
    repo.obtener_por_especialista_id = MagicMock(return_value=None)
    return repo

@pytest.fixture
def repo_procedimiento_mock():
    """Mock de IRepositorioProcedimiento."""
    repo = MagicMock()
    repo.obtener_por_id = MagicMock(return_value=None)
    repo.obtener_activo_por_paciente = MagicMock(return_value=None)
    repo.obtener_procedimientos_por_paciente = MagicMock(return_value=[])
    repo.guardar_procedimiento = MagicMock()
    repo.guardar = MagicMock()
    return repo

# ============ Repository fixtures para tests de infraestructura ============

@pytest.fixture
def repo_paciente_mem():
    from infrastructure.persistence.RepositorioPacienteMem import RepositorioPacienteMem
    return RepositorioPacienteMem()

@pytest.fixture
def repo_usuario_mem():
    from infrastructure.persistence.RepositorioUsuarioMem import RepositorioUsuarioMem
    return RepositorioUsuarioMem()

@pytest.fixture
def repo_procedimiento_mem():
    from infrastructure.persistence.RepositorioProcedimientoMem import RepositorioProcedimientoMem
    return RepositorioProcedimientoMem()


# ============ Entity fixtures para tests de infraestructura ============

@pytest.fixture
def paciente_entity():
    from domain.entities.EntityPaciente import EntityPaciente
    return EntityPaciente(
        id="pac-456-uuid",
        dni="12345678A",
        fecha_nacimiento=date(1985, 10, 12),
        nombre="Alejandro",
        apellidos="Sanz",
        direccion="Calle de la Salud 4",
        telefono="611223344"
    )

@pytest.fixture
def especialista_entity():
    from domain.entities.EntityEspecialista import EntityEspecialista
    return EntityEspecialista(
        id="esp-1",
        nombre="Juan",
        apellidos="Garcia",
        dni="87654321B",
        fecha_nacimiento=date(1980, 3, 9),
        direccion="Calle Medico 19",
        telefono="611223345"
    )

@pytest.fixture
def usuario_entity(especialista_entity):
    from domain.entities.EntityUsuario import EntityUsuario
    return EntityUsuario(
        id="user-456-uuid",
        email="juan.garcia@clinica.es",
        username="juangarcia",
        password_hash=generate_password_hash("Password123"),
        especialista=especialista_entity
    )

@pytest.fixture
def procedimiento_factory(paciente_entity):
    from domain.entities.EntityProcedimiento import EntityProcedimiento, EstadoProcedimiento

    def factory(id: str):
        procedimiento = EntityProcedimiento(id=id, paciente=paciente_entity)
        procedimiento.id_paciente = paciente_entity.id
        procedimiento.activo = procedimiento.estado == EstadoProcedimiento.ACTIVO

        original_finalizar = procedimiento.finalizar
        def finalizar_y_actualizar():
            result = original_finalizar()
            procedimiento.activo = procedimiento.estado == EstadoProcedimiento.ACTIVO
            return result

        procedimiento.finalizar = finalizar_y_actualizar
        return procedimiento

    return factory


@pytest.fixture
def procedimiento_entity(procedimiento_factory):
    return procedimiento_factory("proc-999")
