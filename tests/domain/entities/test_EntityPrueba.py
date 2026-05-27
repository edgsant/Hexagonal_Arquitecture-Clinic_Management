from datetime import date
import pytest

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
    fecha=date(2025, 6, 10),
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


def test_crear_prueba_valida_pendiente_por_defecto():
    analista = crear_analista()
    fecha = date(2025, 6, 10)

    prueba = crear_prueba(
        id='pr-1',
        fecha=fecha,
        especialistas=[analista]
    )

    assert prueba.id == 'pr-1'
    assert prueba.fecha == fecha
    assert prueba.especialistas == [analista]
    assert prueba.pendiente is True


def test_crear_prueba_valida_no_pendiente():
    prueba = crear_prueba(pendiente=False)

    assert prueba.pendiente is False


def test_crear_prueba_con_id_vacio_lanza_error():
    with pytest.raises(ValueError):
        crear_prueba(id='')


def test_crear_prueba_con_fecha_vacia_lanza_error():
    with pytest.raises(ValueError):
        crear_prueba(fecha=None)


def test_crear_prueba_sin_especialistas_lanza_error():
    with pytest.raises(ValueError):
        crear_prueba(especialistas=[])


def test_crear_prueba_con_especialista_invalido_lanza_error():
    with pytest.raises(ValueError):
        crear_prueba(especialistas=['no es especialista'])


def test_crear_prueba_con_pendiente_invalido_lanza_error():
    with pytest.raises(ValueError):
        crear_prueba(pendiente='si')


def test_marcar_completada_cambia_estado_a_no_pendiente():
    prueba = crear_prueba()
    analista = crear_analista(
        id='ana-2',
        dni='77777777G',
        nombre='Marta',
        apellidos='Santos',
        direccion='Calle Laboratorio 4',
        telefono='622334455'
    )

    prueba.marcar_completada(analista)

    assert prueba.pendiente is False


def test_marcar_completada_anade_especialista_si_no_estaba_asignado():
    analista_inicial = crear_analista(id='ana-inicial', dni='11111111A')
    analista_responsable = crear_analista(
        id='ana-responsable',
        dni='22222222B',
        nombre='Patricia',
        apellidos='Gómez',
        direccion='Calle Laboratorio 20',
        telefono='633445566'
    )

    prueba = crear_prueba(especialistas=[analista_inicial])

    prueba.marcar_completada(analista_responsable)

    assert analista_responsable in prueba.especialistas
    assert len(prueba.especialistas) == 2


def test_marcar_completada_no_duplica_especialista_si_ya_estaba_asignado():
    analista = crear_analista()
    prueba = crear_prueba(especialistas=[analista])

    prueba.marcar_completada(analista)

    assert prueba.especialistas == [analista]
    assert len(prueba.especialistas) == 1


def test_no_permite_marcar_completada_dos_veces():
    prueba = crear_prueba()
    analista = crear_analista()

    prueba.marcar_completada(analista)

    with pytest.raises(ValueError):
        prueba.marcar_completada(analista)


def test_segundo_marcado_como_completada_no_modifica_especialistas():
    analista = crear_analista()
    prueba = crear_prueba(especialistas=[analista])

    prueba.marcar_completada(analista)

    especialista_nuevo = crear_analista(
        id='ana-2',
        dni='77777777G',
        nombre='Marta',
        apellidos='Santos',
        direccion='Calle Laboratorio 4',
        telefono='622334455'
    )

    with pytest.raises(ValueError):
        prueba.marcar_completada(especialista_nuevo)

    assert prueba.especialistas == [analista]
    assert especialista_nuevo not in prueba.especialistas
    assert prueba.pendiente is False


def test_marcar_completada_con_especialista_invalido_lanza_error():
    prueba = crear_prueba()

    with pytest.raises(ValueError):
        prueba.marcar_completada('no es especialista')


def test_marcar_completada_con_especialista_invalido_no_modifica_estado():
    prueba = crear_prueba()

    with pytest.raises(ValueError):
        prueba.marcar_completada('no es especialista')

    assert prueba.pendiente is True


def test_marcar_completada_con_especialista_invalido_no_modifica_especialistas():
    analista = crear_analista()
    prueba = crear_prueba(especialistas=[analista])

    with pytest.raises(ValueError):
        prueba.marcar_completada('no es especialista')

    assert prueba.especialistas == [analista]


def test_dos_pruebas_con_mismo_id_son_iguales():
    prueba_1 = crear_prueba(id='pr-igual')
    prueba_2 = crear_prueba(id='pr-igual')

    assert prueba_1 == prueba_2


def test_dos_pruebas_con_distinto_id_no_son_iguales():
    prueba_1 = crear_prueba(id='pr-1')
    prueba_2 = crear_prueba(id='pr-2')

    assert prueba_1 != prueba_2


def test_prueba_no_se_compara_con_otro_tipo():
    prueba = crear_prueba()

    assert prueba.__eq__('no es prueba') is NotImplemented


def test_hash_depende_del_id():
    prueba_1 = crear_prueba(id='pr-hash')
    prueba_2 = crear_prueba(id='pr-hash')

    assert hash(prueba_1) == hash(prueba_2)


def test_repr_contiene_nombre_de_clase_id_y_fecha():
    fecha = date(2025, 6, 10)
    prueba = crear_prueba(id='pr-repr', fecha=fecha)

    representacion = repr(prueba)

    assert 'EntityPrueba' in representacion
    assert 'pr-repr' in representacion
    assert str(fecha) in representacion