from datetime import date
import pytest

from domain.entities.EntityUrologo import EntityUrologo
from domain.entities.EntityEspecialista import EntityEspecialista


def crear_urologo(
    id='uro-1',
    nombre='Federico',
    apellidos='Pérez',
    dni='55555555A',
    fecha_nacimiento=date(1974, 2, 14),
    direccion='Calle Urología 8',
    telefono='611223344'
):
    return EntityUrologo(
        id=id,
        nombre=nombre,
        apellidos=apellidos,
        dni=dni,
        fecha_nacimiento=fecha_nacimiento,
        direccion=direccion,
        telefono=telefono
    )


def test_crear_urologo_valido():
    urologo = crear_urologo()

    assert urologo.id == 'uro-1'
    assert urologo.nombre == 'Federico'
    assert urologo.apellidos == 'Pérez'
    assert urologo.dni == '55555555A'
    assert urologo.fecha_nacimiento == date(1974, 2, 14)
    assert urologo.direccion == 'Calle Urología 8'
    assert urologo.telefono == '611223344'


def test_urologo_es_especialista():
    urologo = crear_urologo()

    assert isinstance(urologo, EntityUrologo)
    assert isinstance(urologo, EntityEspecialista)


def test_urologo_hereda_validacion_de_id():
    with pytest.raises(ValueError):
        crear_urologo(id='')


def test_urologo_hereda_validacion_de_dni():
    with pytest.raises(ValueError):
        crear_urologo(dni='DNI_INVALIDO')


def test_urologo_hereda_validacion_de_fecha_nacimiento():
    with pytest.raises(ValueError):
        crear_urologo(fecha_nacimiento=None)


def test_urologo_hereda_validacion_de_nombre():
    with pytest.raises(ValueError):
        crear_urologo(nombre='')


def test_urologo_hereda_validacion_de_nombre_demasiado_corto():
    with pytest.raises(ValueError):
        crear_urologo(nombre=' A ')


def test_urologo_hereda_validacion_de_apellidos():
    with pytest.raises(ValueError):
        crear_urologo(apellidos='')


def test_urologo_hereda_validacion_de_apellidos_demasiado_cortos():
    with pytest.raises(ValueError):
        crear_urologo(apellidos=' P ')


def test_urologo_hereda_validacion_de_direccion():
    with pytest.raises(ValueError):
        crear_urologo(direccion='abc')


def test_urologo_hereda_validacion_de_telefono():
    with pytest.raises(ValueError):
        crear_urologo(telefono='123')


def test_urologo_permite_modificar_datos_mutables_validos():
    urologo = crear_urologo()

    urologo.nombre = 'Laura'
    urologo.apellidos = 'García Pérez'
    urologo.direccion = 'Avenida Clínica 10'
    urologo.telefono = '+34699887766'

    assert urologo.nombre == 'Laura'
    assert urologo.apellidos == 'García Pérez'
    assert urologo.direccion == 'Avenida Clínica 10'
    assert urologo.telefono == '+34699887766'


def test_setter_nombre_invalido_no_modifica_valor_anterior():
    urologo = crear_urologo()

    with pytest.raises(ValueError):
        urologo.nombre = ''

    assert urologo.nombre == 'Federico'


def test_setter_apellidos_invalidos_no_modifica_valor_anterior():
    urologo = crear_urologo()

    with pytest.raises(ValueError):
        urologo.apellidos = ''

    assert urologo.apellidos == 'Pérez'


def test_setter_direccion_invalida_no_modifica_valor_anterior():
    urologo = crear_urologo()

    with pytest.raises(ValueError):
        urologo.direccion = 'abc'

    assert urologo.direccion == 'Calle Urología 8'


def test_setter_telefono_invalido_no_modifica_valor_anterior():
    urologo = crear_urologo()

    with pytest.raises(ValueError):
        urologo.telefono = '123'

    assert urologo.telefono == '611223344'


def test_dos_urologos_con_mismo_id_son_iguales():
    urologo_1 = crear_urologo(
        id='uro-igual',
        dni='11111111A'
    )

    urologo_2 = crear_urologo(
        id='uro-igual',
        nombre='Ana',
        apellidos='Sánchez',
        dni='22222222B',
        fecha_nacimiento=date(1978, 5, 20),
        direccion='Calle Consulta 12',
        telefono='622334455'
    )

    assert urologo_1 == urologo_2


def test_dos_urologos_con_distinto_id_no_son_iguales():
    urologo_1 = crear_urologo(
        id='uro-1',
        dni='11111111A'
    )

    urologo_2 = crear_urologo(
        id='uro-2',
        dni='22222222B'
    )

    assert urologo_1 != urologo_2


def test_urologo_no_se_compara_con_otro_tipo():
    urologo = crear_urologo()

    assert urologo.__eq__('no es especialista') is NotImplemented


def test_hash_depende_del_id():
    urologo_1 = crear_urologo(
        id='uro-hash',
        dni='11111111A'
    )

    urologo_2 = crear_urologo(
        id='uro-hash',
        dni='22222222B'
    )

    assert hash(urologo_1) == hash(urologo_2)


def test_str_contiene_nombre_apellidos_y_dni():
    urologo = crear_urologo()

    representacion = str(urologo)

    assert 'Federico Pérez' in representacion
    assert '55555555A' in representacion


def test_repr_contiene_nombre_de_clase_base_id_y_nombre():
    urologo = crear_urologo()

    representacion = repr(urologo)

    assert 'EntityEspecialista' in representacion
    assert 'uro-1' in representacion
    assert 'Federico' in representacion