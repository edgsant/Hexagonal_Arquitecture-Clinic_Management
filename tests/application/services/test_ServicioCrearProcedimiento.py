import pytest
from unittest.mock import MagicMock
from application.services.ServicioCrearProcedimiento import ServicioCrearProcedimiento


class TestServicioCrearProcedimiento:
    """Tests para el servicio de creación de procedimientos (CU03)."""

    def test_crear_procedimiento_exitoso(self, repo_paciente_mock, repo_procedimiento_mock, paciente_mock):
        """Debe crear un procedimiento nuevo exitosamente cuando no existe procedimiento activo."""
        # Arrange
        repo_paciente_mock.obtener_por_id.return_value = paciente_mock
        repo_procedimiento_mock.obtener_activo_por_paciente.return_value = None  # Sin procedimiento activo
        
        servicio = ServicioCrearProcedimiento(repo_paciente_mock, repo_procedimiento_mock)

        # Act
        respuesta = servicio.crear_procedimiento("pac-456-uuid")

        # Assert
        assert respuesta.id_procedimiento is not None
        assert respuesta.paciente_id == "pac-456-uuid"
        assert respuesta.paciente_nombre_completo == "Alejandro Sanz"
        assert respuesta.estado == "Activo"
        repo_paciente_mock.obtener_por_id.assert_called_with("pac-456-uuid")
        repo_procedimiento_mock.obtener_activo_por_paciente.assert_called_with("pac-456-uuid")
        assert repo_procedimiento_mock.guardar_procedimiento.called

    def test_crear_procedimiento_falla_paciente_no_existe(self, repo_paciente_mock, repo_procedimiento_mock):
        """Debe lanzar ValueError si el paciente no existe."""
        # Arrange
        repo_paciente_mock.obtener_por_id.return_value = None
        
        servicio = ServicioCrearProcedimiento(repo_paciente_mock, repo_procedimiento_mock)

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            servicio.crear_procedimiento("pac-inexistente")
        
        assert "No existe ningún paciente con el ID" in str(exc_info.value)
        assert not repo_procedimiento_mock.guardar_procedimiento.called

    def test_crear_procedimiento_falla_ya_existe_activo(self, repo_paciente_mock, repo_procedimiento_mock, 
                                                        paciente_mock, procedimiento_mock):
        """Debe lanzar ValueError si el paciente ya tiene un procedimiento activo."""
        # Arrange
        repo_paciente_mock.obtener_por_id.return_value = paciente_mock
        repo_procedimiento_mock.obtener_activo_por_paciente.return_value = procedimiento_mock
        
        servicio = ServicioCrearProcedimiento(repo_paciente_mock, repo_procedimiento_mock)

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            servicio.crear_procedimiento("pac-456-uuid")
        
        assert "El paciente ya tiene un procedimiento clínico activo" in str(exc_info.value)
        assert not repo_procedimiento_mock.guardar_procedimiento.called

    def test_crear_procedimiento_genera_id_unico(self, repo_paciente_mock, repo_procedimiento_mock, paciente_mock):
        """Debe generar IDs únicos para cada procedimiento creado."""
        # Arrange
        repo_paciente_mock.obtener_por_id.return_value = paciente_mock
        repo_procedimiento_mock.obtener_activo_por_paciente.return_value = None
        
        servicio = ServicioCrearProcedimiento(repo_paciente_mock, repo_procedimiento_mock)

        # Act
        respuesta1 = servicio.crear_procedimiento("pac-456-uuid")
        respuesta2 = servicio.crear_procedimiento("pac-456-uuid")

        # Assert
        assert respuesta1.id_procedimiento != respuesta2.id_procedimiento
