from datetime import date
import pytest

from domain.entities.EntityConsulta import EntityConsulta
from domain.entities.EntitySolicitud import EntitySolicitud
from domain.entities.EntityPrueba import EntityPrueba
from domain.entities.EntityAnalistaClinico import EntityAnalistaClinico


def test_registrar_solicitud_en_consulta_y_no_duplicados():
    analista = EntityAnalistaClinico(
        id='ana-3',
        nombre='Pilar',
        apellidos='Nuñez',
        dni='22222222A',
        fecha_nacimiento=date(1982, 8, 8),
        direccion='Calle Prueba 10',
        telefono='611223344'
    )
    consulta = EntityConsulta('cons-3', date.today(), [analista])
    prueba = EntityPrueba('pr-3', date.today(), [analista])
    solicitud = EntitySolicitud('sol-1', date.today(), prueba)

    consulta.registrar_solicitud(solicitud)
    consulta.registrar_solicitud(solicitud)

    assert consulta.solicitudes == [solicitud]
    assert consulta.solicitudes is not solicitud


def test_registrar_solicitud_invalida_levanta_error():
    analista = EntityAnalistaClinico(
        id='ana-4',
        nombre='Javier',
        apellidos='Ruiz',
        dni='33333333B',
        fecha_nacimiento=date(1983, 9, 9),
        direccion='Calle Prueba 11',
        telefono='611223344'
    )
    consulta = EntityConsulta('cons-4', date.today(), [analista])

    with pytest.raises(ValueError):
        consulta.registrar_solicitud('no es una solicitud')
