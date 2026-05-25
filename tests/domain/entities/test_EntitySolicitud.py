from datetime import date
import pytest

from domain.entities.EntitySolicitud import EntitySolicitud
from domain.entities.EntityPrueba import EntityPrueba
from domain.entities.EntityAnalistaClinico import EntityAnalistaClinico


def test_crear_solicitud_valida_y_str_repr():
    analista = EntityAnalistaClinico(
        id='ana-5',
        nombre='Marta',
        apellidos='Ortiz',
        dni='44444444A',
        fecha_nacimiento=date(1985, 3, 3),
        direccion='Calle Prueba 12',
        telefono='611223344'
    )
    prueba = EntityPrueba('pr-4', date.today(), [analista])
    solicitud = EntitySolicitud('sol-2', date.today(), prueba)

    assert solicitud.prueba is prueba
    assert 'sol-2' in str(solicitud)
    assert 'EntitySolicitud' in repr(solicitud)
    assert solicitud == EntitySolicitud('sol-2', date.today(), prueba)


def test_solicitud_con_prueba_invalida_levanta_error():
    with pytest.raises(ValueError):
        EntitySolicitud('sol-3', date.today(), prueba='no es una prueba')
