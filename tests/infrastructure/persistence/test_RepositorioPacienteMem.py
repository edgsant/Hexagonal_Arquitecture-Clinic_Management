from domain.entities.EntityPaciente import EntityPaciente


def test_guardar_y_obtener_paciente_por_id_y_dni(repo_paciente_mem, paciente_entity):
    repo_paciente_mem.guardar_paciente(paciente_entity)

    assert repo_paciente_mem.obtener_por_id("pac-456-uuid") is paciente_entity
    assert repo_paciente_mem.obtener_por_dni("12345678A") is paciente_entity


def test_obtener_por_id_devuelve_none_si_no_existe(repo_paciente_mem):
    assert repo_paciente_mem.obtener_por_id("unknown-id") is None
    assert repo_paciente_mem.obtener_por_dni("00000000Z") is None


def test_guardar_varios_pacientes_mantiene_diferentes_indices(repo_paciente_mem, paciente_entity):
    otro_paciente = EntityPaciente(
        id="pac-789-uuid",
        dni="87654321B",
        fecha_nacimiento=paciente_entity.fecha_nacimiento,
        nombre="Lucia",
        apellidos="Martinez",
        direccion="Calle Nueva 12",
        telefono="611223345"
    )

    repo_paciente_mem.guardar_paciente(paciente_entity)
    repo_paciente_mem.guardar_paciente(otro_paciente)

    assert repo_paciente_mem.obtener_por_id("pac-456-uuid") is paciente_entity
    assert repo_paciente_mem.obtener_por_dni("87654321B") is otro_paciente
    assert repo_paciente_mem.obtener_por_id("pac-789-uuid") is otro_paciente
