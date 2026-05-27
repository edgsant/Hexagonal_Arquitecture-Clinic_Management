from datetime import date
import pytest

from domain.entities.EntityInformeInicial import EntityInformeInicial
from domain.entities.EntityUrologo import EntityUrologo


def crear_autor(
    id='uro-6',
    nombre='Federico',
    apellidos='Pérez',
    dni='55555555A',
    fecha_nacimiento=date(1974, 2, 14),
    direccion='Calle Informes 8',
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


def crear_informe(
    id='inf-3',
    fecha=date(2025, 4, 10),
    antecedentes='Sin alergias.',
    sintomas='Molestia leve.',
    antecedentes_familiares='No aporta.',
    exploracion_fisica='Exploración normal.',
    autor=None
):
    if autor is None:
        autor = crear_autor()

    return EntityInformeInicial(
        id=id,
        fecha=fecha,
        antecedentes=antecedentes,
        sintomas=sintomas,
        antecedentes_familiares=antecedentes_familiares,
        exploracion_fisica=exploracion_fisica,
        autor=autor
    )


def test_crear_informe_inicial_valido():
    autor = crear_autor()
    fecha = date(2025, 4, 10)

    informe = crear_informe(
        id='inf-3',
        fecha=fecha,
        autor=autor
    )

    assert informe.id == 'inf-3'
    assert informe.fecha == fecha
    assert informe.antecedentes == 'Sin alergias.'
    assert informe.sintomas == 'Molestia leve.'
    assert informe.antecedentes_familiares == 'No aporta.'
    assert informe.exploracion_fisica == 'Exploración normal.'
    assert informe.autor is autor


def test_crear_informe_con_id_vacio_lanza_error():
    with pytest.raises(ValueError):
        crear_informe(id='')


def test_crear_informe_con_fecha_vacia_lanza_error():
    with pytest.raises(ValueError):
        crear_informe(fecha=None)


def test_crear_informe_con_antecedentes_vacios_lanza_error():
    with pytest.raises(ValueError):
        crear_informe(antecedentes='')


def test_crear_informe_con_antecedentes_solo_espacios_lanza_error():
    with pytest.raises(ValueError):
        crear_informe(antecedentes='   ')


def test_crear_informe_con_sintomas_vacios_lanza_error():
    with pytest.raises(ValueError):
        crear_informe(sintomas='')


def test_crear_informe_con_sintomas_solo_espacios_lanza_error():
    with pytest.raises(ValueError):
        crear_informe(sintomas='   ')


def test_crear_informe_con_antecedentes_familiares_vacios_lanza_error():
    with pytest.raises(ValueError):
        crear_informe(antecedentes_familiares='')


def test_crear_informe_con_antecedentes_familiares_solo_espacios_lanza_error():
    with pytest.raises(ValueError):
        crear_informe(antecedentes_familiares='   ')


def test_crear_informe_con_exploracion_fisica_vacia_lanza_error():
    with pytest.raises(ValueError):
        crear_informe(exploracion_fisica='')


def test_crear_informe_con_exploracion_fisica_solo_espacios_lanza_error():
    with pytest.raises(ValueError):
        crear_informe(exploracion_fisica='   ')


def test_crear_informe_con_autor_invalido_lanza_error():
    with pytest.raises(ValueError):
        crear_informe(autor='no es un especialista')


def test_crear_informe_elimina_espacios_laterales_en_campos_clinicos():
    informe = crear_informe(
        antecedentes='  Sin alergias.  ',
        sintomas='  Molestia leve.  ',
        antecedentes_familiares='  No aporta.  ',
        exploracion_fisica='  Exploración normal.  '
    )

    assert informe.antecedentes == 'Sin alergias.'
    assert informe.sintomas == 'Molestia leve.'
    assert informe.antecedentes_familiares == 'No aporta.'
    assert informe.exploracion_fisica == 'Exploración normal.'


def test_dos_informes_con_mismo_id_son_iguales():
    informe_1 = crear_informe(
        id='inf-igual',
        antecedentes='Antecedentes 1.'
    )

    informe_2 = crear_informe(
        id='inf-igual',
        antecedentes='Antecedentes 2.',
        sintomas='Síntomas diferentes.',
        antecedentes_familiares='Familiares diferentes.',
        exploracion_fisica='Exploración diferente.'
    )

    assert informe_1 == informe_2


def test_dos_informes_con_distinto_id_no_son_iguales():
    informe_1 = crear_informe(id='inf-1')
    informe_2 = crear_informe(id='inf-2')

    assert informe_1 != informe_2


def test_informe_no_se_compara_con_otro_tipo():
    informe = crear_informe()

    assert informe.__eq__('no es informe') is NotImplemented


def test_hash_depende_del_id():
    informe_1 = crear_informe(id='inf-hash')
    informe_2 = crear_informe(id='inf-hash')

    assert hash(informe_1) == hash(informe_2)


def test_str_contiene_fecha_y_autor():
    fecha = date(2025, 4, 10)
    autor = crear_autor(nombre='Federico', apellidos='Pérez')

    informe = crear_informe(
        fecha=fecha,
        autor=autor
    )

    representacion = str(informe)

    assert 'Informe Inicial' in representacion
    assert str(fecha) in representacion
    assert 'Autor: Federico Pérez' in representacion


def test_repr_contiene_nombre_de_clase_id_y_fecha():
    fecha = date(2025, 4, 10)

    informe = crear_informe(
        id='inf-repr',
        fecha=fecha
    )

    representacion = repr(informe)

    assert 'EntityInformeInicial' in representacion
    assert 'inf-repr' in representacion
    assert str(fecha) in representacion