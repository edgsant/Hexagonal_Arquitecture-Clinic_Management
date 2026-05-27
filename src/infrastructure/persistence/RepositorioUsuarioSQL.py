from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base, sessionmaker

from domain.entities.EntityUsuario import EntityUsuario


Base = declarative_base()


class UsuarioModel(Base):
    """
    Modelo SQLAlchemy para la tabla de usuarios.

    Esta clase representa cómo se guarda un usuario en la base de datos.
    """

    __tablename__ = "usuarios"

    id = Column(String(50), primary_key=True)
    email = Column(String(150), unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)


class Usuario:
    """
    Entidad de dominio que representa un usuario.

    Esta clase es la que usaría la lógica de negocio.
    """

    def __init__(self, id: str, email: str, username: str, password: str):
        """
        Inicializa un usuario.

        Args:
            id: Identificador único del usuario.
            email: Email del usuario.
            username: Nombre de usuario.
            password: Contraseña del usuario.
        """

        self.id = id
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):
        """
        Representación en texto del usuario.
        """

        return (
            f"Usuario("
            f"id='{self.id}', "
            f"email='{self.email}', "
            f"username='{self.username}'"
            f")"
        )


class RepositorioUsuarioSQLAlchemy:
    """
    Repositorio SQL para usuarios usando SQLAlchemy y MySQL.

    Implementa la interfaz de repositorio de usuarios.
    """

    def __init__(self, url_bd: str):
        """
        Inicializa el repositorio.

        Args:
            url_bd: URL de conexión a la base de datos MySQL.

        Ejemplo:
            mysql+pymysql://usuario:password@localhost:3306/clinica
        """

        self.engine = create_engine(url_bd)
        self.Session = sessionmaker(bind=self.engine)

        Base.metadata.create_all(self.engine)

    def _a_entidad(self, modelo: UsuarioModel):
        """
        Convierte un modelo SQLAlchemy en una entidad de dominio.

        Args:
            modelo: UsuarioModel obtenido desde la base de datos.

        Returns:
            Entidad Usuario, o None si el modelo no existe.
        """

        if modelo is None:
            return None

        return Usuario(
            id=modelo.id,
            email=modelo.email,
            username=modelo.username,
            password=modelo.password
        )

    def _a_modelo(self, usuario: Usuario):
        """
        Convierte una entidad de dominio en un modelo SQLAlchemy.

        Args:
            usuario: Entidad Usuario.

        Returns:
            Modelo UsuarioModel.
        """

        return UsuarioModel(
            id=usuario.id,
            email=usuario.email,
            username=usuario.username,
            password=usuario.password
        )

    def guardar_usuario(self, usuario: Usuario):
        """
        Guarda un usuario en la base de datos.

        Si ya existe un usuario con el mismo id, lo actualiza.

        Args:
            usuario: Usuario que se va a guardar.
        """

        session = self.Session()

        try:
            modelo_existente = session.get(UsuarioModel, usuario.id)

            if modelo_existente is None:
                modelo = self._a_modelo(usuario)
                session.add(modelo)
            else:
                modelo_existente.email = usuario.email
                modelo_existente.username = usuario.username
                modelo_existente.password = usuario.password

            session.commit()

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()

    def obtener_por_id(self, usuario_id: str):
        """
        Obtiene un usuario por su identificador.

        Args:
            usuario_id: Identificador del usuario.

        Returns:
            Usuario encontrado, o None si no existe.
        """

        session = self.Session()

        try:
            modelo = session.get(UsuarioModel, usuario_id)
            return self._a_entidad(modelo)

        finally:
            session.close()

    def obtener_por_email(self, email: str):
        """
        Obtiene un usuario por su email.

        Args:
            email: Email del usuario.

        Returns:
            Usuario encontrado, o None si no existe.
        """

        session = self.Session()

        try:
            modelo = (
                session.query(UsuarioModel)
                .filter(UsuarioModel.email == email)
                .first()
            )

            return self._a_entidad(modelo)

        finally:
            session.close()

    def obtener_por_username(self, username: str):
        """
        Obtiene un usuario por su nombre de usuario.

        Args:
            username: Nombre de usuario.

        Returns:
            Usuario encontrado, o None si no existe.
        """

        session = self.Session()

        try:
            modelo = (
                session.query(UsuarioModel)
                .filter(UsuarioModel.username == username)
                .first()
            )

            return self._a_entidad(modelo)

        finally:
            session.close()

    def obtener_por_email_o_username(self, identificador: str):
        """
        Obtiene un usuario usando email o username.

        Primero intenta buscar por email.
        Si no encuentra ningún usuario, busca por username.

        Args:
            identificador: Email o username del usuario.

        Returns:
            Usuario encontrado, o None si no existe.
        """

        session = self.Session()

        try:
            modelo = (
                session.query(UsuarioModel)
                .filter(
                    (UsuarioModel.email == identificador) |
                    (UsuarioModel.username == identificador)
                )
                .first()
            )

            return self._a_entidad(modelo)

        finally:
            session.close()

    def obtener_todos(self):
        """
        Obtiene todos los usuarios guardados.

        Returns:
            Lista de usuarios.
        """

        session = self.Session()

        try:
            modelos = session.query(UsuarioModel).all()

            usuarios = []

            for modelo in modelos:
                usuarios.append(self._a_entidad(modelo))

            return usuarios

        finally:
            session.close()

    def eliminar_por_id(self, usuario_id: str):
        """
        Elimina un usuario por su identificador.

        Args:
            usuario_id: Identificador del usuario que se quiere eliminar.
        """

        session = self.Session()

        try:
            modelo = session.get(UsuarioModel, usuario_id)

            if modelo is not None:
                session.delete(modelo)
                session.commit()

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()