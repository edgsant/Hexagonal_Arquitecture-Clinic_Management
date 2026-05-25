import pytest
from unittest.mock import MagicMock
from application.services.ServicioDarAlta import ServicioDarAlta


class TestServicioDarAlta:
    """Tests para el servicio de finalización de procedimientos (CU07)."""

    def test_finalizar_procedimiento_exitoso(self, repo_procedimiento_mock, procedimiento_mock):
        """Debe finalizar un procedimiento exitosamente."""
        # Arrange
        repo_procedimiento_mock.obtener_por_id.return_value = procedimiento_mock
        
        # Simulamos que la finalización cambia el estado
        estado_finalizado = MagicMock()
        estado_finalizado.value = "Finalizado"
        procedimiento_mock.estado = estado_finalizado
        
        servicio = ServicioDarAlta(repo_procedimiento_mock)

        # Act
        respuesta = servicio.finalizar_procedimiento("proc-999")

        # Assert
        assert respuesta.id_procedimiento == "proc-999"
        assert respuesta.paciente_id == "pac-456-uuid"
        assert respuesta.paciente_nombre_completo == "Alejandro Sanz"
        assert respuesta.estado == "Finalizado"
        repo_procedimiento_mock.obtener_por_id.assert_called_with("proc-999")
        procedimiento_mock.finalizar.assert_called_once()
        assert repo_procedimiento_mock.guardar_procedimiento.called

    def test_finalizar_procedimiento_falla_no_existe(self, repo_procedimiento_mock):
        """Debe lanzar ValueError si el procedimiento no existe."""
        # Arrange
        repo_procedimiento_mock.obtener_por_id.return_value = None
        
        servicio = ServicioDarAlta(repo_procedimiento_mock)

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            servicio.finalizar_procedimiento("proc-inexistente")
        
        assert "No se encontró ningún procedimiento clínico con el ID" in str(exc_info.value)

    def test_finalizar_procedimiento_falla_por_restriccion_dominio(self, repo_procedimiento_mock, procedimiento_mock):
        """Debe lanzar ValueError si el dominio rechaza la finalización (ej: pruebas pendientes)."""
        # Arrange
        repo_procedimiento_mock.obtener_por_id.return_value = procedimiento_mock
        procedimiento_mock.finalizar.side_effect = Exception("El procedimiento tiene pruebas pendientes")
        
        servicio = ServicioDarAlta(repo_procedimiento_mock)

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            servicio.finalizar_procedimiento("proc-999")
        
        assert "El procedimiento tiene pruebas pendientes" in str(exc_info.value)
        assert not repo_procedimiento_mock.guardar_procedimiento.called

    def test_finalizar_procedimiento_persiste_cambios(self, repo_procedimiento_mock, procedimiento_mock):
        """Debe guardar los cambios del procedimiento en el repositorio."""
        # Arrange
        repo_procedimiento_mock.obtener_por_id.return_value = procedimiento_mock
        estado_finalizado = MagicMock()
        estado_finalizado.value = "Finalizado"
        procedimiento_mock.estado = estado_finalizado
        
        servicio = ServicioDarAlta(repo_procedimiento_mock)

        # Act
        servicio.finalizar_procedimiento("proc-999")

        # Assert
        assert repo_procedimiento_mock.guardar_procedimiento.called
        # Verificamos que se pasó el procedimiento modificado
        call_args = repo_procedimiento_mock.guardar_procedimiento.call_args
        assert call_args[0][0] == procedimiento_mock
