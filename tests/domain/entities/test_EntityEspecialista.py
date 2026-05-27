from datetime import date
import pytest

from domain.entities.EntityEspecialista import EntityEspecialista


def crear_especialista(
    id='esp-1',
    nombre='Laura',
    apellidos='García',
    dni='12345678A',
    fecha_nacimiento=date(1980, 5, 15),
    direccion='Calle del Río 10',
    telefono='+34611223344'
):
    return EntityEspecialista(
        id=id,
        nombre=nombre,
        apellidos=apellidos,
        dni=dni,
        fecha_nacimiento=fecha_nacimiento,
        direccion=direccion,
        telefono=telefono
    )


def test_crear_especialista_valido():
    especialista = crear_especialista()

    assert especialista.id == 'esp-1'
    assert especialista.nombre == 'Laura'
    assert especialista.apellidos == 'García'
    assert especialista.dni == '12345678A'
    assert especialista.fecha_nacimiento == date(1980, 5, 15)
    assert especialista.direccion == 'Calle del Río 10'
    assert especialista.telefono == '+34611223344'


def test_crear_especialista_con_id_vacio_lanza_error():
    with pytest.raises(ValueError):
        crear_especialista(id='')


def test_crear_especialista_con_dni_invalido_lanza_error():
    with pytest.raises(ValueError):
        crear_especialista(dni='1234X')


def test_crear_especialista_con_fecha_nacimiento_vacia_lanza_error():
    with pytest.raises(ValueError):
        crear_especialista(fecha_nacimiento=None)


def test_crear_especialista_con_nombre_vacio_lanza_error():
    with pytest.raises(ValueError):
        crear_especialista(nombre='')


def test_crear_especialista_con_nombre_demasiado_corto_lanza_error():
    with pytest.raises(ValueError):
        crear_especialista(nombre=' A ')


def test_crear_especialista_con_apellidos_vacios_lanza_error():
    with pytest.raises(ValueError):
        crear_especialista(apellidos='')


def test_crear_especialista_con_apellidos_demasiado_cortos_lanza_error():
    with pytest.raises(ValueError):
        crear_especialista(apellidos=' B ')


def test_crear_especialista_con_direccion_vacia_lanza_error():
    with pytest.raises(ValueError):
        crear_especialista(direccion='')


def test_crear_especialista_con_direccion_demasiado_corta_lanza_error():
    with pytest.raises(ValueError):
        crear_especialista(direccion='abc')


def test_crear_especialista_con_telefono_invalido_lanza_error():
    with pytest.raises(ValueError):
        crear_especialista(telefono='123')


def test_setters_permiten_modificar_campos_validos():
    especialista = crear_especialista()

    especialista.nombre = 'Carlos Alberto'
    especialista.apellidos = 'Santos Pérez'
    especialista.direccion = 'Avenida Principal 3'
    especialista.telefono = '611223344'

    assert especialista.nombre == 'Carlos Alberto'
    assert especialista.apellidos == 'Santos Pérez'
    assert especialista.direccion == 'Avenida Principal 3'
    assert especialista.telefono == '611223344'


def test_setter_nombre_elimina_espacios_laterales():
    especialista = crear_especialista()

    especialista.nombre = '  Carlos  '

    assert especialista.nombre == 'Carlos'


def test_setter_apellidos_elimina_espacios_laterales():
    especialista = crear_especialista()

    especialista.apellidos = '  Santos Pérez  '

    assert especialista.apellidos == 'Santos Pérez'


def test_setter_direccion_elimina_espacios_laterales():
    especialista = crear_especialista()

    especialista.direccion = '  Avenida Principal 3  '

    assert especialista.direccion == 'Avenida Principal 3'


def test_setter_nombre_invalido_no_modifica_valor_anterior():
    especialista = crear_especialista()

    with pytest.raises(ValueError):
        especialista.nombre = ''

    assert especialista.nombre == 'Laura'


def test_setter_apellidos_invalidos_no_modifica_valor_anterior():
    especialista = crear_especialista()

    with pytest.raises(ValueError):
        especialista.apellidos = ''

    assert especialista.apellidos == 'García'


def test_setter_direccion_invalida_no_modifica_valor_anterior():
    especialista = crear_especialista()

    with pytest.raises(ValueError):
        especialista.direccion = 'abc'

    assert especialista.direccion == 'Calle del Río 10'


def test_setter_telefono_invalido_no_modifica_valor_anterior():
    especialista = crear_especialista()

    with pytest.raises(ValueError):
        especialista.telefono = '123'

    assert especialista.telefono == '+34611223344'


def test_telefono_valido_sin_prefijo():
    especialista = crear_especialista(telefono='611223344')

    assert especialista.telefono == '611223344'


def test_telefono_valido_con_prefijo_mas_34():
    especialista = crear_especialista(telefono='+34611223344')

    assert especialista.telefono == '+34611223344'


def test_telefono_valido_con_prefijo_0034():
    especialista = crear_especialista(telefono='0034611223344')

    assert especialista.telefono == '0034611223344'


def test_dos_especialistas_con_mismo_id_son_iguales():
    primero = crear_especialista(
        id='esp-igual',
        dni='11111111A'
    )

    segundo = crear_especialista(
        id='esp-igual',
        nombre='Marta',
        apellidos='Domínguez',
        dni='22222222B',
        fecha_nacimiento=date(1982, 11, 1),
        direccion='Calle Real 7',
        telefono='611223344'
    )

    assert primero == segundo


def test_dos_especialistas_con_distinto_id_no_son_iguales():
    primero = crear_especialista(
        id='esp-1',
        dni='11111111A'
    )

    segundo = crear_especialista(
        id='esp-2',
        dni='22222222B'
    )

    assert primero != segundo


def test_especialista_no_se_compara_con_otro_tipo():
    especialista = crear_especialista()

    assert especialista.__eq__('no es especialista') is NotImplemented


def test_hash_depende_del_id():
    primero = crear_especialista(
        id='esp-hash',
        dni='11111111A'
    )

    segundo = crear_especialista(
        id='esp-hash',
        dni='22222222B'
    )

    assert hash(primero) == hash(segundo)


def test_str_contiene_nombre_apellidos_y_dni():
    especialista = crear_especialista()

    representacion = str(especialista)

    assert 'Laura García' in representacion
    assert '12345678A' in representacion


def test_repr_contiene_nombre_de_clase_id_y_nombre():
    especialista = crear_especialista()

    representacion = repr(especialista)

    assert 'EntityEspecialista' in representacion
    assert 'esp-1' in representacion
    assert 'Laura' in representacion