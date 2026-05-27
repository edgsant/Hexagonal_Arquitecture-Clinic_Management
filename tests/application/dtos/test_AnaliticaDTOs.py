import pytest
from application.dtos.AnaliticaDTOs import RegistrarResultadosRequestDTO, AnaliticaResponseDTO

def test_registrar_resultados_request_valido(datos_analitica_validos):
    """Verifica la instanciación correcta con datos válidos."""
    dto = RegistrarResultadosRequestDTO(**datos_analitica_validos)
    assert dto.leucocitos == "6.5 x10^3/µL"
    assert dto.psa == "1.4 ng/mL"
    assert dto.procedimiento_id == "proc-999"

def test_registrar_resultados_falla_si_psa_no_es_str(datos_analitica_validos):
    """Debe lanzar TypeError si psa no es string."""
    datos_analitica_validos["psa"] = 1.4  # Float erróneo
    with pytest.raises(TypeError):
        RegistrarResultadosRequestDTO(**datos_analitica_validos)

def test_registrar_resultados_falla_si_procedimiento_id_esta_vacio(datos_analitica_validos):
    """Debe lanzar ValueError si procedimiento_id está vacío."""
    datos_analitica_validos["procedimiento_id"] = ""
    with pytest.raises(ValueError):
        RegistrarResultadosRequestDTO(**datos_analitica_validos)

def test_registrar_resultados_falla_si_analitica_id_esta_vacio(datos_analitica_validos):
    """Debe lanzar ValueError si analitica_id está vacío."""
    datos_analitica_validos["analitica_id"] = ""
    with pytest.raises(ValueError):
        RegistrarResultadosRequestDTO(**datos_analitica_validos)

def test_analitica_response_dto_valido(datos_analitica_response):
    """Verifica la instanciación correcta de AnaliticaResponseDTO."""
    dto = AnaliticaResponseDTO(**datos_analitica_response)
    assert dto.analitica_id == "an-888"
    assert dto.pendiente is False
    assert dto.psa == "1.4 ng/mL"