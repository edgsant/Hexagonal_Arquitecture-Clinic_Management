from datetime import date
from .EntityActoClinico import EntityActoClinico
from .EntityEspecialista import EntityEspecialista
from .EntitySolicitud import EntitySolicitud


class EntityConsulta(EntityActoClinico):
    """
    Entidad que representa una consulta médica.
    Hereda de EntityActoClinico y actúa como contenedor de múltiples
    solicitudes de pruebas médicas.
    """

    def __init__(self, id: str, fecha: date, especialistas: list[EntityEspecialista]):
        # Llamamos al superconstructor de la clase padre
        super().__init__(id, fecha, especialistas)

        # Inicializamos la lista de solicitudes encapsulada y protegida
        self._solicitudes: list[EntitySolicitud] = []

    # --- GETTERS ---

    @property
    def solicitudes(self) -> list[EntitySolicitud]:
        """
        Devuelve una copia de la lista.
        Garantiza que nadie pueda mutar la colección desde fuera sin usar
        los métodos de negocio.
        """
        return list(self._solicitudes)

    # --- MÉTODOS DE NEGOCIO ---

    def registrar_solicitud(self, solicitud: EntitySolicitud) -> None:
        """
        Registra una solicitud de prueba médica surgida durante esta consulta.
        """
        # Validación defensiva de tipos
        if not isinstance(solicitud, EntitySolicitud):
            raise ValueError("Solo se pueden registrar instancias válidas de EntitySolicitud.")

        # Evitamos duplicados indeseados
        if solicitud not in self._solicitudes:
            self._solicitudes.append(solicitud)

    # Nota: Los métodos mágicos __eq__, __hash__ y __repr__
    # se heredan de EntityActoClinico basados en su identificador.