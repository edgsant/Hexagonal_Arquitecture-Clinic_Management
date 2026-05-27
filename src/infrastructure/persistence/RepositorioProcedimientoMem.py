from domain.entities.EntityProcedimiento import EntityProcedimiento, EstadoProcedimiento


class RepositorioProcedimientoMem:
    """
    Repositorio en memoria para procedimientos.

    Implementa la interfaz IRepositorioProcedimiento usando diccionarios
    para poder buscar procedimientos por id y por paciente.
    """

    def __init__(self):
        """
        Inicializa el repositorio con diccionarios vacíos.

        - procedimientos_por_id:
            Guarda cada procedimiento usando su id como clave.

        - procedimientos_por_paciente:
            Guarda una lista de procedimientos usando el id del paciente como clave.
        """

        self.procedimientos_por_id = {}
        self.procedimientos_por_paciente = {}

    def guardar_procedimiento(self, procedimiento: EntityProcedimiento):
        """
        Agrega un procedimiento al repositorio.

        Args:
            procedimiento: El procedimiento que se va a guardar.
        """

        self.procedimientos_por_id[procedimiento.id] = procedimiento

        paciente_id = procedimiento.paciente.id
        if paciente_id not in self.procedimientos_por_paciente:
            self.procedimientos_por_paciente[paciente_id] = []

        self.procedimientos_por_paciente[paciente_id].append(procedimiento)

    def obtener_procedimiento_por_id(self, id: str):
        """
        Obtiene un procedimiento por su identificador.

        Args:
            id: Identificador del procedimiento.

        Returns:
            El procedimiento asociado al id, o None si no existe.
        """

        return self.procedimientos_por_id.get(id)

    def obtener_activo_por_paciente(self, id_paciente: str):
        """
        Obtiene el procedimiento activo de un paciente.

        Args:
            id_paciente: Identificador del paciente.

        Returns:
            El procedimiento activo del paciente, o None si no existe.
        """

        procedimientos = self.procedimientos_por_paciente.get(id_paciente, [])

        for procedimiento in procedimientos:
            if procedimiento.estado == EstadoProcedimiento.ACTIVO:
                return procedimiento

        return None

    def obtener_procedimientos_por_paciente(self, id_paciente: str):
        """
        Obtiene todos los procedimientos asociados a un paciente.

        Args:
            id_paciente: Identificador del paciente.

        Returns:
            Lista de procedimientos del paciente.
        """

        return self.procedimientos_por_paciente.get(id_paciente, [])

    def obtener_procedimientos_activos(self):
        """
        Obtiene todos los procedimientos activos del repositorio.

        Returns:
            Lista con todos los procedimientos activos.
        """

        procedimientos_activos = []

        for procedimiento in self.procedimientos_por_id.values():
            if procedimiento.estado == EstadoProcedimiento.ACTIVO:
                procedimientos_activos.append(procedimiento)

        return procedimientos_activos