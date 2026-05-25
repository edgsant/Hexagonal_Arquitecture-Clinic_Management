import pytest
from unittest.mock import MagicMock, patch
from application.dtos.InformeDTOs import RegistrarInformeRequestDTO
from application.services.ServicioRegistrarInforme import ServicioRegistrarInforme


class TestServicioRegistrarInforme:
    """Tests para el servicio de registro de informes (CU04)."""

    def test_registrar_informe_exitoso(self, datos_informe_validos, repo_procedimiento_mock, repo_usuario_mock, 
                                       procedimiento_mock, usuario_mock):
        """Debe registrar un informe exitosamente cuando el procedimiento existe y está activo."""
        # Arrange
        repo_procedimiento_mock.obtener_por_id.return_value = procedimiento_mock
        repo_usuario_mock.obtener_por_especialista_id.return_value = usuario_mock
        
        servicio = ServicioRegistrarInforme(repo_procedimiento_mock, repo_usuario_mock)
        peticion = RegistrarInformeRequestDTO(**datos_informe_validos)

        # Act
        respuesta = servicio.registrar_informe(peticion)

        # Assert
        assert respuesta.informe_id is not None
        assert respuesta.procedimiento_id == "proc-999"
        assert respuesta.fecha == datos_informe_validos["fecha"]
        assert repo_procedimiento_mock.guardar.called

    def test_registrar_informe_falla_procedimiento_no_existe(self, datos_informe_validos, 
                                                             repo_procedimiento_mock, repo_usuario_mock):
        """Debe lanzar ValueError si el procedimiento no existe."""
        # Arrange
        repo_procedimiento_mock.obtener_por_id.return_value = None
        
        servicio = ServicioRegistrarInforme(repo_procedimiento_mock, repo_usuario_mock)
        peticion = RegistrarInformeRequestDTO(**datos_informe_validos)

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            servicio.registrar_informe(peticion)
        
        assert "Procedimiento no encontrado" in str(exc_info.value)

    def test_registrar_informe_falla_procedimiento_finalizado(self, datos_informe_validos, 
                                                              repo_procedimiento_mock, repo_usuario_mock, 
                                                              paciente_mock):
        """Debe lanzar ValueError si el procedimiento está finalizado."""
        # Arrange
        from domain.entities.EntityProcedimiento import EntityProcedimiento, EstadoProcedimiento
        procedimiento_finalizado = MagicMock(spec=EntityProcedimiento)
        procedimiento_finalizado.estado = EstadoProcedimiento.FINALIZADO
        
        repo_procedimiento_mock.obtener_por_id.return_value = procedimiento_finalizado
        
        servicio = ServicioRegistrarInforme(repo_procedimiento_mock, repo_usuario_mock)
        peticion = RegistrarInformeRequestDTO(**datos_informe_validos)

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            servicio.registrar_informe(peticion)
        
        assert "No se pueden añadir informes a un procedimiento finalizado" in str(exc_info.value)

    def test_registrar_informe_falla_especialista_no_existe(self, datos_informe_validos, 
                                                            repo_procedimiento_mock, repo_usuario_mock, 
                                                            procedimiento_mock):
        """Debe lanzar ValueError si el especialista no existe."""
        # Arrange
        repo_procedimiento_mock.obtener_por_id.return_value = procedimiento_mock
        repo_usuario_mock.obtener_por_especialista_id.return_value = None
        
        servicio = ServicioRegistrarInforme(repo_procedimiento_mock, repo_usuario_mock)
        peticion = RegistrarInformeRequestDTO(**datos_informe_validos)

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            servicio.registrar_informe(peticion)
        
        assert "Especialista no autorizado o no encontrado" in str(exc_info.value)
