from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base, sessionmaker

from domain.entities.EntityPaciente import EntityPaciente


Base = declarative_base()


class PacienteModel(Base):
    """
    Modelo SQLAlchemy para la tabla de pacientes.

    Esta clase representa cómo se guarda un paciente en la base de datos.
    """

    __tablename__ = "pacientes"

    id = Column(String(50), primary_key=True)
    dni = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    apellidos = Column(String(150), nullable=False)


class RepositorioPacienteSQLAlchemy:
    """
    Repositorio SQL para pacientes usando SQLAlchemy y MySQL.

    Implementa la interfaz RepositorioPaciente.
    """

    def __init__(self, url_bd: str):
        """
        Inicializa el repositorio.

        Args:
            url_bd: URL de conexión a la base de datos MySQL.

        """

        self.engine = create_engine(url_bd)
        self.Session = sessionmaker(bind=self.engine)

        Base.metadata.create_all(self.engine)

    def _a_entidad(self, modelo: PacienteModel):
        """
        Convierte un modelo SQLAlchemy en una entidad de dominio.

        Args:
            modelo: PacienteModel obtenido desde la base de datos.

        Returns:
            Entidad Paciente, o None si el modelo no existe.
        """

        if modelo is None:
            return None

        return EntityPaciente(
            id=modelo.id,
            dni=modelo.dni,
            nombre=modelo.nombre,
            apellidos=modelo.apellidos
        )

    def _a_modelo(self, paciente: EntityPaciente):
        """
        Convierte una entidad de dominio en un modelo SQLAlchemy.

        Args:
            paciente: Entidad Paciente.

        Returns:
            Modelo PacienteModel.
        """

        return PacienteModel(
            id=paciente.id,
            dni=paciente.dni,
            nombre=paciente.nombre,
            apellidos=paciente.apellidos
        )

    def guardar_paciente(self, paciente: EntityPaciente):
        """
        Guarda un paciente en la base de datos.

        Si ya existe un paciente con el mismo id, lo actualiza.

        Args:
            paciente: Paciente que se va a guardar.
        """

        session = self.Session()

        try:
            modelo_existente = session.get(PacienteModel, paciente.id)

            if modelo_existente is None:
                modelo = self._a_modelo(paciente)
                session.add(modelo)
            else:
                modelo_existente.dni = paciente.dni
                modelo_existente.nombre = paciente.nombre
                modelo_existente.apellidos = paciente.apellidos

            session.commit()

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()

    def obtener_por_id(self, paciente_id: str):
        """
        Obtiene un paciente por su identificador.

        Args:
            paciente_id: Identificador del paciente.

        Returns:
            Paciente encontrado, o None si no existe.
        """

        session = self.Session()

        try:
            modelo = session.get(PacienteModel, paciente_id)
            return self._a_entidad(modelo)

        finally:
            session.close()

    def obtener_por_dni(self, dni: str):
        """
        Obtiene un paciente por su DNI.

        Args:
            dni: DNI del paciente.

        Returns:
            Paciente encontrado, o None si no existe.
        """

        session = self.Session()

        try:
            modelo = (
                session.query(PacienteModel)
                .filter(PacienteModel.dni == dni)
                .first()
            )

            return self._a_entidad(modelo)

        finally:
            session.close()

    def obtener_todos(self):
        """
        Obtiene todos los pacientes guardados.

        Returns:
            Lista de pacientes.
        """

        session = self.Session()

        try:
            modelos = session.query(PacienteModel).all()

            pacientes = []

            for modelo in modelos:
                pacientes.append(self._a_entidad(modelo))

            return pacientes

        finally:
            session.close()

    def eliminar_por_id(self, paciente_id: str):
        """
        Elimina un paciente por su identificador.

        Args:
            paciente_id: Identificador del paciente que se quiere eliminar.
        """

        session = self.Session()

        try:
            modelo = session.get(PacienteModel, paciente_id)

            if modelo is not None:
                session.delete(modelo)
                session.commit()

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()