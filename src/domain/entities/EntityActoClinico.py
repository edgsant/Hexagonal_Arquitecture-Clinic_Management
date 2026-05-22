from abc import ABC
from datetime import date
from .EntityEspecialista import EntityEspecialista

class EntityActoClinico(ABC):
    """
    Clase base abstracta para todos los actos médicos de un procedimiento.
    Soporta múltiples especialistas (1..*) y protege su integridad (DDD).
    """
    def __init__(self, id: str, fecha: date, especialistas: list[EntityEspecialista]):
        if not id:
            raise ValueError("El acto clínico debe tener un ID válido.")
        if not fecha:
            raise ValueError("La fecha es obligatoria.")
        if not especialistas:
            raise ValueError("Un acto clínico debe tener al menos un especialista asignado.")
            
        self._id = id
        self._fecha = fecha
        # Guardamos una copia interna de la lista para evitar que referencias externas la muten
        self._especialistas = list(especialistas)

    # --- GETTERS ---

    @property
    def id(self) -> str:
        return self._id

    @property
    def fecha(self) -> date:
        return self._fecha

    @property
    def especialistas(self) -> list[EntityEspecialista]:
        """
        Devolvemos una copia de la lista. 
        Si alguien quiere añadir uno, debe usar el método anadir_especialista().
        """
        return list(self._especialistas)

    # --- COMPORTAMIENTO DEL DOMINIO ---

    def anadir_especialista(self, especialista: EntityEspecialista) -> None:
        """Añade un especialista garantizando la integridad de los datos."""
        if not isinstance(especialista, EntityEspecialista):
            raise ValueError("Debe ser una instancia de EntityEspecialista.")
        
        if especialista not in self._especialistas:
            self._especialistas.append(especialista)

    # --- MÉTODOS MÁGICOS (Identidad DDD) ---

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EntityActoClinico):
            return NotImplemented
        return self._id == other.id

    def __hash__(self) -> int:
        return hash(self._id)

    def __repr__(self) -> str:
        # __class__.__name__ imprimirá dinámicamente "EntityConsulta" o "EntityPrueba"
        return f"<{self.__class__.__name__} id={self._id} fecha={self._fecha}>"