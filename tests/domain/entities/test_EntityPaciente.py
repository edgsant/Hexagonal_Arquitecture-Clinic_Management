from datetime import date, timedelta
import pytest

from domain.entities.EntityPaciente import EntityPaciente


def test_crear_paciente_valido():
    paciente = EntityPaciente(
        id='pac-1',
        dni='12345678A',
        fecha_nacimiento=date(1985, 10, 12),
        nombre='Alejandro',
        apellidos='Sanz',
        direccion='Calle de la Salud 4',
        telefono='+34611223344'
    )

    assert paciente.id == 'pac-1'
    assert paciente.dni == '12345678A'
    assert paciente.nombre == 'Alejandro'
    assert paciente.apellidos == 'Sanz'
    assert paciente.direccion == 'Calle de la Salud 4'
    assert paciente.telefono == '+34611223344'
    assert 'Alejandro Sanz' in str(paciente)


def test_crear_paciente_dni_invalido_levanta_error():
    with pytest.raises(ValueError):
        EntityPaciente(
            id='pac-2',
            dni='1234A',
            fecha_nacimiento=date(1985, 10, 12),
            nombre='Laura',
            apellidos='Pérez',
            direccion='Calle Falsa 123',
            telefono='611223344'
        )


def test_crear_paciente_fecha_nacimiento_futura_levanta_error():
    with pytest.raises(ValueError):
        EntityPaciente(
            id='pac-3',
            dni='87654321B',
            fecha_nacimiento=date.today() + timedelta(days=1),
            nombre='María',
            apellidos='Gómez',
            direccion='Calle Falsa 123',
            telefono='611223344'
        )


def test_telefono_invalido_levanta_error():
    paciente = EntityPaciente(
        id='pac-4',
        dni='12345678B',
        fecha_nacimiento=date(1990, 1, 1),
        nombre='Pablo',
        apellidos='López',
        direccion='Avda. Siempre Viva 20',
        telefono='611223344'
    )

    with pytest.raises(ValueError):
        paciente.telefono = '12345'


def test_paciente_es_igual_por_id():
    paciente_1 = EntityPaciente(
        id='pac-5',
        dni='12345678C',
        fecha_nacimiento=date(1970, 7, 7),
        nombre='José',
        apellidos='Martínez',
        direccion='Calle Mayor 1',
        telefono='911223344'
    )
    paciente_2 = EntityPaciente(
        id='pac-5',
        dni='87654321C',
        fecha_nacimiento=date(1971, 8, 8),
        nombre='José',
        apellidos='Martínez',
        direccion='Calle Mayor 1',
        telefono='911223344'
    )

    assert paciente_1 == paciente_2
    assert hash(paciente_1) == hash(paciente_2)
