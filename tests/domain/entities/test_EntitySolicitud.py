from datetime import date
import pytest

from domain.entities.EntitySolicitud import EntitySolicitud
from domain.entities.EntityPrueba import EntityPrueba
from domain.entities.EntityAnalistaClinico import EntityAnalistaClinico


def crear_analista(
    id='ana-1',
    nombre='Lucía',
    apellidos='Díaz',
    dni='66666666F',
    fecha_nacimiento=date(1986, 4, 4),
    direccion='Calle Salud 2',
    telefono='611223344'
):
    return EntityAnalistaClinico(
        id=id,
        nombre=nombre,
        apellidos=apellidos,
        dni=dni,
        fecha_nacimiento=fecha_nacimiento,
        direccion=direccion,
        telefono=telefono
    )


def crear_prueba(
    id='pr-1',
    fecha=date(2025, 7, 10),
    especialistas=None,
    pendiente=True
):
    if especialistas is None:
        especialistas = [crear_analista()]

    return EntityPrueba(
        id=id,
        fecha=fecha,
        especialistas=especialistas,
        pendiente=pendiente
    )


def crear_solicitud(
    id='sol-1',
    fecha_prevista=date(2025, 7, 15),
    prueba=None
):
    if prueba is None:
        prueba = crear_prueba()

    return EntitySolicitud(
        id=id,
        fecha_prevista=fecha_prevista,
        prueba=prueba
    )


def test_crear_solicitud_valida():
    prueba = crear_prueba()
    fecha_prevista = date(2025, 7, 15)

    solicitud = crear_solicitud(
        id='sol-1',
        fecha_prevista=fecha_prevista,
        prueba=prueba
    )

    assert solicitud.id == 'sol-1'
    assert solicitud.fecha_prevista == fecha_prevista
    assert solicitud.prueba is prueba


def test_crear_solicitud_con_id_vacio_lanza_error():
    with pytest.raises(ValueError):
        crear_solicitud(id='')


def test_crear_solicitud_con_fecha_prevista_vacia_lanza_error():
    with pytest.raises(ValueError):
        crear_solicitud(fecha_prevista=None)


def test_crear_solicitud_con_prueba_invalida_lanza_error():
    with pytest.raises(ValueError):
        crear_solicitud(prueba='no es prueba')


def test_dos_solicitudes_con_mismo_id_son_iguales():
    solicitud_1 = crear_solicitud(
        id='sol-igual',
        prueba=crear_prueba(id='pr-1')
    )

    solicitud_2 = crear_solicitud(
        id='sol-igual',
        prueba=crear_prueba(id='pr-2')
    )

    assert solicitud_1 == solicitud_2


def test_dos_solicitudes_con_distinto_id_no_son_iguales():
    solicitud_1 = crear_solicitud(id='sol-1')
    solicitud_2 = crear_solicitud(id='sol-2')

    assert solicitud_1 != solicitud_2


def test_solicitud_no_se_compara_con_otro_tipo():
    solicitud = crear_solicitud()

    assert solicitud.__eq__('no es solicitud') is NotImplemented


def test_hash_depende_del_id():
    solicitud_1 = crear_solicitud(
        id='sol-hash',
        prueba=crear_prueba(id='pr-1')
    )

    solicitud_2 = crear_solicitud(
        id='sol-hash',
        prueba=crear_prueba(id='pr-2')
    )

    assert hash(solicitud_1) == hash(solicitud_2)


def test_str_contiene_id_y_fecha_prevista():
    fecha_prevista = date(2025, 7, 15)

    solicitud = crear_solicitud(
        id='sol-str',
        fecha_prevista=fecha_prevista
    )

    representacion = str(solicitud)

    assert 'Solicitud sol-str' in representacion
    assert str(fecha_prevista) in representacion


def test_repr_contiene_nombre_de_clase_id_y_fecha_prevista():
    fecha_prevista = date(2025, 7, 15)

    solicitud = crear_solicitud(
        id='sol-repr',
        fecha_prevista=fecha_prevista
    )

    representacion = repr(solicitud)

    assert 'EntitySolicitud' in representacion
    assert 'sol-repr' in representacion
    assert str(fecha_prevista) in representacion