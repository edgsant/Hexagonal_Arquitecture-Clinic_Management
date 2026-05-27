import pytest
from datetime import date
from application.dtos.InformeDTOs import RegistrarInformeRequestDTO, InformeResponseDTO

def test_registrar_informe_request_valido(datos_informe_validos):
    """Verifica la instanciación correcta con datos válidos."""
    dto = RegistrarInformeRequestDTO(**datos_informe_validos)
    assert dto.procedimiento_id == "proc-999"
    assert dto.especialista_id == "esp-urologo-1"
    assert dto.antecedentes == "Paciente con historial previo de litiasis renal en 2022, tratado exitosamente."

def test_registrar_informe_request_falla_por_tipo_en_fecha(datos_informe_validos):
    """Debe lanzar TypeError si la fecha no es de tipo datetime.date."""
    datos_informe_validos["fecha"] = "2026-05-25"  # String en vez de date
    with pytest.raises(TypeError) as exc_info:
        RegistrarInformeRequestDTO(**datos_informe_validos)
    assert "El campo 'fecha' debe ser de tipo datetime.date" in str(exc_info.value)

def test_registrar_informe_request_falla_por_procedimiento_id_vacio(datos_informe_validos):
    """Debe lanzar ValueError si procedimiento_id está vacío."""
    datos_informe_validos["procedimiento_id"] = "   "
    with pytest.raises(ValueError) as exc_info:
        RegistrarInformeRequestDTO(**datos_informe_validos)
    assert "El campo 'procedimiento_id' no puede estar vacío" in str(exc_info.value)

def test_informe_response_dto_valido():
    """Comprueba que el DTO de respuesta se construya correctamente."""
    fecha = date(2026, 5, 25)
    dto = InformeResponseDTO(
        informe_id="inf-1",
        procedimiento_id="proc-999",
        fecha=fecha,
    )
    assert dto.informe_id == "inf-1"
    assert dto.procedimiento_id == "proc-999"
    assert dto.fecha == fecha