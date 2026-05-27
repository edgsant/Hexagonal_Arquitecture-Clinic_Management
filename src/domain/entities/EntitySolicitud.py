from datetime import date
from .EntityPrueba import EntityPrueba


class EntitySolicitud:
    """
    Entidad que representa la solicitud de una prueba médica.

    Una solicitud relaciona una consulta con una prueba pendiente de realizar,
    registrando la fecha prevista para su realización.
    """

    def __init__(self, id: str, fecha_prevista: date, prueba: EntityPrueba):
        # Comprobación de identidad obligatoria
        # El ID es la identidad de la entidad y se utiliza en __eq__ y __hash__.
        if not id:
            raise ValueError("La solicitud debe tener un ID válido.")

        # Comprobación de fecha prevista obligatoria
        if not fecha_prevista:
            raise ValueError("La fecha prevista de la solicitud es obligatoria.")

        # Comprobación de la prueba asociada
        # Una solicitud siempre debe estar asociada a una prueba médica válida.
        if not isinstance(prueba, EntityPrueba):
            raise ValueError("La solicitud debe estar asociada a una EntityPrueba válida.")

        # Asignación de atributos internos
        self._id = id
        self._fecha_prevista = fecha_prevista
        self._prueba = prueba

    # --- GETTERS ---

    @property
    def id(self) -> str:
        return self._id

    @property
    def fecha_prevista(self) -> date:
        return self._fecha_prevista

    @property
    def prueba(self) -> EntityPrueba:
        return self._prueba

    # --- MÉTODOS MÁGICOS (Identidad DDD) ---

    def __eq__(self, other: object) -> bool:
        """
        Regla DDD: Dos solicitudes son la misma si tienen el mismo ID.
        """
        if not isinstance(other, EntitySolicitud):
            return NotImplemented

        return self._id == other.id

    def __hash__(self) -> int:
        return hash(self._id)

    def __str__(self) -> str:
        """
        Representación legible para interfaces.
        """
        return f"Solicitud {self._id} prevista para {self._fecha_prevista}"

    def __repr__(self) -> str:
        """
        Representación técnica para debugging.
        """
        return f"<EntitySolicitud id={self._id} fecha_prevista={self._fecha_prevista}>"