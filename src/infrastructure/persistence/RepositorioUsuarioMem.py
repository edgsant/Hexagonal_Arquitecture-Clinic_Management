from domain.entities.EntityUsuario import EntityUsuario

class RepositorioUsuarioMem:
    """
    Repositorio en memoria para usuarios.

    Implementa la interfaz RepositorioUsuario usando un diccionario en memoria.
    """
    def __init__(self):
        """
        Inicializa el repositorio con un diccionario vacío para cada tipo de clave.
        """
        self.usuarios_por_email = {}
        self.usuarios_por_username = {}
        self.usuarios_por_id = {}
    
    def guardar_usuario(self, usuario: EntityUsuario):
        """
        Agrega un paciente a los repositorios.

        Args:
            usuario: El usuario que se va aguardar.
        """
        self.usuarios_por_email[usuario.email] = usuario
        self.usuarios_por_username[usuario.username] = usuario
        self.usuarios_por_id[usuario.id] = usuario

    def obtener_por_id(self, usuario_id: str):
        """
        Obtiene un usuario por su DNI.

        Args:
            usuario_dni: DNI del usuario.

        Returns:
            Usuario or None: El usuario si existe, None en caso contrario.
        """
        return self.usuarios_por_id.get(usuario_id)
    
    def obtener_por_email_o_username(self, identificador: str):
        """
        Obtiene un usuario por email o nombre de usuario indistintamente

        Args:
            identificador: email o nombre de usuario del usuario

        Returns:
            Usuario or None: El usuario si existe, None en caso contrario.
        """
        usuario = self.usuarios_por_email.get(identificador)

        if usuario is not None:
            return usuario

        return self.usuarios_por_username.get(identificador)