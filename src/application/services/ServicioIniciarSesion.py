from domain.ports import IRepositorioUsuario
from application.dtos.authDTOs import LoginRequestDTO, LoginResponseDTO

class ServicioIniciarSesion:
    def __init__(self, repo_usuario: IRepositorioUsuario):
        self._repo_usuario = repo_usuario

    def login(self, peticion: LoginRequestDTO) -> LoginResponseDTO:
        # 1. Validación temprana
        if not peticion.identificador or not peticion.password:
            raise ValueError("Credenciales incompletas.")

        # 2. Búsqueda
        usuario = self._repo_usuario.obtener_por_email_o_username(peticion.identificador)
        if usuario is None:
            raise ValueError("Credenciales incorrectas.")

        # 3. Lógica de negocio (Comprobación del texto plano contra el hash)
        if not usuario.validar_credenciales(peticion.password):
            raise ValueError("Credenciales incorrectas.")

        # 4. Preparación de datos
        especialista = usuario.obtener_datos()
        nombre_rol = especialista.__class__.__name__.replace("Entity", "")

        # 5. Retorno
        return LoginResponseDTO(
            usuario_id=usuario.id,
            especialista_id=especialista.id,
            rol=nombre_rol
        )