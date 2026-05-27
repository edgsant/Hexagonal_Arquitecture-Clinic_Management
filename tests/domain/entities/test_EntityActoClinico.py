from datetime import date
import pytest

from domain.entities.EntityPrueba import EntityPrueba
from domain.entities.EntityAnalistaClinico import EntityAnalistaClinico


def crear_analista(
    id='ana-1',
    nombre='Patricia',
    apellidos='López',
    dni='66666666A',
    fecha_nacimiento=date(1984, 6, 6),
    direccion='Calle Salud 6',
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
    fecha=date(2025, 1, 10),
    especialistas=None
):
    if especialistas is None:
        especialistas = [crear_analista()]

    return EntityPrueba(
        id=id,
        fecha=fecha,
        especialistas=especialistas
    )


def test_crear_acto_clinico_valido():
    fecha = date(2025, 1, 10)
    analista = crear_analista()

    prueba = crear_prueba(
        id='pr-1',
        fecha=fecha,
        especialistas=[analista]
    )

    assert prueba.id == 'pr-1'
    assert prueba.fecha == fecha
    assert prueba.especialistas == [analista]


def test_crear_acto_clinico_con_id_vacio_lanza_error():
    with pytest.raises(ValueError):
        crear_prueba(id='')


def test_crear_acto_clinico_con_fecha_vacia_lanza_error():
    with pytest.raises(ValueError):
        crear_prueba(fecha=None)


def test_crear_acto_clinico_sin_especialistas_lanza_error():
    with pytest.raises(ValueError):
        crear_prueba(especialistas=[])


def test_crear_acto_clinico_con_especialista_invalido_lanza_error():
    with pytest.raises(ValueError):
        crear_prueba(especialistas=['no es especialista'])


def test_crear_acto_clinico_con_lista_mixta_de_especialistas_lanza_error():
    analista = crear_analista()

    with pytest.raises(ValueError):
        crear_prueba(especialistas=[analista, 'no es especialista'])


def test_constructor_copia_lista_de_especialistas_para_evitar_mutacion_externa():
    analista = crear_analista()
    especialistas = [analista]

    prueba = crear_prueba(especialistas=especialistas)

    especialista_nuevo = crear_analista(
        id='ana-2',
        nombre='Andrés',
        apellidos='Delgado',
        dni='77777777B',
        fecha_nacimiento=date(1981, 1, 1),
        direccion='Calle Salud 7'
    )

    especialistas.append(especialista_nuevo)

    assert prueba.especialistas == [analista]
    assert especialista_nuevo not in prueba.especialistas


def test_getter_especialistas_devuelve_copia_y_no_permite_mutar_lista_interna():
    analista = crear_analista()
    prueba = crear_prueba(especialistas=[analista])

    especialistas_obtenidos = prueba.especialistas

    especialista_nuevo = crear_analista(
        id='ana-3',
        nombre='Lucía',
        apellidos='Martín',
        dni='88888888C',
        fecha_nacimiento=date(1980, 2, 2),
        direccion='Calle Salud 8'
    )

    especialistas_obtenidos.append(especialista_nuevo)

    assert prueba.especialistas == [analista]
    assert especialista_nuevo not in prueba.especialistas


def test_anadir_especialista_no_duplica_si_ya_existe():
    analista = crear_analista()
    prueba = crear_prueba(especialistas=[analista])

    prueba.anadir_especialista(analista)

    assert prueba.especialistas == [analista]
    assert len(prueba.especialistas) == 1


def test_anadir_especialista_nuevo():
    analista = crear_analista()
    prueba = crear_prueba(especialistas=[analista])

    especialista_nuevo = crear_analista(
        id='ana-4',
        nombre='Marta',
        apellidos='Santos',
        dni='99999999D',
        fecha_nacimiento=date(1982, 3, 3),
        direccion='Calle Salud 9'
    )

    prueba.anadir_especialista(especialista_nuevo)

    assert especialista_nuevo in prueba.especialistas
    assert len(prueba.especialistas) == 2


def test_anadir_especialista_invalido_lanza_error():
    prueba = crear_prueba()

    with pytest.raises(ValueError):
        prueba.anadir_especialista('no es especialista')


def test_dos_actos_clinicos_con_mismo_id_son_iguales():
    prueba_1 = crear_prueba(id='pr-igual')
    prueba_2 = crear_prueba(id='pr-igual')

    assert prueba_1 == prueba_2


def test_dos_actos_clinicos_con_distinto_id_no_son_iguales():
    prueba_1 = crear_prueba(id='pr-1')
    prueba_2 = crear_prueba(id='pr-2')

    assert prueba_1 != prueba_2


def test_acto_clinico_no_se_compara_con_otro_tipo():
    prueba = crear_prueba()

    assert prueba.__eq__('no es acto clínico') is NotImplemented


def test_hash_depende_del_id():
    prueba_1 = crear_prueba(id='pr-hash')
    prueba_2 = crear_prueba(id='pr-hash')

    assert hash(prueba_1) == hash(prueba_2)


def test_repr_contiene_nombre_de_clase_id_y_fecha():
    fecha = date(2025, 1, 10)
    prueba = crear_prueba(id='pr-repr', fecha=fecha)

    representacion = repr(prueba)

    assert 'EntityPrueba' in representacion
    assert 'pr-repr' in representacion
    assert str(fecha) in representacion