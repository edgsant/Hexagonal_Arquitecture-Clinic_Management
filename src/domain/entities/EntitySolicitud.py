from datetime import date
from .EntityPrueba import EntityPrueba

class EntitySolicitud:
    """
    Entidad que representa la petición de una prueba médica.
    Pertenece intrínsecamente a una EntityConsulta (Composición) 
    y mantiene una asociación directa (1:1) con la EntityPrueba a realizar.
    """
    def __init__(self, id: str, fecha_prevista: date, prueba: EntityPrueba):
        # Validaciones de integridad defensiva
        if not id:
            raise ValueError("La solicitud debe tener un ID válido.")
        if not fecha_prevista:
            raise ValueError("La fecha prevista es obligatoria.")
        if not isinstance(prueba, EntityPrueba):
            raise ValueError("La solicitud debe vincularse a una instancia de EntityPrueba.")

        # Atributos protegidos según el diagrama UML (-)
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
        """Devuelve la referencia a la prueba médica asociada."""
        return self._prueba

    # --- MÉTODOS MÁGICOS (Identidad DDD) ---

    def __eq__(self, other: object) -> bool:
        """Dos solicitudes son idénticas si tienen el mismo identificador."""
        if not isinstance(other, EntitySolicitud):
            return NotImplemented
        return self._id == other.id

    def __hash__(self) -> int:
        return hash(self._id)

    def __str__(self) -> str:
        """Representación legible para interfaces o logs de aplicación."""
        return f"Solicitud de prueba [{self._fecha_prevista}] (ID: {self._id})"

    def __repr__(self) -> str:
        """Representación técnica para debugging."""
        return f"<EntitySolicitud id={self._id} fecha_prevista={self._fecha_prevista}>"