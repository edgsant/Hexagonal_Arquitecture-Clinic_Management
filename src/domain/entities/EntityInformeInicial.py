from datetime import date
from .EntityEspecialista import EntityEspecialista


class EntityInformeInicial:
    """
    Entidad que representa el documento clínico de la primera valoración del paciente.
    Es parte del Agregado de Procedimiento.
    Diseñada como inmutable: un informe clínico no se modifica una vez emitido.
    """

    def __init__(
        self,
        id: str,
        fecha: date,
        antecedentes: str,
        sintomas: str,
        antecedentes_familiares: str,
        exploracion_fisica: str,
        autor: EntityEspecialista
    ):
        # Comprobaciones de identidad y fecha obligatorias
        if not id:
            raise ValueError("El informe debe tener un ID válido.")

        if not fecha:
            raise ValueError("La fecha del informe es obligatoria.")

        # Comprobaciones de contenido clínico obligatorio
        # Al tratarse de un informe clínico inicial, no debe crearse vacío.
        if not antecedentes or len(antecedentes.strip()) == 0:
            raise ValueError("Los antecedentes no pueden estar vacíos.")

        if not sintomas or len(sintomas.strip()) == 0:
            raise ValueError("Los síntomas no pueden estar vacíos.")

        if not antecedentes_familiares or len(antecedentes_familiares.strip()) == 0:
            raise ValueError("Los antecedentes familiares no pueden estar vacíos.")

        if not exploracion_fisica or len(exploracion_fisica.strip()) == 0:
            raise ValueError("La exploración física no puede estar vacía.")

        # Comprobación del especialista responsable del informe
        if not isinstance(autor, EntityEspecialista):
            raise ValueError("El informe debe estar firmado por un Especialista válido.")

        # Asignación de atributos internos
        self._id = id
        self._fecha = fecha
        self._antecedentes = antecedentes.strip()
        self._sintomas = sintomas.strip()
        self._antecedentes_familiares = antecedentes_familiares.strip()
        self._exploracion_fisica = exploracion_fisica.strip()
        self._autor = autor

    # --- GETTERS (Sin setters para garantizar inmutabilidad clínica) ---

    @property
    def id(self) -> str:
        return self._id

    @property
    def fecha(self) -> date:
        return self._fecha

    @property
    def antecedentes(self) -> str:
        return self._antecedentes

    @property
    def sintomas(self) -> str:
        return self._sintomas

    @property
    def antecedentes_familiares(self) -> str:
        return self._antecedentes_familiares

    @property
    def exploracion_fisica(self) -> str:
        return self._exploracion_fisica

    @property
    def autor(self) -> EntityEspecialista:
        return self._autor

    # --- MÉTODOS MÁGICOS (Identidad DDD) ---

    def __eq__(self, other: object) -> bool:
        """
        Regla DDD: Dos informes son el mismo si tienen el mismo ID.
        """
        if not isinstance(other, EntityInformeInicial):
            return NotImplemented

        return self._id == other.id

    def __hash__(self) -> int:
        return hash(self._id)

    def __str__(self) -> str:
        """
        Representación amigable para interfaces.
        """
        return f"Informe Inicial [{self._fecha}] - Autor: {self._autor.nombre} {self._autor.apellidos}"

    def __repr__(self) -> str:
        """
        Representación técnica para debugging.
        """
        return f"<EntityInformeInicial id={self._id} fecha={self._fecha}>"