from datetime import date
import pytest

from domain.entities.EntityEspecialista import EntityEspecialista


def test_crear_especialista_valido():
    especialista = EntityEspecialista(
        id='esp-1',
        nombre='Laura',
        apellidos='García',
        dni='12345678A',
        fecha_nacimiento=date(1980, 5, 15),
        direccion='Calle del Río 10',
        telefono='+34611223344'
    )

    assert especialista.id == 'esp-1'
    assert especialista.nombre == 'Laura'
    assert especialista.apellidos == 'García'
    assert especialista.dni == '12345678A'
    assert especialista.telefono == '+34611223344'
    assert 'Laura García' in str(especialista)


def test_especialista_dni_invalido_levanta_error():
    with pytest.raises(ValueError):
        EntityEspecialista(
            id='esp-2',
            nombre='Ana',
            apellidos='Ruiz',
            dni='1234X',
            fecha_nacimiento=date(1985, 5, 15),
            direccion='Calle Luna 2',
            telefono='611223344'
        )


def test_especialista_setters_validan_campos():
    especialista = EntityEspecialista(
        id='esp-3',
        nombre='Carlos',
        apellidos='Santos',
        dni='87654321B',
        fecha_nacimiento=date(1975, 10, 23),
        direccion='Calle Sol 12',
        telefono='611223344'
    )

    especialista.nombre = 'Carlos Alberto'
    especialista.apellidos = 'Santos Pérez'
    especialista.direccion = 'Avenida Principal 3'
    especialista.telefono = '+34611223344'

    assert especialista.nombre == 'Carlos Alberto'
    assert especialista.apellidos == 'Santos Pérez'
    assert especialista.direccion == 'Avenida Principal 3'
    assert especialista.telefono == '+34611223344'


def test_especialista_es_igual_por_id():
    primero = EntityEspecialista(
        id='esp-4',
        nombre='Marta',
        apellidos='Domínguez',
        dni='11111111A',
        fecha_nacimiento=date(1982, 11, 1),
        direccion='Calle Real 7',
        telefono='611223344'
    )
    segundo = EntityEspecialista(
        id='esp-4',
        nombre='Marta',
        apellidos='Domínguez',
        dni='22222222B',
        fecha_nacimiento=date(1982, 11, 1),
        direccion='Calle Real 7',
        telefono='611223344'
    )

    assert primero == segundo
    assert hash(primero) == hash(segundo)
