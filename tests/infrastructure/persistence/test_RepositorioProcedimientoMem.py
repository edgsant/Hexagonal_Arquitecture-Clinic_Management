def test_obtener_procedimiento_por_id_devuelve_none_si_no_existe(repo_procedimiento_mem):
    assert repo_procedimiento_mem.obtener_procedimiento_por_id("missing") is None


def test_guardar_y_obtener_procedimiento_por_id(repo_procedimiento_mem, procedimiento_entity):
    repo_procedimiento_mem.guardar_procedimiento(procedimiento_entity)

    assert repo_procedimiento_mem.obtener_procedimiento_por_id(procedimiento_entity.id) is procedimiento_entity


def test_obtener_activo_por_paciente_retorna_procedimiento_activo(repo_procedimiento_mem, procedimiento_entity):
    repo_procedimiento_mem.guardar_procedimiento(procedimiento_entity)

    assert repo_procedimiento_mem.obtener_activo_por_paciente(procedimiento_entity.paciente.id) is procedimiento_entity


def test_obtener_procedimientos_por_paciente_agrupa_por_id(repo_procedimiento_mem, procedimiento_entity, procedimiento_factory):
    repo_procedimiento_mem.guardar_procedimiento(procedimiento_entity)

    otro_procedimiento = procedimiento_factory("proc-1000")
    repo_procedimiento_mem.guardar_procedimiento(otro_procedimiento)

    assert repo_procedimiento_mem.obtener_procedimientos_por_paciente(procedimiento_entity.paciente.id) == [procedimiento_entity, otro_procedimiento]


def test_obtener_procedimientos_activos_devuelve_solo_activos(repo_procedimiento_mem, procedimiento_entity, procedimiento_factory):
    repo_procedimiento_mem.guardar_procedimiento(procedimiento_entity)

    finalizado = procedimiento_factory("proc-1000")
    finalizado.finalizar()
    repo_procedimiento_mem.guardar_procedimiento(finalizado)

    assert repo_procedimiento_mem.obtener_procedimientos_activos() == [procedimiento_entity]


def test_obtener_activo_por_paciente_devuelve_none_si_no_hay_activo(repo_procedimiento_mem, procedimiento_entity):
    procedimiento_entity.finalizar()
    repo_procedimiento_mem.guardar_procedimiento(procedimiento_entity)

    assert repo_procedimiento_mem.obtener_activo_por_paciente(procedimiento_entity.paciente.id) is None


def test_obtener_procedimientos_por_paciente_devuelve_lista_vacia_si_no_existe(repo_procedimiento_mem):
    assert repo_procedimiento_mem.obtener_procedimientos_por_paciente("pac-no-existe") == []
