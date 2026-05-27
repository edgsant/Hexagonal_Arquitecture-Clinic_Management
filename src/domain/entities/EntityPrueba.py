from datetime import date
from .EntityActoClinico import EntityActoClinico
from .EntityEspecialista import EntityEspecialista


class EntityPrueba(EntityActoClinico):
    """
    Entidad que representa una prueba médica dentro de un procedimiento.
    Hereda de EntityActoClinico y añade el estado de pendiente/completada.
    """

    def __init__(
        self,
        id: str,
        fecha: date,
        especialistas: list[EntityEspecialista],
        pendiente: bool = True
    ):
        # Llamamos al superconstructor de la clase padre
        super().__init__(id, fecha, especialistas)

        # Comprobación del estado de la prueba
        # El atributo pendiente debe ser booleano porque representa si la prueba
        # todavía está pendiente de completarse o ya ha sido realizada/informada.
        if not isinstance(pendiente, bool):
            raise ValueError("El estado pendiente debe ser un valor booleano.")

        # Asignación del estado interno de la prueba
        self._pendiente = pendiente

    # --- GETTERS ---

    @property
    def pendiente(self) -> bool:
        return self._pendiente

    # --- MÉTODOS DE NEGOCIO ---

    def marcar_completada(self, especialista: EntityEspecialista) -> None:
        """
        Marca la prueba como completada y registra el especialista responsable.

        Una prueba solo puede completarse una vez. Además, el especialista recibido
        debe ser una instancia válida de EntityEspecialista.
        """
        # Comprobación del estado antes de modificar la entidad
        if not self._pendiente:
            raise ValueError("La prueba ya está completada.")

        # Comprobación defensiva del especialista antes de cambiar el estado.
        # Esto evita que la prueba quede completada si el especialista no es válido.
        if not isinstance(especialista, EntityEspecialista):
            raise ValueError("Debe ser una instancia de EntityEspecialista.")

        # Se registra el especialista responsable de completar la prueba
        self.anadir_especialista(especialista)

        # Finalmente, una vez superadas las validaciones, se actualiza el estado
        self._pendiente = False

    # Nota: Los métodos mágicos __eq__, __hash__ y __repr__
    # se heredan de EntityActoClinico basados en su identificador.