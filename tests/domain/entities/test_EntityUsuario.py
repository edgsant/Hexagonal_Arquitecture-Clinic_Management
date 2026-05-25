from datetime import date
from werkzeug.security import generate_password_hash

from domain.entities.EntityUsuario import EntityUsuario
from domain.entities.EntityUrologo import EntityUrologo


def test_usuario_valida_credenciales_y_actualiza_campos():
    especialista = EntityUrologo(
        id='uro-7',
        nombre='Hugo',
        apellidos='Adán',
        dni='12345678A',
        fecha_nacimiento=date(1980, 6, 6),
        direccion='Calle Prueba 3',
        telefono='611223344'
    )
    usuario = EntityUsuario(
        id='user-1',
        email='hugo@example.com',
        username='hugo_ad',
        password_hash=generate_password_hash('PasswordSegura123'),
        especialista=especialista
    )

    assert usuario.validar_credenciales('PasswordSegura123') is True
    assert usuario.validar_credenciales('incorrecta') is False
    assert usuario.obtener_datos() is especialista

    usuario.email = 'nuevo@example.com'
    usuario.username = 'nuevo_usuario'

    assert usuario.email == 'nuevo@example.com'
    assert usuario.username == 'nuevo_usuario'
    assert 'nuevo_usuario' in str(usuario)
