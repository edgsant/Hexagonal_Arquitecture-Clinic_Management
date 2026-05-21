from abc import ABC
from datetime import date
import re
class EntityEspecialista(ABC):
    """
    Entidad abstracta que representa a un especialista médico.
    Aplica encapsulamiento Pythónico e igualdad basada en Identidad (DDD).
    """

    # Pre-compilamos los patrones regex para que sea más eficiente en memoria
    _PATRON_DNI = re.compile(r'^\d{8}[A-Za-z]$')
    _PATRON_TELEFONO = re.compile(r'^(?:\+34|0034)?[6789]\d{8}$') # Admite +34 y 9 dígitos
    
    def __init__(self, id: str, nombre: str, apellidos: str, dni: str, 
                 fecha_nacimiento: date, direccion: str, telefono: str):
        
        # 1. Validamos los atributos inmutables al nacer
        if not self._PATRON_DNI.match(dni):
            raise ValueError(f"Formato de DNI inválido: {dni}")
        if not fecha_nacimiento:
            raise ValueError("La fecha de nacimiento no puede estar vacía")

        self._id = id
        self._dni = dni
        self._fecha_nacimiento = fecha_nacimiento
        
        # 2. Asignamos los mutables usando SUS PROPIOS SETTERS para aprovechar su validación
        self.nombre = nombre
        self.apellidos = apellidos
        self.direccion = direccion
        self.telefono = telefono



    # --- GETTERS (Estilo Python usando @property) ---
    
    @property
    def id(self) -> str:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def apellidos(self) -> str:
        return self._apellidos

    @property
    def dni(self) -> str:
        return self._dni

    @property
    def fecha_nacimiento(self) -> date:
        return self._fecha_nacimiento

    @property
    def direccion(self) -> str:
        return self._direccion

    @property
    def telefono(self) -> str:
        return self._telefono

    # --- SETTERS (Solo para lo que puede cambiar en la vida real) ---
    
    @nombre.setter
    def nombre(self, nuevo_nombre: str) -> None:
        if not nuevo_nombre or len(nuevo_nombre.strip()) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres útiles.")
        self._nombre = nuevo_nombre.strip()

    @apellidos.setter
    def apellidos(self, nuevos_apellidos: str) -> None:
        if not nuevos_apellidos or len(nuevos_apellidos.strip()) < 2:
            raise ValueError("Los apellidos deben tener al menos 2 caracteres útiles.")
        self._apellidos = nuevos_apellidos.strip()

    @direccion.setter
    def direccion(self, nueva_direccion: str) -> None:
        if not nueva_direccion or len(nueva_direccion.strip()) < 5:
            raise ValueError("La dirección es demasiado corta para ser válida.")
        self._direccion = nueva_direccion.strip()

    @telefono.setter
    def telefono(self, nuevo_telefono: str) -> None:
        # Validación con Expresión Regular para el teléfono
        if not self._PATRON_TELEFONO.match(nuevo_telefono):
            raise ValueError(f"Formato de teléfono inválido: {nuevo_telefono}")
        self._telefono = nuevo_telefono

    # --- MÉTODOS MÁGICOS (Equivalentes a equals, hashCode y toString) ---

    def __eq__(self, other: object) -> bool:
        """
        Regla DDD: Dos entidades son idénticas si tienen el mismo ID, 
        independientemente del resto de sus atributos.
        """
        if not isinstance(other, EntityEspecialista):
            return NotImplemented
        return self._id == other.id

    def __hash__(self) -> int:
        """Necesario para usar la entidad en Sets o como clave de Diccionario."""
        return hash(self._id)

    def __str__(self) -> str:
        """Equivalente a toString() para interfaces de usuario o print()."""
        return f"{self._nombre} {self._apellidos} (DNI: {self._dni})"

    def __repr__(self) -> str:
        """Representación técnica para debugging y logs."""
        return f"<EntityEspecialista id={self._id} nombre='{self._nombre}'>"