import pytest
from datetime import date
from application.dtos.PacienteDTOs import RegistrarPacienteRequestDTO, PacienteResponseDTO

def test_registrar_paciente_dto_valido(datos_paciente_request):
    """Verifica la instanciación correcta con datos válidos."""
    dto = RegistrarPacienteRequestDTO(**datos_paciente_request)
    assert dto.dni == "12345678A"
    assert dto.nombre == "Alejandro"
    assert dto.apellidos == "Sanz"

def test_registrar_paciente_dto_lanza_type_error(datos_paciente_request):
    """Debe lanzar TypeError si un tipo de dato es incorrecto."""
    datos_copia = datos_paciente_request.copy()
    datos_copia["nombre"] = 12345  # Tipo inválido
    with pytest.raises(TypeError) as exc_info:
        RegistrarPacienteRequestDTO(**datos_copia)
    assert "El campo 'nombre' debe ser un string" in str(exc_info.value)

def test_registrar_paciente_dto_lanza_type_error_fecha(datos_paciente_request):
    """Debe lanzar TypeError si fecha_nacimiento no es de tipo date."""
    datos_copia = datos_paciente_request.copy()
    datos_copia["fecha_nacimiento"] = "1985-10-12"  # String en vez de date
    with pytest.raises(TypeError) as exc_info:
        RegistrarPacienteRequestDTO(**datos_copia)
    assert "El campo 'fecha_nacimiento' debe ser de tipo datetime.date" in str(exc_info.value)

@pytest.mark.parametrize("dni_invalido", ["", " ", "   ", "\n"])
def test_registrar_paciente_dto_lanza_value_error_por_vacio(datos_paciente_request, dni_invalido):
    """Debe lanzar ValueError si un campo obligatorio queda vacío o con espacios."""
    datos_copia = datos_paciente_request.copy()
    datos_copia["dni"] = dni_invalido
    with pytest.raises(ValueError) as exc_info:
        RegistrarPacienteRequestDTO(**datos_copia)
    assert "El campo 'dni' no puede estar vacío" in str(exc_info.value)

def test_paciente_response_dto_valido(datos_paciente):
    """Comprueba que el DTO de salida se construya correctamente."""
    dto = PacienteResponseDTO(**datos_paciente)
    assert dto.id == "pac-456-uuid"
    assert dto.dni == "12345678A"
    assert dto.nombre == "Alejandro"
    assert dto.apellidos == "Sanz"
    assert dto.fecha_nacimiento == date(1985, 10, 12)

def test_paciente_response_dto_falla_si_id_vacio(datos_paciente):
    """Debe lanzar ValueError si id está vacío."""
    datos_copia = datos_paciente.copy()
    datos_copia["id"] = ""
    with pytest.raises(ValueError) as exc_info:
        PacienteResponseDTO(**datos_copia)
    assert "El campo 'id' debe ser un string válido" in str(exc_info.value)
