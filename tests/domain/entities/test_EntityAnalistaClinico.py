from datetime import date
import pytest

from domain.entities.EntityAnalistaClinico import EntityAnalistaClinico
from domain.entities.EntityEspecialista import EntityEspecialista


def crear_analista(
    id='ana-1',
    nombre='Elena',
    apellidos='Ruiz',
    dni='87654321Z',
    fecha_nacimiento=date(1988, 12, 5),
    direccion='Calle Analítica 5',
    telefono='+34611223344'
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


def test_crear_analista_clinico_valido():
    analista = crear_analista()

    assert analista.id == 'ana-1'
    assert analista.nombre == 'Elena'
    assert analista.apellidos == 'Ruiz'
    assert analista.dni == '87654321Z'
    assert analista.fecha_nacimiento == date(1988, 12, 5)
    assert analista.direccion == 'Calle Analítica 5'
    assert analista.telefono == '+34611223344'


def test_analista_clinico_es_especialista():
    analista = crear_analista()

    assert isinstance(analista, EntityAnalistaClinico)
    assert isinstance(analista, EntityEspecialista)


def test_analista_clinico_hereda_validacion_de_dni():
    with pytest.raises(ValueError):
        crear_analista(dni='DNI_INVALIDO')


def test_analista_clinico_hereda_validacion_de_fecha_nacimiento():
    with pytest.raises(ValueError):
        crear_analista(fecha_nacimiento=None)


def test_analista_clinico_hereda_validacion_de_nombre():
    with pytest.raises(ValueError):
        crear_analista(nombre='')


def test_analista_clinico_hereda_validacion_de_apellidos():
    with pytest.raises(ValueError):
        crear_analista(apellidos='')


def test_analista_clinico_hereda_validacion_de_direccion():
    with pytest.raises(ValueError):
        crear_analista(direccion='abc')


def test_analista_clinico_hereda_validacion_de_telefono():
    with pytest.raises(ValueError):
        crear_analista(telefono='123')


def test_analista_clinico_permite_modificar_datos_mutables_validos():
    analista = crear_analista()

    analista.nombre = 'Laura'
    analista.apellidos = 'García Pérez'
    analista.direccion = 'Avenida Laboratorio 10'
    analista.telefono = '699887766'

    assert analista.nombre == 'Laura'
    assert analista.apellidos == 'García Pérez'
    assert analista.direccion == 'Avenida Laboratorio 10'
    assert analista.telefono == '699887766'


def test_dos_analistas_con_mismo_id_son_iguales():
    analista_1 = crear_analista(
        id='ana-igual',
        dni='11111111A'
    )

    analista_2 = crear_analista(
        id='ana-igual',
        nombre='Marta',
        apellidos='Santos',
        dni='22222222B',
        fecha_nacimiento=date(1990, 1, 1),
        direccion='Calle Laboratorio 22',
        telefono='611223344'
    )

    assert analista_1 == analista_2


def test_dos_analistas_con_distinto_id_no_son_iguales():
    analista_1 = crear_analista(
        id='ana-1',
        dni='11111111A'
    )

    analista_2 = crear_analista(
        id='ana-2',
        dni='22222222B'
    )

    assert analista_1 != analista_2


def test_analista_no_se_compara_con_otro_tipo():
    analista = crear_analista()

    assert analista.__eq__('no es especialista') is NotImplemented


def test_hash_depende_del_id():
    analista_1 = crear_analista(
        id='ana-hash',
        dni='11111111A'
    )

    analista_2 = crear_analista(
        id='ana-hash',
        dni='22222222B'
    )

    assert hash(analista_1) == hash(analista_2)


def test_str_contiene_nombre_apellidos_y_dni():
    analista = crear_analista()

    representacion = str(analista)

    assert 'Elena Ruiz' in representacion
    assert '87654321Z' in representacion


def test_repr_contiene_nombre_de_clase_base_id_y_nombre():
    analista = crear_analista()

    representacion = repr(analista)

    assert 'EntityEspecialista' in representacion
    assert 'ana-1' in representacion
    assert 'Elena' in representacion