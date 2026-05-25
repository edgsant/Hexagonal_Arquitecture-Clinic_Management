import pytest
from unittest.mock import MagicMock
from application.dtos.AuthDTOs import LoginRequestDTO
from application.services.ServicioIniciarSesion import ServicioIniciarSesion


class TestServicioIniciarSesion:
    """Tests para el servicio de inicio de sesión (CU01)."""

    def test_login_exitoso(self, repo_usuario_mock, usuario_mock, especialista_mock):
        """Debe loguearse exitosamente con credenciales válidas."""
        # Arrange
        usuario_mock.obtener_datos = MagicMock(return_value=especialista_mock)
        repo_usuario_mock.obtener_por_email_o_username.return_value = usuario_mock
        
        servicio = ServicioIniciarSesion(repo_usuario_mock)
        peticion = LoginRequestDTO(identificador="urologo_usuario", password="PasswordSegura123")

        # Act
        respuesta = servicio.login(peticion)

        # Assert
        assert respuesta.usuario_id == "user-uuid-1"
        assert respuesta.especialista_id == "esp-urologo-1"
        assert respuesta.rol is not None  # El rol se extrae del nombre de la clase del especialista
        repo_usuario_mock.obtener_por_email_o_username.assert_called_with("urologo_usuario")

    def test_login_falla_usuario_no_existe(self, repo_usuario_mock):
        """Debe lanzar ValueError si el usuario no existe."""
        # Arrange
        repo_usuario_mock.obtener_por_email_o_username.return_value = None
        
        servicio = ServicioIniciarSesion(repo_usuario_mock)
        peticion = LoginRequestDTO(identificador="usuario_inexistente", password="cualquier_pass")

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            servicio.login(peticion)
        
        assert "Credenciales incorrectas" in str(exc_info.value)

    def test_login_falla_password_invalida(self, repo_usuario_mock, usuario_mock):
        """Debe lanzar ValueError si la contraseña es incorrecta."""
        # Arrange
        usuario_mock.validar_credenciales.return_value = False
        repo_usuario_mock.obtener_por_email_o_username.return_value = usuario_mock
        
        servicio = ServicioIniciarSesion(repo_usuario_mock)
        peticion = LoginRequestDTO(identificador="urologo_usuario", password="PasswordIncorrecto")

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            servicio.login(peticion)
        
        assert "Credenciales incorrectas" in str(exc_info.value)
        usuario_mock.validar_credenciales.assert_called_with("PasswordIncorrecto")

    def test_login_busca_por_email_o_username(self, repo_usuario_mock, usuario_mock):
        """Debe buscar el usuario usando el identificador proporcionado."""
        # Arrange
        repo_usuario_mock.obtener_por_email_o_username.return_value = usuario_mock
        
        servicio = ServicioIniciarSesion(repo_usuario_mock)
        
        # Act con email
        peticion_email = LoginRequestDTO(identificador="juan.garcia@clinica.es", password="PasswordSegura123")
        servicio.login(peticion_email)
        
        # Assert
        repo_usuario_mock.obtener_por_email_o_username.assert_called_with("juan.garcia@clinica.es")
