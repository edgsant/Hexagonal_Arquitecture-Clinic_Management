import pytest
from application.dtos.ProcedimientoDTOs import ProcedimientoResponseDTO

def test_procedimiento_response_dto_valido():
    """Verifica que el DTO de respuesta se construya de forma correcta."""
    dto = ProcedimientoResponseDTO(
        id_procedimiento="proc-123",
        estado="ACTIVO",
        paciente_id="pac-456",
        paciente_nombre_completo="Hugo Adán"
    )
    assert dto.id_procedimiento == "proc-123"
    assert dto.estado == "ACTIVO"
    assert dto.paciente_id == "pac-456"
    assert dto.paciente_nombre_completo == "Hugo Adán"

@pytest.mark.parametrize("campo", ["id_procedimiento", "estado", "paciente_id", "paciente_nombre_completo"])
def test_procedimiento_response_dto_falla_si_un_campo_interno_viene_vacio(campo):
    """Verifica que se lance ValueError si algún campo obligatorio viene vacío."""
    datos = {
        "id_procedimiento": "proc-123",
        "estado": "ACTIVO",
        "paciente_id": "pac-456",
        "paciente_nombre_completo": "Hugo Adán"
    }
    datos[campo] = "   "  # Forzamos campo vacío con espacios
    
    with pytest.raises(ValueError):
        ProcedimientoResponseDTO(**datos)

def test_procedimiento_response_dto_falla_por_tipo_incorrecto():
    """Verifica que se lance TypeError si algún campo no es string."""
    with pytest.raises(ValueError):  # El validador del DTO lanza ValueError para valores no string
        ProcedimientoResponseDTO(
            id_procedimiento=123,  # Debe ser string
            estado="ACTIVO",
            paciente_id="pac-456",
            paciente_nombre_completo="Hugo Adán"
        )