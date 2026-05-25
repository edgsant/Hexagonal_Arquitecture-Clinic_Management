import pytest
from unittest.mock import MagicMock
from application.dtos.AnaliticaDTOs import RegistrarResultadosRequestDTO
from application.services.ServicioRegistrarResultados import ServicioRegistrarResultados


class TestServicioRegistrarResultados:
    """Tests para el servicio de registro de resultados analíticos (CU05)."""

    def test_registrar_resultados_exitoso(self, datos_analitica_validos, repo_procedimiento_mock, 
                                          repo_usuario_mock, procedimiento_mock, usuario_mock, analitica_mock):
        """Debe registrar los resultados analíticos exitosamente."""
        # Arrange
        procedimiento_mock.obtener_pruebas_pendientes.return_value = [analitica_mock]
        repo_procedimiento_mock.obtener_por_id.return_value = procedimiento_mock
        repo_usuario_mock.obtener_por_especialista_id.return_value = usuario_mock
        
        servicio = ServicioRegistrarResultados(repo_procedimiento_mock, repo_usuario_mock)
        peticion = RegistrarResultadosRequestDTO(**datos_analitica_validos)

        # Act
        respuesta = servicio.registrar_resultados(peticion)

        # Assert
        assert respuesta.analitica_id == "an-888"
        assert respuesta.analista_id == "esp-urologo-1"
        assert respuesta.psa == "1.4 ng/mL"
        assert respuesta.pendiente is False
        assert repo_procedimiento_mock.guardar.called
        analitica_mock.registrar_resultados.assert_called_once()

    def test_registrar_resultados_falla_procedimiento_no_existe(self, datos_analitica_validos,
                                                                repo_procedimiento_mock, repo_usuario_mock):
        """Debe lanzar ValueError si el procedimiento no existe."""
        # Arrange
        repo_procedimiento_mock.obtener_por_id.return_value = None
        
        servicio = ServicioRegistrarResultados(repo_procedimiento_mock, repo_usuario_mock)
        peticion = RegistrarResultadosRequestDTO(**datos_analitica_validos)

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            servicio.registrar_resultados(peticion)
        
        assert "Procedimiento no encontrado" in str(exc_info.value)

    def test_registrar_resultados_falla_procedimiento_finalizado(self, datos_analitica_validos,
                                                                 repo_procedimiento_mock, repo_usuario_mock,
                                                                 paciente_mock):
        """Debe lanzar ValueError si el procedimiento está finalizado."""
        # Arrange
        from domain.entities.EntityProcedimiento import EntityProcedimiento, EstadoProcedimiento
        procedimiento_finalizado = MagicMock(spec=EntityProcedimiento)
        procedimiento_finalizado.estado = EstadoProcedimiento.FINALIZADO
        
        repo_procedimiento_mock.obtener_por_id.return_value = procedimiento_finalizado
        
        servicio = ServicioRegistrarResultados(repo_procedimiento_mock, repo_usuario_mock)
        peticion = RegistrarResultadosRequestDTO(**datos_analitica_validos)

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            servicio.registrar_resultados(peticion)
        
        assert "No se puede modificar un procedimiento que ya está finalizado" in str(exc_info.value)

    def test_registrar_resultados_falla_especialista_no_existe(self, datos_analitica_validos,
                                                               repo_procedimiento_mock, repo_usuario_mock,
                                                               procedimiento_mock, analitica_mock):
        """Debe lanzar ValueError si el especialista no existe."""
        # Arrange
        procedimiento_mock.obtener_pruebas_pendientes.return_value = [analitica_mock]
        repo_procedimiento_mock.obtener_por_id.return_value = procedimiento_mock
        repo_usuario_mock.obtener_por_especialista_id.return_value = None
        
        servicio = ServicioRegistrarResultados(repo_procedimiento_mock, repo_usuario_mock)
        peticion = RegistrarResultadosRequestDTO(**datos_analitica_validos)

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            servicio.registrar_resultados(peticion)
        
        assert "Especialista no autorizado o no encontrado" in str(exc_info.value)

    def test_registrar_resultados_falla_analitica_no_existe(self, datos_analitica_validos,
                                                            repo_procedimiento_mock, repo_usuario_mock,
                                                            procedimiento_mock, usuario_mock):
        """Debe lanzar ValueError si la analítica no existe en el procedimiento."""
        # Arrange
        procedimiento_mock.obtener_pruebas_pendientes.return_value = []  # Sin análiticas pendientes
        repo_procedimiento_mock.obtener_por_id.return_value = procedimiento_mock
        repo_usuario_mock.obtener_por_especialista_id.return_value = usuario_mock
        
        servicio = ServicioRegistrarResultados(repo_procedimiento_mock, repo_usuario_mock)
        peticion = RegistrarResultadosRequestDTO(**datos_analitica_validos)

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            servicio.registrar_resultados(peticion)
        
        assert "La analítica no existe en este procedimiento o ya fue completada" in str(exc_info.value)
