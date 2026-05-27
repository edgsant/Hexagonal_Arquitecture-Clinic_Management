from datetime import date
import pytest

from domain.entities.EntityConsulta import EntityConsulta
from domain.entities.EntitySolicitud import EntitySolicitud
from domain.entities.EntityPrueba import EntityPrueba
from domain.entities.EntityAnalistaClinico import EntityAnalistaClinico


def crear_analista(
    id='ana-1',
    nombre='Pilar',
    apellidos='Nuñez',
    dni='22222222A',
    fecha_nacimiento=date(1982, 8, 8),
    direccion='Calle Prueba 10',
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


def crear_consulta(
    id='cons-1',
    fecha=date(2025, 3, 10),
    especialistas=None
):
    if especialistas is None:
        especialistas = [crear_analista()]

    return EntityConsulta(
        id=id,
        fecha=fecha,
        especialistas=especialistas
    )


def crear_prueba(
    id='pr-1',
    fecha=date(2025, 3, 15),
    especialistas=None
):
    if especialistas is None:
        especialistas = [crear_analista()]

    return EntityPrueba(
        id=id,
        fecha=fecha,
        especialistas=especialistas
    )


def crear_solicitud(
    id='sol-1',
    fecha_prevista=date(2025, 3, 20),
    prueba=None
):
    if prueba is None:
        prueba = crear_prueba()

    return EntitySolicitud(
        id=id,
        fecha_prevista=fecha_prevista,
        prueba=prueba
    )


def test_crear_consulta_valida():
    analista = crear_analista()
    fecha = date(2025, 3, 10)

    consulta = crear_consulta(
        id='cons-1',
        fecha=fecha,
        especialistas=[analista]
    )

    assert consulta.id == 'cons-1'
    assert consulta.fecha == fecha
    assert consulta.especialistas == [analista]
    assert consulta.solicitudes == []


def test_crear_consulta_con_id_vacio_lanza_error():
    with pytest.raises(ValueError):
        crear_consulta(id='')


def test_crear_consulta_con_fecha_vacia_lanza_error():
    with pytest.raises(ValueError):
        crear_consulta(fecha=None)


def test_crear_consulta_sin_especialistas_lanza_error():
    with pytest.raises(ValueError):
        crear_consulta(especialistas=[])


def test_crear_consulta_con_especialista_invalido_lanza_error():
    with pytest.raises(ValueError):
        crear_consulta(especialistas=['no es especialista'])


def test_registrar_solicitud_en_consulta():
    consulta = crear_consulta()
    solicitud = crear_solicitud()

    consulta.registrar_solicitud(solicitud)

    assert consulta.solicitudes == [solicitud]


def test_registrar_solicitud_no_duplica_misma_instancia():
    consulta = crear_consulta()
    solicitud = crear_solicitud()

    consulta.registrar_solicitud(solicitud)
    consulta.registrar_solicitud(solicitud)

    assert consulta.solicitudes == [solicitud]
    assert len(consulta.solicitudes) == 1


def test_registrar_solicitud_no_duplica_solicitud_con_mismo_id():
    consulta = crear_consulta()

    solicitud_1 = crear_solicitud(
        id='sol-duplicada',
        prueba=crear_prueba(id='pr-1')
    )

    solicitud_2 = crear_solicitud(
        id='sol-duplicada',
        prueba=crear_prueba(id='pr-2')
    )

    consulta.registrar_solicitud(solicitud_1)
    consulta.registrar_solicitud(solicitud_2)

    assert consulta.solicitudes == [solicitud_1]
    assert len(consulta.solicitudes) == 1


def test_registrar_varias_solicitudes_distintas():
    consulta = crear_consulta()

    solicitud_1 = crear_solicitud(
        id='sol-1',
        prueba=crear_prueba(id='pr-1')
    )

    solicitud_2 = crear_solicitud(
        id='sol-2',
        prueba=crear_prueba(id='pr-2')
    )

    consulta.registrar_solicitud(solicitud_1)
    consulta.registrar_solicitud(solicitud_2)

    assert solicitud_1 in consulta.solicitudes
    assert solicitud_2 in consulta.solicitudes
    assert len(consulta.solicitudes) == 2


def test_registrar_solicitud_invalida_lanza_error():
    consulta = crear_consulta()

    with pytest.raises(ValueError):
        consulta.registrar_solicitud('no es una solicitud')


def test_registrar_solicitud_invalida_no_modifica_lista():
    consulta = crear_consulta()
    solicitud = crear_solicitud()

    consulta.registrar_solicitud(solicitud)

    with pytest.raises(ValueError):
        consulta.registrar_solicitud('no es una solicitud')

    assert consulta.solicitudes == [solicitud]


def test_getter_solicitudes_devuelve_copia_y_no_permite_mutar_lista_interna():
    consulta = crear_consulta()
    solicitud_original = crear_solicitud(id='sol-original')

    consulta.registrar_solicitud(solicitud_original)

    solicitudes_obtenidas = consulta.solicitudes
    solicitud_externa = crear_solicitud(
        id='sol-externa',
        prueba=crear_prueba(id='pr-externa')
    )

    solicitudes_obtenidas.append(solicitud_externa)

    assert consulta.solicitudes == [solicitud_original]
    assert solicitud_externa not in consulta.solicitudes


def test_dos_consultas_con_mismo_id_son_iguales():
    consulta_1 = crear_consulta(id='cons-igual')
    consulta_2 = crear_consulta(id='cons-igual')

    assert consulta_1 == consulta_2


def test_dos_consultas_con_distinto_id_no_son_iguales():
    consulta_1 = crear_consulta(id='cons-1')
    consulta_2 = crear_consulta(id='cons-2')

    assert consulta_1 != consulta_2


def test_consulta_no_se_compara_con_otro_tipo():
    consulta = crear_consulta()

    assert consulta.__eq__('no es consulta') is NotImplemented


def test_hash_depende_del_id():
    consulta_1 = crear_consulta(id='cons-hash')
    consulta_2 = crear_consulta(id='cons-hash')

    assert hash(consulta_1) == hash(consulta_2)


def test_repr_contiene_nombre_de_clase_id_y_fecha():
    fecha = date(2025, 3, 10)
    consulta = crear_consulta(id='cons-repr', fecha=fecha)

    representacion = repr(consulta)

    assert 'EntityConsulta' in representacion
    assert 'cons-repr' in representacion
    assert str(fecha) in representacion