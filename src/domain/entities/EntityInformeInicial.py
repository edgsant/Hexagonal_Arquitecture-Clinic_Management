from datetime import date
from .EntityEspecialista import EntityEspecialista

class EntityInformeInicial:
    """
    Entidad que representa el documento clínico de la primera valoración del paciente.
    Es parte del Agregado de Procedimiento.
    Diseñada como inmutable: un informe clínico no se modifica una vez emitido.
    """
    def __init__(self, id: str, fecha: date, antecedentes: str, sintomas: str, 
                 antecedentes_familiares: str, exploracion_fisica: str, autor: EntityEspecialista):
        
        # Validaciones de integridad básicas
        if not id:
            raise ValueError("El informe debe tener un ID válido.")
        if not fecha:
            raise ValueError("La fecha del informe es obligatoria.")
        if not isinstance(autor, EntityEspecialista):
            raise ValueError("El informe debe estar firmado por un Especialista válido.")

        self._id = id
        self._fecha = fecha
        self._antecedentes = antecedentes
        self._sintomas = sintomas
        self._antecedentes_familiares = antecedentes_familiares
        self._exploracion_fisica = exploracion_fisica  # Corregido según el DCD
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
        """Regla DDD: Dos informes son el mismo si tienen el mismo ID."""
        if not isinstance(other, EntityInformeInicial):
            return NotImplemented
        return self._id == other.id

    def __hash__(self) -> int:
        return hash(self._id)

    def __str__(self) -> str:
        """Representación amigable para interfaces."""
        return f"Informe Inicial [{self._fecha}] - Autor: {self._autor.nombre} {self._autor.apellidos}"

    def __repr__(self) -> str:
        """Representación técnica para debugging."""
        return f"<EntityInformeInicial id={self._id} fecha={self._fecha}>"