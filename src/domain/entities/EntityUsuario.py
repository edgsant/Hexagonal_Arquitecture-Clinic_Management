from werkzeug.security import check_password_hash
from .EntityEspecialista import EntityEspecialista

class EntityUsuario:
    """
    Entidad que representa la cuenta de acceso de un especialista al sistema.
    Gestiona la autenticación y mantiene una relación 1:1 con EntityEspecialista.
    """

    def __init__(self, id: str, email: str, username: str, 
                 password_hash: str, especialista: EntityEspecialista):
        
        # Validaciones básicas de negocio
        if not email or "@" not in email:
            raise ValueError("Formato de email inválido.")
        if not username:
            raise ValueError("El username no puede estar vacío.")
        if not especialista:
            raise ValueError("Un usuario debe estar vinculado a un especialista.")

        self._id = id
        self._email = email
        self._username = username
        self._password_hash = password_hash
        self._especialista = especialista


    # --- GETTERS ---
    @property
    def id(self) -> str: return self._id

    @property
    def email(self) -> str: return self._email

    @property
    def username(self) -> str: return self._username

    @property
    def password_hash(self) -> str: return self._password_hash


    # --- SETTERS (Para datos mutables) ---
    @email.setter
    def email(self, nuevo_email: str) -> None:
        if not nuevo_email or "@" not in nuevo_email:
            raise ValueError("Formato de email inválido.")
        self._email = nuevo_email

    @username.setter
    def username(self, nuevo_username: str) -> None:
        if not nuevo_username:
            raise ValueError("El username no puede estar vacío.")
        self._username = nuevo_username


    # --- MÉTODOS DE NEGOCIO (Según el DCD) ---

    def validar_credenciales(self, passwd: str) -> bool:
        """
        Comprueba si la contraseña en texto plano coincide con el hash guardado.
        Equivalente a +validarCredenciales(passwd: string) : boolean
        """
        # Delegamos la comparación segura a werkzeug
        return check_password_hash(self._password_hash, passwd)

    def obtener_datos(self) -> EntityEspecialista:
        """
        Devuelve el especialista asociado a esta cuenta.
        Equivalente a +obtenerDatos() : EntityEspecialista
        """
        return self._especialista


    # --- MÉTODOS MÁGICOS (DDD) ---

    def __eq__(self, other: object) -> bool:
        """Dos cuentas de usuario son idénticas si tienen el mismo ID."""
        if not isinstance(other, EntityUsuario):
            return NotImplemented
        return self._id == other.id

    def __hash__(self) -> int:
        return hash(self._id)
    
    def __str__(self) -> str:
        """Equivalente a toString() para representación humana limpia."""
        return f"Cuenta: {self._username} <{self._email}>"

    def __repr__(self) -> str:
        return f"<EntityUsuario id={self._id} username='{self._username}'>"