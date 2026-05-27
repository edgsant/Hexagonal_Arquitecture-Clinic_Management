import pytest
from unittest.mock import MagicMock
from application.services.ServicioConsultarProcedimiento import ServicioConsultarProcedimiento


class TestServicioConsultarProcedimiento:
    """Tests para el servicio de consulta de procedimientos (CU06/RF04)."""

    def test_consultar_procedimiento_exitoso(self, repo_procedimiento_mock, procedimiento_mock):
        """Debe consultar un procedimiento existente exitosamente."""
        # Arrange
        repo_procedimiento_mock.obtener_por_id.return_value = procedimiento_mock
        
        servicio = ServicioConsultarProcedimiento(repo_procedimiento_mock)

        # Act
        respuesta = servicio.consultar_procedimiento("proc-999")

        # Assert
        assert respuesta.id_procedimiento == "proc-999"
        assert respuesta.paciente_id == "pac-456-uuid"
        assert respuesta.paciente_nombre_completo == "Alejandro Sanz"
        assert respuesta.estado == "Activo"

    def test_consultar_procedimiento_falla_no_existe(self, repo_procedimiento_mock):
        """Debe lanzar ValueError si el procedimiento no existe."""
        # Arrange
        repo_procedimiento_mock.obtener_por_id.return_value = None
        
        servicio = ServicioConsultarProcedimiento(repo_procedimiento_mock)

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            servicio.consultar_procedimiento("proc-inexistente")
        
        assert "No se encontró ningún procedimiento clínico con el ID" in str(exc_info.value)

    def test_consultar_procedimientos_paciente_exitoso(self, repo_procedimiento_mock, procedimiento_mock):
        """Debe consultar todos los procedimientos de un paciente."""
        # Arrange
        procedimiento_mock2 = MagicMock()
        procedimiento_mock2.id = "proc-998"
        procedimiento_mock2.paciente = procedimiento_mock.paciente
        estado_finalizado = MagicMock()
        estado_finalizado.value = "Finalizado"
        procedimiento_mock2.estado = estado_finalizado
        
        repo_procedimiento_mock.obtener_procedimientos_por_paciente.return_value = [procedimiento_mock, procedimiento_mock2]
        
        servicio = ServicioConsultarProcedimiento(repo_procedimiento_mock)

        # Act
        respuestas = servicio.consultar_procedimientos_paciente("pac-456-uuid")

        # Assert
        assert len(respuestas) == 2
        assert respuestas[0].id_procedimiento == "proc-999"
        assert respuestas[1].id_procedimiento == "proc-998"
        assert respuestas[0].paciente_nombre_completo == "Alejandro Sanz"

    def test_consultar_procedimientos_paciente_vacio(self, repo_procedimiento_mock):
        """Debe devolver lista vacía si el paciente no tiene procedimientos."""
        # Arrange
        repo_procedimiento_mock.obtener_procedimientos_por_paciente.return_value = []
        
        servicio = ServicioConsultarProcedimiento(repo_procedimiento_mock)

        # Act
        respuestas = servicio.consultar_procedimientos_paciente("pac-sin-procedimientos")

        # Assert
        assert respuestas == []

    def test_consultar_procedimiento_activo_exitoso(self, repo_procedimiento_mock, procedimiento_mock):
        """Debe consultar el procedimiento activo de un paciente."""
        # Arrange
        repo_procedimiento_mock.obtener_activo_por_paciente.return_value = procedimiento_mock
        
        servicio = ServicioConsultarProcedimiento(repo_procedimiento_mock)

        # Act
        respuesta = servicio.consultar_procedimiento_activo_paciente("pac-456-uuid")

        # Assert
        assert respuesta.id_procedimiento == "proc-999"
        assert respuesta.paciente_id == "pac-456-uuid"
        assert respuesta.estado == "Activo"

    def test_consultar_procedimiento_activo_falla_no_existe(self, repo_procedimiento_mock):
        """Debe lanzar ValueError si el paciente no tiene procedimiento activo."""
        # Arrange
        repo_procedimiento_mock.obtener_activo_por_paciente.return_value = None
        
        servicio = ServicioConsultarProcedimiento(repo_procedimiento_mock)

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            servicio.consultar_procedimiento_activo_paciente("pac-sin-activos")
        
        assert "no tiene ningún procedimiento activo actualmente" in str(exc_info.value)
