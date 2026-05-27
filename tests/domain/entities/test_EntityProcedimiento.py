from datetime import date
import pytest

from domain.entities.EntityPaciente import EntityPaciente
from domain.entities.EntityProcedimiento import EntityProcedimiento, EstadoProcedimiento
from domain.entities.EntityConsulta import EntityConsulta
from domain.entities.EntityPrueba import EntityPrueba
from domain.entities.EntityInformeInicial import EntityInformeInicial
from domain.entities.EntityAnalistaClinico import EntityAnalistaClinico
from domain.entities.EntityUrologo import EntityUrologo


def crear_paciente(
    id='pac-1',
    dni='12345678A',
    fecha_nacimiento=date(1990, 1, 1),
    nombre='Laura',
    apellidos='Pérez',
    direccion='Calle Nueva 10',
    telefono='611223344'
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


def crear_urologo(
    id='uro-1',
    nombre='Ana',
    apellidos='Sánchez',
    dni='11111111A',
    fecha_nacimiento=date(1975, 6, 6),
    direccion='Calle Médico 2',
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


def crear_procedimiento(
    id='proc-1',
    paciente=None
):
    if paciente is None:
        paciente = crear_paciente()

    return EntityProcedimiento(
        id=id,
        paciente=paciente
    )


def crear_consulta(
    id='cons-1',
    fecha=date(2025, 5, 10),
    especialistas=None
):
    if especialistas is None:
        especialistas = [crear_urologo()]

    return EntityConsulta(
        id=id,
        fecha=fecha,
        especialistas=especialistas
    )


def crear_prueba(
    id='pr-1',
    fecha=date(2025, 5, 11),
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


def crear_informe(
    id='inf-1',
    fecha=date(2025, 5, 12),
    antecedentes='Sin alergias relevantes.',
    sintomas='Molestia lumbar.',
    antecedentes_familiares='Negativos.',
    exploracion_fisica='Abdomen blando.',
    autor=None
):
    if autor is None:
        autor = crear_urologo()

    return EntityInformeInicial(
        id=id,
        fecha=fecha,
        antecedentes=antecedentes,
        sintomas=sintomas,
        antecedentes_familiares=antecedentes_familiares,
        exploracion_fisica=exploracion_fisica,
        autor=autor
    )


def test_crear_procedimiento_valido():
    paciente = crear_paciente()
    procedimiento = crear_procedimiento(
        id='proc-1',
        paciente=paciente
    )

    assert procedimiento.id == 'proc-1'
    assert procedimiento.paciente is paciente
    assert procedimiento.estado == EstadoProcedimiento.ACTIVO
    assert procedimiento.actos_clinicos == []
    assert procedimiento.informe_inicial is None


def test_crear_procedimiento_con_id_vacio_lanza_error():
    with pytest.raises(ValueError):
        crear_procedimiento(id='')


def test_crear_procedimiento_sin_paciente_lanza_error():
    with pytest.raises(ValueError):
        EntityProcedimiento('proc-2', paciente=None)


def test_crear_procedimiento_con_paciente_invalido_lanza_error():
    with pytest.raises(ValueError):
        EntityProcedimiento('proc-3', paciente='no es paciente')


def test_registrar_acto_clinico_valido():
    procedimiento = crear_procedimiento()
    consulta = crear_consulta()

    procedimiento.registrar_acto_clinico(consulta)

    assert procedimiento.actos_clinicos == [consulta]


def test_registrar_acto_clinico_no_duplica_misma_instancia():
    procedimiento = crear_procedimiento()
    consulta = crear_consulta()

    procedimiento.registrar_acto_clinico(consulta)
    procedimiento.registrar_acto_clinico(consulta)

    assert procedimiento.actos_clinicos == [consulta]
    assert len(procedimiento.actos_clinicos) == 1


def test_registrar_acto_clinico_no_duplica_acto_con_mismo_id():
    procedimiento = crear_procedimiento()

    consulta_1 = crear_consulta(id='cons-duplicada')
    consulta_2 = crear_consulta(id='cons-duplicada')

    procedimiento.registrar_acto_clinico(consulta_1)
    procedimiento.registrar_acto_clinico(consulta_2)

    assert procedimiento.actos_clinicos == [consulta_1]
    assert len(procedimiento.actos_clinicos) == 1


def test_registrar_varios_actos_clinicos_distintos():
    procedimiento = crear_procedimiento()
    consulta = crear_consulta(id='cons-1')
    prueba = crear_prueba(id='pr-1')

    procedimiento.registrar_acto_clinico(consulta)
    procedimiento.registrar_acto_clinico(prueba)

    assert consulta in procedimiento.actos_clinicos
    assert prueba in procedimiento.actos_clinicos
    assert len(procedimiento.actos_clinicos) == 2


def test_registrar_acto_clinico_invalido_lanza_error():
    procedimiento = crear_procedimiento()

    with pytest.raises(ValueError):
        procedimiento.registrar_acto_clinico('no es un acto clínico')


def test_registrar_acto_clinico_invalido_no_modifica_historial():
    procedimiento = crear_procedimiento()
    consulta = crear_consulta()

    procedimiento.registrar_acto_clinico(consulta)

    with pytest.raises(ValueError):
        procedimiento.registrar_acto_clinico('no es un acto clínico')

    assert procedimiento.actos_clinicos == [consulta]


def test_getter_actos_clinicos_devuelve_copia_y_no_permite_mutar_lista_interna():
    procedimiento = crear_procedimiento()
    consulta = crear_consulta(id='cons-original')

    procedimiento.registrar_acto_clinico(consulta)

    actos_obtenidos = procedimiento.actos_clinicos
    prueba_externa = crear_prueba(id='pr-externa')

    actos_obtenidos.append(prueba_externa)

    assert procedimiento.actos_clinicos == [consulta]
    assert prueba_externa not in procedimiento.actos_clinicos


def test_obtener_consulta_devuelve_none_si_no_hay_consulta():
    procedimiento = crear_procedimiento()

    assert procedimiento.obtener_consulta() is None


def test_obtener_consulta_devuelve_consulta_registrada():
    procedimiento = crear_procedimiento()
    consulta = crear_consulta(id='cons-1')
    prueba = crear_prueba(id='pr-1')

    procedimiento.registrar_acto_clinico(consulta)
    procedimiento.registrar_acto_clinico(prueba)

    assert procedimiento.obtener_consulta() is consulta


def test_obtener_consulta_ignora_pruebas_y_devuelve_none_si_solo_hay_pruebas():
    procedimiento = crear_procedimiento()
    prueba = crear_prueba(id='pr-1')

    procedimiento.registrar_acto_clinico(prueba)

    assert procedimiento.obtener_consulta() is None


def test_obtener_pruebas_pendientes_devuelve_solo_pruebas_pendientes():
    procedimiento = crear_procedimiento()
    consulta = crear_consulta(id='cons-1')
    prueba_pendiente = crear_prueba(id='pr-pendiente', pendiente=True)
    prueba_completada = crear_prueba(id='pr-completada', pendiente=False)

    procedimiento.registrar_acto_clinico(consulta)
    procedimiento.registrar_acto_clinico(prueba_pendiente)
    procedimiento.registrar_acto_clinico(prueba_completada)

    assert procedimiento.obtener_pruebas_pendientes() == [prueba_pendiente]


def test_obtener_pruebas_pendientes_devuelve_lista_vacia_si_no_hay_pendientes():
    procedimiento = crear_procedimiento()
    consulta = crear_consulta(id='cons-1')
    prueba_completada = crear_prueba(id='pr-completada', pendiente=False)

    procedimiento.registrar_acto_clinico(consulta)
    procedimiento.registrar_acto_clinico(prueba_completada)

    assert procedimiento.obtener_pruebas_pendientes() == []


def test_finalizar_procedimiento_sin_pruebas_pendientes():
    procedimiento = crear_procedimiento()

    procedimiento.finalizar()

    assert procedimiento.estado == EstadoProcedimiento.FINALIZADO


def test_finalizar_procedimiento_con_pruebas_pendientes_lanza_error():
    procedimiento = crear_procedimiento()
    prueba = crear_prueba(pendiente=True)

    procedimiento.registrar_acto_clinico(prueba)

    with pytest.raises(ValueError):
        procedimiento.finalizar()


def test_finalizar_procedimiento_con_pruebas_pendientes_no_modifica_estado():
    procedimiento = crear_procedimiento()
    prueba = crear_prueba(pendiente=True)

    procedimiento.registrar_acto_clinico(prueba)

    with pytest.raises(ValueError):
        procedimiento.finalizar()

    assert procedimiento.estado == EstadoProcedimiento.ACTIVO


def test_vincular_informe_valido():
    procedimiento = crear_procedimiento()
    informe = crear_informe()

    procedimiento.vincular_informe(informe)

    assert procedimiento.informe_inicial is informe


def test_vincular_informe_invalido_lanza_error():
    procedimiento = crear_procedimiento()

    with pytest.raises(ValueError):
        procedimiento.vincular_informe('no es informe')


def test_vincular_informe_invalido_no_modifica_informe_actual():
    procedimiento = crear_procedimiento()
    informe = crear_informe()

    procedimiento.vincular_informe(informe)

    with pytest.raises(ValueError):
        procedimiento.vincular_informe('no es informe')

    assert procedimiento.informe_inicial is informe


def test_no_permite_vincular_dos_informes_iniciales():
    procedimiento = crear_procedimiento()
    informe_1 = crear_informe(id='inf-1')
    informe_2 = crear_informe(id='inf-2')

    procedimiento.vincular_informe(informe_1)

    with pytest.raises(ValueError):
        procedimiento.vincular_informe(informe_2)

    assert procedimiento.informe_inicial is informe_1


def test_vincular_informe_a_procedimiento_finalizado_lanza_error():
    procedimiento = crear_procedimiento()
    informe = crear_informe()

    procedimiento.finalizar()

    with pytest.raises(ValueError):
        procedimiento.vincular_informe(informe)


def test_vincular_informe_a_procedimiento_finalizado_no_modifica_informe():
    procedimiento = crear_procedimiento()
    informe = crear_informe()

    procedimiento.finalizar()

    with pytest.raises(ValueError):
        procedimiento.vincular_informe(informe)

    assert procedimiento.informe_inicial is None


def test_registrar_acto_en_procedimiento_finalizado_lanza_error():
    procedimiento = crear_procedimiento()
    consulta = crear_consulta()

    procedimiento.finalizar()

    with pytest.raises(ValueError):
        procedimiento.registrar_acto_clinico(consulta)


def test_registrar_acto_en_procedimiento_finalizado_no_modifica_historial():
    procedimiento = crear_procedimiento()
    consulta = crear_consulta()

    procedimiento.finalizar()

    with pytest.raises(ValueError):
        procedimiento.registrar_acto_clinico(consulta)

    assert procedimiento.actos_clinicos == []


def test_dos_procedimientos_con_mismo_id_son_iguales():
    procedimiento_1 = crear_procedimiento(
        id='proc-igual',
        paciente=crear_paciente(id='pac-1', dni='12345678A')
    )

    procedimiento_2 = crear_procedimiento(
        id='proc-igual',
        paciente=crear_paciente(id='pac-2', dni='87654321B')
    )

    assert procedimiento_1 == procedimiento_2


def test_dos_procedimientos_con_distinto_id_no_son_iguales():
    procedimiento_1 = crear_procedimiento(id='proc-1')
    procedimiento_2 = crear_procedimiento(id='proc-2')

    assert procedimiento_1 != procedimiento_2


def test_procedimiento_no_se_compara_con_otro_tipo():
    procedimiento = crear_procedimiento()

    assert procedimiento.__eq__('no es procedimiento') is NotImplemented


def test_hash_depende_del_id():
    procedimiento_1 = crear_procedimiento(id='proc-hash')
    procedimiento_2 = crear_procedimiento(id='proc-hash')

    assert hash(procedimiento_1) == hash(procedimiento_2)


def test_str_contiene_id_dni_paciente_y_estado():
    paciente = crear_paciente(dni='12345678A')
    procedimiento = crear_procedimiento(
        id='proc-str',
        paciente=paciente
    )

    representacion = str(procedimiento)

    assert 'Procedimiento proc-str' in representacion
    assert '12345678A' in representacion
    assert EstadoProcedimiento.ACTIVO.value in representacion


def test_repr_contiene_nombre_de_clase_id_y_estado():
    procedimiento = crear_procedimiento(id='proc-repr')

    representacion = repr(procedimiento)

    assert 'EntityProcedimiento' in representacion
    assert 'proc-repr' in representacion
    assert EstadoProcedimiento.ACTIVO.value in representacion