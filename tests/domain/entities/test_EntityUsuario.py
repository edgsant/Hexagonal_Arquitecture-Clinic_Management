from datetime import date
import pytest
from werkzeug.security import generate_password_hash

from domain.entities.EntityUsuario import EntityUsuario
from domain.entities.EntityUrologo import EntityUrologo
from domain.entities.EntityEspecialista import EntityEspecialista


def crear_especialista(
    id='uro-7',
    nombre='Hugo',
    apellidos='Adán',
    dni='12345678A',
    fecha_nacimiento=date(1980, 6, 6),
    direccion='Calle Prueba 3',
    telefono='611223344'
):
    return EntityUrologo(
        id=id,
        nombre=nombre,
        apellidos=apellidos,
        dni=dni,
        fecha_nacimiento=fecha_nacimiento,
        direccion=direccion,
        telefono=telefono
    )


def crear_usuario(
    id='user-1',
    email='hugo@example.com',
    username='hugo_ad',
    password_hash=None,
    especialista=None
):
    if password_hash is None:
        password_hash = generate_password_hash('PasswordSegura123')

    if especialista is None:
        especialista = crear_especialista()

    return EntityUsuario(
        id=id,
        email=email,
        username=username,
        password_hash=password_hash,
        especialista=especialista
    )


def test_crear_usuario_valido():
    especialista = crear_especialista()
    password_hash = generate_password_hash('PasswordSegura123')

    usuario = crear_usuario(
        id='user-1',
        email='hugo@example.com',
        username='hugo_ad',
        password_hash=password_hash,
        especialista=especialista
    )

    assert usuario.id == 'user-1'
    assert usuario.email == 'hugo@example.com'
    assert usuario.username == 'hugo_ad'
    assert usuario.password_hash == password_hash
    assert usuario.obtener_datos() is especialista


def test_crear_usuario_con_id_vacio_lanza_error():
    with pytest.raises(ValueError):
        crear_usuario(id='')


def test_crear_usuario_con_email_vacio_lanza_error():
    with pytest.raises(ValueError):
        crear_usuario(email='')


def test_crear_usuario_con_email_sin_arroba_lanza_error():
    with pytest.raises(ValueError):
        crear_usuario(email='hugoexample.com')


def test_crear_usuario_con_username_vacio_lanza_error():
    with pytest.raises(ValueError):
        crear_usuario(username='')


def test_crear_usuario_con_username_solo_espacios_lanza_error():
    with pytest.raises(ValueError):
        crear_usuario(username='   ')


def test_crear_usuario_con_password_hash_vacio_lanza_error():
    with pytest.raises(ValueError):
        crear_usuario(password_hash='')


def test_crear_usuario_sin_especialista_lanza_error():
    with pytest.raises(ValueError):
        EntityUsuario(
            id='user-1',
            email='hugo@example.com',
            username='hugo_ad',
            password_hash=generate_password_hash('PasswordSegura123'),
            especialista=None
        )


def test_crear_usuario_con_especialista_invalido_lanza_error():
    with pytest.raises(ValueError):
        crear_usuario(especialista='no es especialista')


def test_usuario_limpia_espacios_laterales_en_email_y_username():
    usuario = crear_usuario(
        email='  hugo@example.com  ',
        username='  hugo_ad  '
    )

    assert usuario.email == 'hugo@example.com'
    assert usuario.username == 'hugo_ad'


def test_validar_credenciales_correctas_devuelve_true():
    usuario = crear_usuario(
        password_hash=generate_password_hash('PasswordSegura123')
    )

    assert usuario.validar_credenciales('PasswordSegura123') is True


def test_validar_credenciales_incorrectas_devuelve_false():
    usuario = crear_usuario(
        password_hash=generate_password_hash('PasswordSegura123')
    )

    assert usuario.validar_credenciales('incorrecta') is False


def test_obtener_datos_devuelve_especialista_asociado():
    especialista = crear_especialista()
    usuario = crear_usuario(especialista=especialista)

    assert usuario.obtener_datos() is especialista
    assert isinstance(usuario.obtener_datos(), EntityEspecialista)


def test_setter_email_valido_modifica_email():
    usuario = crear_usuario()

    usuario.email = 'nuevo@example.com'

    assert usuario.email == 'nuevo@example.com'


def test_setter_username_valido_modifica_username():
    usuario = crear_usuario()

    usuario.username = 'nuevo_usuario'

    assert usuario.username == 'nuevo_usuario'


def test_setter_email_elimina_espacios_laterales():
    usuario = crear_usuario()

    usuario.email = '  nuevo@example.com  '

    assert usuario.email == 'nuevo@example.com'


def test_setter_username_elimina_espacios_laterales():
    usuario = crear_usuario()

    usuario.username = '  nuevo_usuario  '

    assert usuario.username == 'nuevo_usuario'


def test_setter_email_invalido_no_modifica_valor_anterior():
    usuario = crear_usuario()

    with pytest.raises(ValueError):
        usuario.email = 'email_invalido'

    assert usuario.email == 'hugo@example.com'


def test_setter_username_invalido_no_modifica_valor_anterior():
    usuario = crear_usuario()

    with pytest.raises(ValueError):
        usuario.username = ''

    assert usuario.username == 'hugo_ad'


def test_dos_usuarios_con_mismo_id_son_iguales():
    usuario_1 = crear_usuario(
        id='user-igual',
        email='primero@example.com',
        username='primero'
    )

    usuario_2 = crear_usuario(
        id='user-igual',
        email='segundo@example.com',
        username='segundo',
        especialista=crear_especialista(
            id='uro-8',
            dni='87654321B',
            nombre='Ana',
            apellidos='Sánchez',
            direccion='Calle Segunda 8'
        )
    )

    assert usuario_1 == usuario_2


def test_dos_usuarios_con_distinto_id_no_son_iguales():
    usuario_1 = crear_usuario(id='user-1')
    usuario_2 = crear_usuario(id='user-2')

    assert usuario_1 != usuario_2


def test_usuario_no_se_compara_con_otro_tipo():
    usuario = crear_usuario()

    assert usuario.__eq__('no es usuario') is NotImplemented


def test_hash_depende_del_id():
    usuario_1 = crear_usuario(id='user-hash')
    usuario_2 = crear_usuario(
        id='user-hash',
        email='otro@example.com',
        username='otro'
    )

    assert hash(usuario_1) == hash(usuario_2)


def test_str_contiene_username_y_email():
    usuario = crear_usuario()

    representacion = str(usuario)

    assert 'Cuenta: hugo_ad' in representacion
    assert 'hugo@example.com' in representacion


def test_repr_contiene_nombre_de_clase_id_y_username():
    usuario = crear_usuario()

    representacion = repr(usuario)

    assert 'EntityUsuario' in representacion
    assert 'user-1' in representacion
    assert 'hugo_ad' in representacion