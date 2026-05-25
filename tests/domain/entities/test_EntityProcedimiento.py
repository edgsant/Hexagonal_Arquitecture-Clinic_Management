from datetime import date
import pytest

from domain.entities.EntityPaciente import EntityPaciente
from domain.entities.EntityProcedimiento import EntityProcedimiento, EstadoProcedimiento
from domain.entities.EntityConsulta import EntityConsulta
from domain.entities.EntityPrueba import EntityPrueba
from domain.entities.EntityInformeInicial import EntityInformeInicial
from domain.entities.EntityAnalistaClinico import EntityAnalistaClinico
from domain.entities.EntityUrologo import EntityUrologo


def test_crear_procedimiento_valido():
    paciente = EntityPaciente(
        id='pac-1',
        dni='12345678A',
        fecha_nacimiento=date(1990, 1, 1),
        nombre='Laura',
        apellidos='Pérez',
        direccion='Calle Nueva 10',
        telefono='611223344'
    )
    procedimiento = EntityProcedimiento('proc-1', paciente)

    assert procedimiento.id == 'proc-1'
    assert procedimiento.paciente is paciente
    assert procedimiento.estado == EstadoProcedimiento.ACTIVO
    assert procedimiento.actos_clinicos == []


def test_crear_procedimiento_sin_paciente_levanta_error():
    with pytest.raises(ValueError):
        EntityProcedimiento('proc-2', paciente=None)


def test_registrar_acto_clinico_y_no_duplicados():
    paciente = EntityPaciente(
        id='pac-2',
        dni='87654321B',
        fecha_nacimiento=date(1992, 2, 2),
        nombre='Carlos',
        apellidos='Ramírez',
        direccion='Calle Olivo 9',
        telefono='611223344'
    )
    procedimiento = EntityProcedimiento('proc-3', paciente)
    especialista = EntityUrologo(
        id='uro-2',
        nombre='Ana',
        apellidos='Sánchez',
        dni='11111111A',
        fecha_nacimiento=date(1975, 6, 6),
        direccion='Calle Médico 2',
        telefono='611223344'
    )
    consulta = EntityConsulta('cons-1', date.today(), [especialista])

    procedimiento.registrar_acto_clinico(consulta)
    procedimiento.registrar_acto_clinico(consulta)

    assert procedimiento.actos_clinicos == [consulta]


def test_obtener_consulta_devuelve_consulta_registrada():
    paciente = EntityPaciente(
        id='pac-4',
        dni='22222222B',
        fecha_nacimiento=date(1995, 5, 5),
        nombre='Elena',
        apellidos='Morales',
        direccion='Calle Ejemplo 4',
        telefono='611223344'
    )
    procedimiento = EntityProcedimiento('proc-4', paciente)
    especialista = EntityUrologo(
        id='uro-3',
        nombre='Ignacio',
        apellidos='López',
        dni='33333333C',
        fecha_nacimiento=date(1977, 7, 7),
        direccion='Calle Real 3',
        telefono='611223344'
    )
    consulta = EntityConsulta('cons-2', date.today(), [especialista])
    prueba = EntityPrueba('pr-1', date.today(), [especialista])

    procedimiento.registrar_acto_clinico(consulta)
    procedimiento.registrar_acto_clinico(prueba)

    assert procedimiento.obtener_consulta() is consulta
    assert procedimiento.obtener_pruebas_pendientes() == [prueba]


def test_finalizar_procedimiento_sin_pruebas_pendientes():
    paciente = EntityPaciente(
        id='pac-5',
        dni='44444444D',
        fecha_nacimiento=date(2000, 8, 8),
        nombre='Sofía',
        apellidos='Castillo',
        direccion='Avenida del Sol 1',
        telefono='611223344'
    )
    procedimiento = EntityProcedimiento('proc-5', paciente)

    procedimiento.finalizar()

    assert procedimiento.estado == EstadoProcedimiento.FINALIZADO


def test_finalizar_procedimiento_con_pruebas_pendientes_levanta_error():
    paciente = EntityPaciente(
        id='pac-6',
        dni='55555555E',
        fecha_nacimiento=date(1999, 9, 9),
        nombre='Martín',
        apellidos='Vega',
        direccion='Calle de la Salud 8',
        telefono='611223344'
    )
    procedimiento = EntityProcedimiento('proc-6', paciente)
    analista = EntityAnalistaClinico(
        id='ana-2',
        nombre='Lucía',
        apellidos='Díaz',
        dni='66666666F',
        fecha_nacimiento=date(1986, 4, 4),
        direccion='Calle Salud 2',
        telefono='611223344'
    )
    prueba = EntityPrueba('pr-2', date.today(), [analista])

    procedimiento.registrar_acto_clinico(prueba)

    with pytest.raises(ValueError):
        procedimiento.finalizar()


def test_vincular_informe_valido():
    paciente = EntityPaciente(
        id='pac-7',
        dni='77777777G',
        fecha_nacimiento=date(1991, 11, 11),
        nombre='Ana',
        apellidos='Fernández',
        direccion='Calle Luna 6',
        telefono='611223344'
    )
    procedimiento = EntityProcedimiento('proc-7', paciente)
    autor = EntityUrologo(
        id='uro-4',
        nombre='Miguel',
        apellidos='Ruiz',
        dni='88888888H',
        fecha_nacimiento=date(1969, 1, 1),
        direccion='Calle Luz 10',
        telefono='611223344'
    )
    informe = EntityInformeInicial(
        id='inf-1',
        fecha=date.today(),
        antecedentes='Sin alergias relevantes.',
        sintomas='Molestia lumbar.',
        antecedentes_familiares='Negativos.',
        exploracion_fisica='Abdomen blando.',
        autor=autor
    )

    procedimiento.vincular_informe(informe)

    assert procedimiento.informe_inicial is informe


def test_vincular_informe_a_procedimiento_finalizado_levanta_error():
    paciente = EntityPaciente(
        id='pac-8',
        dni='99999999I',
        fecha_nacimiento=date(1992, 12, 12),
        nombre='Laura',
        apellidos='Pérez',
        direccion='Calle Salud 9',
        telefono='611223344'
    )
    procedimiento = EntityProcedimiento('proc-8', paciente)
    procedimiento.finalizar()
    autor = EntityUrologo(
        id='uro-5',
        nombre='Álvaro',
        apellidos='Gómez',
        dni='10101010J',
        fecha_nacimiento=date(1972, 2, 2),
        direccion='Calle Norte 4',
        telefono='611223344'
    )
    informe = EntityInformeInicial(
        id='inf-2',
        fecha=date.today(),
        antecedentes='No relevantes.',
        sintomas='Molestia general.',
        antecedentes_familiares='No aporta.',
        exploracion_fisica='Normal.',
        autor=autor
    )

    with pytest.raises(ValueError):
        procedimiento.vincular_informe(informe)
