import pytest
from datetime import date

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