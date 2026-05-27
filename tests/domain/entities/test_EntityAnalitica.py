from datetime import date
import pytest

from domain.entities.EntityAnalitica import EntityAnalitica
from domain.entities.EntityAnalistaClinico import EntityAnalistaClinico


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


def crear_analitica(
    id='analitica-1',
    fecha=date(2025, 2, 10),
    especialistas=None,
    pendiente=True
):
    if especialistas is None:
        especialistas = [crear_analista()]

    return EntityAnalitica(
        id=id,
        fecha=fecha,
        especialistas=especialistas,
        pendiente=pendiente
    )


def registrar_resultados_validos(analitica, analista=None):
    if analista is None:
        analista = crear_analista(
            id='ana-resultado',
            dni='12345678A',
            nombre='Patricia',
            apellidos='López',
            direccion='Calle Laboratorio 10',
            telefono='611223344'
        )

    analitica.registrar_resultados(
        psa='4.2 ng/mL',
        leucocitos='7000/uL',
        hemoglobina='14.1 g/dL',
        hematocrito='42%',
        plaquetas='250000/uL',
        creatinina='0.9 mg/dL',
        glucosa='95 mg/dL',
        colesterol='180 mg/dL',
        observaciones='Resultados dentro de los valores esperados.',
        analista=analista
    )

    return analista


def test_crear_analitica_valida_pendiente():
    analista = crear_analista()
    fecha = date(2025, 2, 10)

    analitica = crear_analitica(
        id='analitica-1',
        fecha=fecha,
        especialistas=[analista]
    )

    assert analitica.id == 'analitica-1'
    assert analitica.fecha == fecha
    assert analitica.especialistas == [analista]
    assert analitica.pendiente is True


def test_crear_analitica_inicializa_resultados_a_none():
    analitica = crear_analitica()

    assert analitica.psa is None
    assert analitica.leucocitos is None
    assert analitica.hemoglobina is None
    assert analitica.hematocrito is None
    assert analitica.plaquetas is None
    assert analitica.creatinina is None
    assert analitica.glucosa is None
    assert analitica.colesterol is None
    assert analitica.observaciones is None


def test_crear_analitica_con_id_vacio_lanza_error():
    with pytest.raises(ValueError):
        crear_analitica(id='')


def test_crear_analitica_con_fecha_vacia_lanza_error():
    with pytest.raises(ValueError):
        crear_analitica(fecha=None)


def test_crear_analitica_sin_especialistas_lanza_error():
    with pytest.raises(ValueError):
        crear_analitica(especialistas=[])


def test_crear_analitica_con_especialista_invalido_lanza_error():
    with pytest.raises(ValueError):
        crear_analitica(especialistas=['no es especialista'])


def test_registrar_resultados_guarda_todos_los_valores():
    analitica = crear_analitica()

    registrar_resultados_validos(analitica)

    assert analitica.psa == '4.2 ng/mL'
    assert analitica.leucocitos == '7000/uL'
    assert analitica.hemoglobina == '14.1 g/dL'
    assert analitica.hematocrito == '42%'
    assert analitica.plaquetas == '250000/uL'
    assert analitica.creatinina == '0.9 mg/dL'
    assert analitica.glucosa == '95 mg/dL'
    assert analitica.colesterol == '180 mg/dL'
    assert analitica.observaciones == 'Resultados dentro de los valores esperados.'


def test_registrar_resultados_marca_analitica_como_no_pendiente():
    analitica = crear_analitica()

    registrar_resultados_validos(analitica)

    assert analitica.pendiente is False


def test_registrar_resultados_anade_analista_si_no_estaba_asignado():
    analista_inicial = crear_analista(id='ana-inicial', dni='11111111A')
    analista_resultado = crear_analista(
        id='ana-resultado',
        dni='22222222B',
        nombre='Marta',
        apellidos='Santos',
        direccion='Calle Laboratorio 20',
        telefono='622334455'
    )

    analitica = crear_analitica(especialistas=[analista_inicial])

    registrar_resultados_validos(analitica, analista=analista_resultado)

    assert analista_resultado in analitica.especialistas
    assert len(analitica.especialistas) == 2


def test_registrar_resultados_no_duplica_analista_si_ya_estaba_asignado():
    analista = crear_analista()
    analitica = crear_analitica(especialistas=[analista])

    registrar_resultados_validos(analitica, analista=analista)

    assert analitica.especialistas == [analista]
    assert len(analitica.especialistas) == 1


def test_no_permite_registrar_resultados_dos_veces():
    analitica = crear_analitica()

    registrar_resultados_validos(analitica)

    with pytest.raises(ValueError):
        analitica.registrar_resultados(
            psa='9.9 ng/mL',
            leucocitos='9999/uL',
            hemoglobina='10 g/dL',
            hematocrito='30%',
            plaquetas='100000/uL',
            creatinina='2.0 mg/dL',
            glucosa='200 mg/dL',
            colesterol='300 mg/dL',
            observaciones='Segundo intento incorrecto.',
            analista=crear_analista(id='ana-2', dni='33333333C')
        )


def test_segundo_registro_fallido_no_sobrescribe_resultados_previos():
    analitica = crear_analitica()

    registrar_resultados_validos(analitica)

    with pytest.raises(ValueError):
        analitica.registrar_resultados(
            psa='9.9 ng/mL',
            leucocitos='9999/uL',
            hemoglobina='10 g/dL',
            hematocrito='30%',
            plaquetas='100000/uL',
            creatinina='2.0 mg/dL',
            glucosa='200 mg/dL',
            colesterol='300 mg/dL',
            observaciones='Segundo intento incorrecto.',
            analista=crear_analista(id='ana-2', dni='33333333C')
        )

    assert analitica.psa == '4.2 ng/mL'
    assert analitica.leucocitos == '7000/uL'
    assert analitica.hemoglobina == '14.1 g/dL'
    assert analitica.hematocrito == '42%'
    assert analitica.plaquetas == '250000/uL'
    assert analitica.creatinina == '0.9 mg/dL'
    assert analitica.glucosa == '95 mg/dL'
    assert analitica.colesterol == '180 mg/dL'
    assert analitica.observaciones == 'Resultados dentro de los valores esperados.'


def test_registrar_resultados_con_analista_invalido_lanza_error():
    analitica = crear_analitica()

    with pytest.raises(ValueError):
        analitica.registrar_resultados(
            psa='4.2 ng/mL',
            leucocitos='7000/uL',
            hemoglobina='14.1 g/dL',
            hematocrito='42%',
            plaquetas='250000/uL',
            creatinina='0.9 mg/dL',
            glucosa='95 mg/dL',
            colesterol='180 mg/dL',
            observaciones='Resultados válidos.',
            analista='no es analista'
        )


def test_registro_con_analista_invalido_no_modifica_resultados_ni_estado():
    analitica = crear_analitica()

    with pytest.raises(ValueError):
        analitica.registrar_resultados(
            psa='4.2 ng/mL',
            leucocitos='7000/uL',
            hemoglobina='14.1 g/dL',
            hematocrito='42%',
            plaquetas='250000/uL',
            creatinina='0.9 mg/dL',
            glucosa='95 mg/dL',
            colesterol='180 mg/dL',
            observaciones='Resultados válidos.',
            analista='no es analista'
        )

    assert analitica.pendiente is True
    assert analitica.psa is None
    assert analitica.leucocitos is None
    assert analitica.hemoglobina is None
    assert analitica.hematocrito is None
    assert analitica.plaquetas is None
    assert analitica.creatinina is None
    assert analitica.glucosa is None
    assert analitica.colesterol is None
    assert analitica.observaciones is None


def test_dos_analiticas_con_mismo_id_son_iguales():
    analitica_1 = crear_analitica(id='analitica-igual')
    analitica_2 = crear_analitica(id='analitica-igual')

    assert analitica_1 == analitica_2


def test_dos_analiticas_con_distinto_id_no_son_iguales():
    analitica_1 = crear_analitica(id='analitica-1')
    analitica_2 = crear_analitica(id='analitica-2')

    assert analitica_1 != analitica_2


def test_hash_depende_del_id():
    analitica_1 = crear_analitica(id='analitica-hash')
    analitica_2 = crear_analitica(id='analitica-hash')

    assert hash(analitica_1) == hash(analitica_2)


def test_repr_contiene_nombre_de_clase_id_y_fecha():
    fecha = date(2025, 2, 10)
    analitica = crear_analitica(id='analitica-repr', fecha=fecha)

    representacion = repr(analitica)

    assert 'EntityAnalitica' in representacion
    assert 'analitica-repr' in representacion
    assert str(fecha) in representacion