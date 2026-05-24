from transversal.Config import Config

from domain.ports.IRepositorioProcedimiento import IRepositorioProcedimiento
from domain.ports.IRepositorioPaciente import IRepositorioPaciente
from domain.ports.IRepositorioUsuario import IRepositorioUsuario

from infrastructure.persistence.RepositorioProcedimientoMem import RepositorioProcedimientoMem
from infrastructure.persistence.RepositorioProcedimientoSQL import RepositorioProcedimientoSQL
from infrastructure.persistence.RepositorioPacienteMem import RepositorioPacienteMem
from infrastructure.persistence.RepositorioPacienteSQL import RepositorioPacienteSQL
from infrastructure.persistence.RepositorioUsuarioMem import RepositorioUsuarioMem
from infrastructure.persistence.RepositorioUsuarioSQL import RepositorioUsuarioSQL


class Factory:
    """
    Fábrica para crear instancias de repositorios.

    Gestiona la creación de repositorios según la configuración del sistema,
    utilizando persistencia en memoria o persistencia SQL.
    """

    def __init__(self, config: Config):
        """
        Inicializa la fábrica con la configuración.

        Args:
            config: Configuración que determina el tipo de repositorio.
        """
        self.config = config
        self.__repoProcedimiento: IRepositorioProcedimiento | None = None
        self.__repoPaciente: IRepositorioPaciente | None = None
        self.__repoUsuario: IRepositorioUsuario | None = None

    def crearRepoProcedimiento(self) -> IRepositorioProcedimiento:
        """
        Crea o devuelve la instancia del repositorio de procedimientos.

        Returns:
            IRepositorioProcedimiento: Instancia del repositorio configurado.
        """
        if self.__repoProcedimiento is None:
            if self.config.usaSQL():
                self.__repoProcedimiento = RepositorioProcedimientoSQL(
                    self.__obtenerDbUrl()
                )
            else:
                self.__repoProcedimiento = RepositorioProcedimientoMem()

        return self.__repoProcedimiento

    def crearRepoPaciente(self) -> IRepositorioPaciente:
        """
        Crea o devuelve la instancia del repositorio de pacientes.

        Returns:
            IRepositorioPaciente: Instancia del repositorio configurado.
        """
        if self.__repoPaciente is None:
            if self.config.usaSQL():
                self.__repoPaciente = RepositorioPacienteSQL(
                    self.__obtenerDbUrl()
                )
            else:
                self.__repoPaciente = RepositorioPacienteMem()

        return self.__repoPaciente

    def crearRepoUsuario(self) -> IRepositorioUsuario:
        """
        Crea o devuelve la instancia del repositorio de usuarios.

        Returns:
            IRepositorioUsuario: Instancia del repositorio configurado.
        """
        if self.__repoUsuario is None:
            if self.config.usaSQL():
                self.__repoUsuario = RepositorioUsuarioSQL(
                    self.__obtenerDbUrl()
                )
            else:
                self.__repoUsuario = RepositorioUsuarioMem()

        return self.__repoUsuario

    def __obtenerDbUrl(self) -> str:
        """
        Obtiene la URL de conexión a la base de datos.

        Returns:
            str: URL de conexión configurada.

        Raises:
            ValueError: Si la URL está vacía cuando se usa SQL.
        """
        if not self.config.db_url:
            raise ValueError(
                "DB_URL no puede estar vacío cuando se utiliza repositorio SQL"
            )

        return self.config.db_url