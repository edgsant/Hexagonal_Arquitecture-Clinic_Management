from transversal.config import Config
from transversal.factory import Factory

from application.services.ServicioIniciarSesion import ServicioIniciarSesion
from application.services.ServicioRegistrarPaciente import ServicioRegistrarPaciente
from application.services.ServicioCrearProcedimiento import ServicioCrearProcedimiento
from application.services.ServicioRegistrarInforme import ServicioRegistrarInforme
from application.services.ServicioRegistrarResultados import ServicioRegistrarResultados
from application.services.ServicioConsultarProcedimiento import ServicioConsultarProcedimiento
from application.services.ServicioDarAlta import ServicioDarAlta


class Container:
    """
    Contenedor de dependencias para la aplicación.

    Gestiona la creación y configuración de los servicios y repositorios del sistema.
    """

    def __init__(self, config: Config | None = None):
        """
        Inicializa el contenedor con la configuración indicada.

        Args:
            config: Configuración de la aplicación. Si no se proporciona, se crea una configuración por defecto.
        """
        self.config = config or Config()
        self.factory = Factory(self.config)

    def servicioIniciarSesion(self) -> ServicioIniciarSesion:
        """
        Crea y devuelve una instancia del servicio de inicio de sesión.

        Returns:
            ServicioIniciarSesion: Servicio configurado.
        """
        return ServicioIniciarSesion(
            self.factory.crearRepoUsuario()
        )

    def servicioRegistrarPaciente(self) -> ServicioRegistrarPaciente:
        """
        Crea y devuelve una instancia del servicio de registro de paciente.

        Returns:
            ServicioRegistrarPaciente: Servicio configurado.
        """
        return ServicioRegistrarPaciente(
            self.factory.crearRepoPaciente()
        )

    def servicioCrearProcedimiento(self) -> ServicioCrearProcedimiento:
        """
        Crea y devuelve una instancia del servicio de creación de procedimiento.

        Returns:
            ServicioCrearProcedimiento: Servicio configurado.
        """
        return ServicioCrearProcedimiento(
            self.factory.crearRepoPaciente(),
            self.factory.crearRepoProcedimiento()
        )

    def servicioRegistrarInforme(self) -> ServicioRegistrarInforme:
        """
        Crea y devuelve una instancia del servicio de registro de informe.

        Returns:
            ServicioRegistrarInforme: Servicio configurado.
        """
        return ServicioRegistrarInforme(
            self.factory.crearRepoProcedimiento()
        )

    def servicioRegistrarResultados(self) -> ServicioRegistrarResultados:
        """
        Crea y devuelve una instancia del servicio de registro de resultados.

        Returns:
            ServicioRegistrarResultados: Servicio configurado.
        """
        return ServicioRegistrarResultados(
            self.factory.crearRepoProcedimiento()
        )

    def servicioConsultarProcedimiento(self) -> ServicioConsultarProcedimiento:
        """
        Crea y devuelve una instancia del servicio de consulta de procedimiento.

        Returns:
            ServicioConsultarProcedimiento: Servicio configurado.
        """
        return ServicioConsultarProcedimiento(
            self.factory.crearRepoProcedimiento()
        )

    def servicioDarAlta(self) -> ServicioDarAlta:
        """
        Crea y devuelve una instancia del servicio de alta.

        Returns:
            ServicioDarAlta: Servicio configurado.
        """
        return ServicioDarAlta(
            self.factory.crearRepoProcedimiento()
        )