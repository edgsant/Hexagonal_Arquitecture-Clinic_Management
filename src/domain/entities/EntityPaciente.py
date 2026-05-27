from datetime import date
import re


class EntityPaciente:
    """
    Entidad (Aggregate Root) que representa a un paciente de la clínica.
    Aplica encapsulamiento, inmutabilidad de identidad y validación global (DDD).
    """

    _PATRON_DNI = re.compile(r'^\d{8}[A-Za-z]$')
    _PATRON_TELEFONO = re.compile(r'^(?:\+34|0034)?[6789]\d{8}$')

    def __init__(
        self,
        id: str,
        dni: str,
        fecha_nacimiento: date,
        nombre: str,
        apellidos: str,
        direccion: str,
        telefono: str
    ):
        # Comprobación de identidad obligatoria
        # El ID es la identidad de la entidad y se utiliza en __eq__ y __hash__.
        if not id:
            raise ValueError("El paciente debe tener un ID válido.")

        # Comprobación de atributos inmutables obligatorios
        if not dni:
            raise ValueError("El DNI no puede estar vacío.")

        if not fecha_nacimiento:
            raise ValueError("La fecha de nacimiento no puede estar vacía.")

        # Asignación de atributos internos inmutables
        self._id = id
        self._dni = dni
        self._fecha_nacimiento = fecha_nacimiento

        # Asignamos los mutables usando sus setters para pre-validar
        self.nombre = nombre
        self.apellidos = apellidos
        self.direccion = direccion
        self.telefono = telefono

        # Cumplimos explícitamente con el DCD: validación global al nacer
        if not self.validar_datos():
            raise ValueError("Los datos del paciente no superan las reglas de negocio globales.")

    # --- GETTERS ---

    @property
    def id(self) -> str:
        return self._id

    @property
    def dni(self) -> str:
        return self._dni

    @property
    def fecha_nacimiento(self) -> date:
        return self._fecha_nacimiento

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def apellidos(self) -> str:
        return self._apellidos

    @property
    def direccion(self) -> str:
        return self._direccion

    @property
    def telefono(self) -> str:
        return self._telefono

    # --- SETTERS (Datos mutables en la vida real) ---

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or len(valor.strip()) < 2:
            raise ValueError("El nombre es inválido.")

        self._nombre = valor.strip()

    @apellidos.setter
    def apellidos(self, valor: str) -> None:
        if not valor or len(valor.strip()) < 2:
            raise ValueError("Los apellidos son inválidos.")

        self._apellidos = valor.strip()

    @direccion.setter
    def direccion(self, valor: str) -> None:
        if not valor:
            raise ValueError("La dirección no puede estar vacía.")

        self._direccion = valor.strip()

    @telefono.setter
    def telefono(self, valor: str) -> None:
        if not self._PATRON_TELEFONO.match(valor):
            raise ValueError("Formato de teléfono inválido.")

        self._telefono = valor

    # --- MÉTODOS DE NEGOCIO (DCD) ---

    def validar_datos(self) -> bool:
        """
        +validarDatos() : boolean
        Comprueba reglas de negocio globales del paciente (invariantes complejas).
        """
        # Validación 1: El DNI debe tener un formato válido
        if not self._PATRON_DNI.match(self._dni):
            return False

        # Validación 2: La fecha de nacimiento no puede ser en el futuro
        if self._fecha_nacimiento > date.today():
            return False

        return True

    # --- MÉTODOS MÁGICOS (Identidad DDD) ---

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EntityPaciente):
            return NotImplemented

        return self._id == other.id

    def __hash__(self) -> int:
        return hash(self._id)

    def __str__(self) -> str:
        return f"{self._nombre} {self._apellidos} (DNI: {self._dni})"

    def __repr__(self) -> str:
        return f"<EntityPaciente id={self._id} dni='{self._dni}'>"