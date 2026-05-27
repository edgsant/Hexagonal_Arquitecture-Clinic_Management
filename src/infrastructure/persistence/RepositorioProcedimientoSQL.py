from sqlalchemy import create_engine, Column, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from domain.entities.EntityProcedimiento import EntityProcedimiento, EstadoProcedimiento


Base = declarative_base()


class ProcedimientoModel(Base):
    """
    Modelo SQLAlchemy para la tabla de procedimientos.

    Esta clase representa cómo se guarda un procedimiento en la base de datos.
    """

    __tablename__ = "procedimientos"

    id = Column(String(50), primary_key=True)
    id_paciente = Column(String(50), nullable=False)
    activo = Column(Boolean, nullable=False)


class RepositorioProcedimientoSQLAlchemy:
    """
    Repositorio SQL para procedimientos usando SQLAlchemy y MySQL.

    Implementa la interfaz IRepositorioProcedimiento.
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

    def _a_entidad(self, modelo: ProcedimientoModel):
        """
        Convierte un modelo SQLAlchemy en una entidad de dominio.

        Args:
            modelo: ProcedimientoModel obtenido desde la base de datos.

        Returns:
            Entidad Procedimiento, o None si el modelo no existe.
        """

        if modelo is None:
            return None
        
        estado_enum = EstadoProcedimiento.ACTIVO if modelo.activo else EstadoProcedimiento.FINALIZADO

        return EntityProcedimiento(
            id=modelo.id,
            id_paciente=modelo.id_paciente,
            activo=estado_enum
        )

    def _a_modelo(self, procedimiento: EntityProcedimiento):
        """
        Convierte una entidad de dominio en un modelo SQLAlchemy.

        Args:
            procedimiento: Entidad Procedimiento.

        Returns:
            Modelo ProcedimientoModel.
        """

        es_activo = (procedimiento.estado == EstadoProcedimiento.ACTIVO)

        return ProcedimientoModel(
            id=procedimiento.id,
            id_paciente=procedimiento.paciente.id,
            activo=es_activo
        )

    def guardar_procedimiento(self, procedimiento: EntityProcedimiento):
        """
        Guarda un procedimiento en la base de datos.

        Si ya existe un procedimiento con el mismo id, lo actualiza.

        Args:
            procedimiento: Procedimiento que se va a guardar.
        """

        session = self.Session()

        try:
            modelo_existente = session.get(ProcedimientoModel, procedimiento.id)

            if modelo_existente is None:
                modelo = self._a_modelo(procedimiento)
                session.add(modelo)
            else:
                modelo_existente.id_paciente = procedimiento.paciente.id
                modelo_existente.activo = (procedimiento.estado == EstadoProcedimiento.ACTIVO)

            session.commit()

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()

    def obtener_procedimiento_por_id(self, id: str):
        """
        Obtiene un procedimiento por su identificador.

        Args:
            id: Identificador del procedimiento.

        Returns:
            Procedimiento encontrado, o None si no existe.
        """

        session = self.Session()

        try:
            modelo = session.get(ProcedimientoModel, id)
            return self._a_entidad(modelo)

        finally:
            session.close()

    def obtener_activo_por_paciente(self, id_paciente: str):
        """
        Obtiene el procedimiento activo de un paciente.

        Args:
            id_paciente: Identificador del paciente.

        Returns:
            Procedimiento activo del paciente, o None si no existe.
        """

        session = self.Session()

        try:
            modelo = (
                session.query(ProcedimientoModel)
                .filter(
                    ProcedimientoModel.id_paciente == id_paciente,
                    ProcedimientoModel.activo == True
                )
                .first()
            )

            return self._a_entidad(modelo)

        finally:
            session.close()

    def obtener_procedimientos_por_paciente(self, id_paciente: str):
        """
        Obtiene todos los procedimientos asociados a un paciente.

        Args:
            id_paciente: Identificador del paciente.

        Returns:
            Lista de procedimientos del paciente.
        """

        session = self.Session()

        try:
            modelos = (
                session.query(ProcedimientoModel)
                .filter(ProcedimientoModel.id_paciente == id_paciente)
                .all()
            )

            procedimientos = []

            for modelo in modelos:
                procedimientos.append(self._a_entidad(modelo))

            return procedimientos

        finally:
            session.close()

    def obtener_procedimientos_activos(self):
        """
        Obtiene todos los procedimientos activos.

        Returns:
            Lista de procedimientos activos.
        """

        session = self.Session()

        try:
            modelos = (
                session.query(ProcedimientoModel)
                .filter(ProcedimientoModel.activo == True)
                .all()
            )

            procedimientos = []

            for modelo in modelos:
                procedimientos.append(self._a_entidad(modelo))

            return procedimientos

        finally:
            session.close()