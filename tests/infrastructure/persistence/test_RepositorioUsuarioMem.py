from domain.entities.EntityUsuario import EntityUsuario
from domain.entities.EntityEspecialista import EntityEspecialista
from werkzeug.security import generate_password_hash


def test_guardar_y_obtener_usuario_por_id(repo_usuario_mem, usuario_entity):
    repo_usuario_mem.guardar_usuario(usuario_entity)

    assert repo_usuario_mem.obtener_por_id(usuario_entity.id) is usuario_entity


def test_obtener_por_email_o_username(repo_usuario_mem, usuario_entity):
    repo_usuario_mem.guardar_usuario(usuario_entity)

    assert repo_usuario_mem.obtener_por_email_o_username(usuario_entity.email) is usuario_entity
    assert repo_usuario_mem.obtener_por_email_o_username(usuario_entity.username) is usuario_entity


def test_obtener_por_email_o_username_devuelve_none_si_no_existe(repo_usuario_mem):
    assert repo_usuario_mem.obtener_por_email_o_username("no-user@example.com") is None


def test_guardar_dos_usuarios_diferentes(repo_usuario_mem, especialista_entity):
    usuario_1 = EntityUsuario(
        id="user-123",
        email="ana.perez@clinica.es",
        username="anaperez",
        password_hash=generate_password_hash("Secret123"),
        especialista=especialista_entity
    )
    usuario_2 = EntityUsuario(
        id="user-456",
        email="luis.garcia@clinica.es",
        username="luisgarcia",
        password_hash=generate_password_hash("Secret456"),
        especialista=especialista_entity
    )

    repo_usuario_mem.guardar_usuario(usuario_1)
    repo_usuario_mem.guardar_usuario(usuario_2)

    assert repo_usuario_mem.obtener_por_id("user-123") is usuario_1
    assert repo_usuario_mem.obtener_por_email_o_username("luisgarcia") is usuario_2
