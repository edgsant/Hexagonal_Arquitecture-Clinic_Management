from enum import Enum
import os


class TipoRepositorio(Enum):
    """
    Enumeración de tipos de repositorio disponibles.
    """
    Memoria = "Memoria"
    MySQL = "MySQL"


class Config:
    """
    Configuración general de la aplicación.

    Lee las variables de entorno necesarias para determinar el tipo de repositorio
    utilizado y la URL de conexión a la base de datos.
    """

    def __init__(self):
        """
        Inicializa la configuración leyendo variables de entorno.
        """
        tipoRepositorio = os.getenv("TIPO_REPOSITORIO", "Memoria")
        self.tipoRepositorio = TipoRepositorio(tipoRepositorio)
        self.db_url = os.getenv("DB_URL", "").strip()

    def usaSQL(self) -> bool:
        """
        Indica si se debe usar MySQL como repositorio.

        Returns:
            bool: True si el tipo de repositorio configurado es MySQL.
        """
        return self.tipoRepositorio == TipoRepositorio.MySQL

    def usaMemoria(self) -> bool:
        """
        Indica si se debe usar memoria como repositorio.

        Returns:
            bool: True si el tipo de repositorio configurado es Memoria.
        """
        return self.tipoRepositorio == TipoRepositorio.Memoria