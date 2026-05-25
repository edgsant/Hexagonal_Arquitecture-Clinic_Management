import pytest
from unittest.mock import MagicMock
from application.dtos.PacienteDTOs import RegistrarPacienteRequestDTO
from application.services.ServicioRegistrarPaciente import ServicioRegistrarPaciente


class TestServicioRegistrarPaciente:
    """Tests para el servicio de registro de pacientes (CU02)."""

    def test_registrar_paciente_falla_por_duplicado(self, datos_paciente_request, repo_paciente_mock, paciente_mock):
        """Debe lanzar ValueError si ya existe un paciente con el mismo DNI."""
        # Arrange
        repo_paciente_mock.obtener_por_dni.return_value = paciente_mock  # Existe duplicado
        
        servicio = ServicioRegistrarPaciente(repo_paciente_mock)
        peticion = RegistrarPacienteRequestDTO(**datos_paciente_request)

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            servicio.registrar_paciente(peticion)
        
        assert "Ya existe un paciente registrado con el DNI" in str(exc_info.value)
        assert not repo_paciente_mock.guardar_paciente.called

    def test_registrar_paciente_busca_duplicados_por_dni(self, datos_paciente_request, repo_paciente_mock):
        """Debe buscar duplicados consultando el repositorio por DNI."""
        # Arrange
        repo_paciente_mock.obtener_por_dni.return_value = None  # No hay duplicado
        
        servicio = ServicioRegistrarPaciente(repo_paciente_mock)
        peticion = RegistrarPacienteRequestDTO(**datos_paciente_request)

        # Act & Assert (la creación fallará porque no tenemos EntityPaciente real, pero verificamos la búsqueda)
        try:
            servicio.registrar_paciente(peticion)
        except:
            pass  # Esperamos error, pero ya verificamos que se buscó por DNI
        
        repo_paciente_mock.obtener_por_dni.assert_called_with(datos_paciente_request["dni"])
