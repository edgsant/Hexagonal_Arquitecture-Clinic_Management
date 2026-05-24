import pytest
from application.dtos.AuthDTOs import LoginRequestDTO, LoginResponseDTO

def test_login_request_dto_valido():
    """Verifica la instanciación correcta con datos válidos."""
    dto = LoginRequestDTO(identificador="urologo_usuario", password="PasswordSegura123")
    assert dto.identificador == "urologo_usuario"
    assert dto.password == "PasswordSegura123"

def test_login_request_falla_por_tipo_en_password():
    """Debe lanzar TypeError si password no es string."""
    with pytest.raises(TypeError) as exc_info:
        LoginRequestDTO(identificador="urologo_usuario", password=None)
    assert "El campo 'password' debe ser un string" in str(exc_info.value)

def test_login_request_falla_por_tipo_en_identificador():
    """Debe lanzar TypeError si identificador no es string."""
    with pytest.raises(TypeError) as exc_info:
        LoginRequestDTO(identificador=12345, password="PasswordSegura123")
    assert "El campo 'identificador' debe ser un string" in str(exc_info.value)

def test_login_request_falla_por_username_con_espacios():
    """Debe lanzar ValueError si identificador está vacío o contiene solo espacios."""
    with pytest.raises(ValueError) as exc_info:
        LoginRequestDTO(identificador="   ", password="PasswordSegura123")
    assert "El campo 'identificador' es obligatorio" in str(exc_info.value)

def test_login_request_falla_por_password_con_espacios():
    """Debe lanzar ValueError si password está vacío o contiene solo espacios."""
    with pytest.raises(ValueError) as exc_info:
        LoginRequestDTO(identificador="urologo_usuario", password="   ")
    assert "El campo 'password' es obligatorio" in str(exc_info.value)

def test_login_response_dto_valido():
    """Verifica la instanciación correcta del DTO de respuesta."""
    dto = LoginResponseDTO(
        usuario_id="uuid-1",
        especialista_id="uuid-4", 
        rol="Urologo"  
    )
    assert dto.usuario_id == "uuid-1"
    assert dto.especialista_id == "uuid-4"
    assert dto.rol == "Urologo"

def test_login_response_falla_por_usuario_id_vacio():
    """Debe lanzar ValueError si usuario_id está vacío."""
    with pytest.raises(ValueError) as exc_info:
        LoginResponseDTO(usuario_id="", especialista_id="uuid-4", rol="Urologo")
    assert "El campo 'usuario_id' debe ser un string válido" in str(exc_info.value)

def test_login_response_falla_por_especialista_id_no_string():
    """Debe lanzar ValueError si especialista_id no es string válido."""
    with pytest.raises(ValueError) as exc_info:
        LoginResponseDTO(usuario_id="uuid-1", especialista_id=None, rol="Urologo")
    assert "El campo 'especialista_id' debe ser un string válido" in str(exc_info.value)