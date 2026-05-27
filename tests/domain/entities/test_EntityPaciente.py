from datetime import date, timedelta
import pytest

from domain.entities.EntityPaciente import EntityPaciente


def crear_paciente(
    id='pac-1',
    dni='12345678A',
    fecha_nacimiento=date(1985, 10, 12),
    nombre='Alejandro',
    apellidos='Sanz',
    direccion='Calle de la Salud 4',
    telefono='+34611223344'
):
    return EntityPaciente(
        id=id,
        dni=dni,
        fecha_nacimiento=fecha_nacimiento,
        nombre=nombre,
        apellidos=apellidos,
        direccion=direccion,
        telefono=telefono
    )


def test_crear_paciente_valido():
    paciente = crear_paciente()

    assert paciente.id == 'pac-1'
    assert paciente.dni == '12345678A'
    assert paciente.fecha_nacimiento == date(1985, 10, 12)
    assert paciente.nombre == 'Alejandro'
    assert paciente.apellidos == 'Sanz'
    assert paciente.direccion == 'Calle de la Salud 4'
    assert paciente.telefono == '+34611223344'


def test_crear_paciente_con_id_vacio_lanza_error():
    with pytest.raises(ValueError):
        crear_paciente(id='')


def test_crear_paciente_con_dni_vacio_lanza_error():
    with pytest.raises(ValueError):
        crear_paciente(dni='')


def test_crear_paciente_con_dni_invalido_lanza_error():
    with pytest.raises(ValueError):
        crear_paciente(dni='1234A')


def test_crear_paciente_con_fecha_nacimiento_vacia_lanza_error():
    with pytest.raises(ValueError):
        crear_paciente(fecha_nacimiento=None)


def test_crear_paciente_con_fecha_nacimiento_futura_lanza_error():
    with pytest.raises(ValueError):
        crear_paciente(fecha_nacimiento=date.today() + timedelta(days=1))


def test_crear_paciente_con_nombre_vacio_lanza_error():
    with pytest.raises(ValueError):
        crear_paciente(nombre='')


def test_crear_paciente_con_nombre_demasiado_corto_lanza_error():
    with pytest.raises(ValueError):
        crear_paciente(nombre=' A ')


def test_crear_paciente_con_apellidos_vacios_lanza_error():
    with pytest.raises(ValueError):
        crear_paciente(apellidos='')


def test_crear_paciente_con_apellidos_demasiado_cortos_lanza_error():
    with pytest.raises(ValueError):
        crear_paciente(apellidos=' S ')


def test_crear_paciente_con_direccion_vacia_lanza_error():
    with pytest.raises(ValueError):
        crear_paciente(direccion='')


def test_crear_paciente_con_telefono_invalido_lanza_error():
    with pytest.raises(ValueError):
        crear_paciente(telefono='12345')


def test_setters_permiten_modificar_campos_validos():
    paciente = crear_paciente()

    paciente.nombre = 'Carlos'
    paciente.apellidos = 'Pérez Gómez'
    paciente.direccion = 'Avenida Principal 10'
    paciente.telefono = '611223344'

    assert paciente.nombre == 'Carlos'
    assert paciente.apellidos == 'Pérez Gómez'
    assert paciente.direccion == 'Avenida Principal 10'
    assert paciente.telefono == '611223344'


def test_setter_nombre_elimina_espacios_laterales():
    paciente = crear_paciente()

    paciente.nombre = '  Carlos  '

    assert paciente.nombre == 'Carlos'


def test_setter_apellidos_elimina_espacios_laterales():
    paciente = crear_paciente()

    paciente.apellidos = '  Pérez Gómez  '

    assert paciente.apellidos == 'Pérez Gómez'


def test_setter_direccion_elimina_espacios_laterales():
    paciente = crear_paciente()

    paciente.direccion = '  Avenida Principal 10  '

    assert paciente.direccion == 'Avenida Principal 10'


def test_setter_nombre_invalido_no_modifica_valor_anterior():
    paciente = crear_paciente()

    with pytest.raises(ValueError):
        paciente.nombre = ''

    assert paciente.nombre == 'Alejandro'


def test_setter_apellidos_invalidos_no_modifica_valor_anterior():
    paciente = crear_paciente()

    with pytest.raises(ValueError):
        paciente.apellidos = ''

    assert paciente.apellidos == 'Sanz'


def test_setter_direccion_invalida_no_modifica_valor_anterior():
    paciente = crear_paciente()

    with pytest.raises(ValueError):
        paciente.direccion = ''

    assert paciente.direccion == 'Calle de la Salud 4'


def test_setter_telefono_invalido_no_modifica_valor_anterior():
    paciente = crear_paciente()

    with pytest.raises(ValueError):
        paciente.telefono = '12345'

    assert paciente.telefono == '+34611223344'


def test_telefono_valido_sin_prefijo():
    paciente = crear_paciente(telefono='611223344')

    assert paciente.telefono == '611223344'


def test_telefono_valido_con_prefijo_mas_34():
    paciente = crear_paciente(telefono='+34611223344')

    assert paciente.telefono == '+34611223344'


def test_telefono_valido_con_prefijo_0034():
    paciente = crear_paciente(telefono='0034611223344')

    assert paciente.telefono == '0034611223344'


def test_validar_datos_devuelve_true_para_paciente_valido():
    paciente = crear_paciente()

    assert paciente.validar_datos() is True


def test_dos_pacientes_con_mismo_id_son_iguales():
    paciente_1 = crear_paciente(
        id='pac-igual',
        dni='12345678C'
    )

    paciente_2 = crear_paciente(
        id='pac-igual',
        dni='87654321C',
        fecha_nacimiento=date(1971, 8, 8),
        nombre='José',
        apellidos='Martínez',
        direccion='Calle Mayor 1',
        telefono='911223344'
    )

    assert paciente_1 == paciente_2


def test_dos_pacientes_con_distinto_id_no_son_iguales():
    paciente_1 = crear_paciente(
        id='pac-1',
        dni='12345678C'
    )

    paciente_2 = crear_paciente(
        id='pac-2',
        dni='87654321C'
    )

    assert paciente_1 != paciente_2


def test_paciente_no_se_compara_con_otro_tipo():
    paciente = crear_paciente()

    assert paciente.__eq__('no es paciente') is NotImplemented


def test_hash_depende_del_id():
    paciente_1 = crear_paciente(
        id='pac-hash',
        dni='12345678C'
    )

    paciente_2 = crear_paciente(
        id='pac-hash',
        dni='87654321C'
    )

    assert hash(paciente_1) == hash(paciente_2)


def test_str_contiene_nombre_apellidos_y_dni():
    paciente = crear_paciente()

    representacion = str(paciente)

    assert 'Alejandro Sanz' in representacion
    assert '12345678A' in representacion


def test_repr_contiene_nombre_de_clase_id_y_dni():
    paciente = crear_paciente()

    representacion = repr(paciente)

    assert 'EntityPaciente' in representacion
    assert 'pac-1' in representacion
    assert '12345678A' in representacion