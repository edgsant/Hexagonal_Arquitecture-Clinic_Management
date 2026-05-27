from datetime import date
from werkzeug.security import generate_password_hash
from transversal.container import Container
from transversal.config import Config
from infrastructure.presentation.app import crear_app
from domain.entities.EntityPaciente import EntityPaciente
from domain.entities.EntityProcedimiento import EntityProcedimiento
from domain.entities.EntityUsuario import EntityUsuario
from domain.entities.EntityUrologo import EntityUrologo
from domain.entities.EntityAnalistaClinico import EntityAnalistaClinico
from domain.entities.EntityInformeInicial import EntityInformeInicial
from domain.entities.EntityAnalitica import EntityAnalitica


def poblar_repositorios_en_memoria(container: Container):
    config = container.config
    print(f"Usando repositorios: {config.tipoRepositorio.value}")
    if config.usaSQL():
        print(f"Base de datos: {config.db_url}")

    repo_pacientes = container.factory.crearRepoPaciente()
    repo_procedimientos = container.factory.crearRepoProcedimiento()
    repo_usuarios = container.factory.crearRepoUsuario()

    especialista1 = EntityUrologo(
        id="esp1",
        nombre="Carlos García",
        apellidos="López Ramírez",
        dni="12345678A",
        fecha_nacimiento=date(1975, 3, 15),
        direccion="Calle Principal 42, Madrid",
        telefono="600123456"
    )

    especialista2 = EntityAnalistaClinico(
        id="esp2",
        nombre="María José",
        apellidos="Fernández Martín",
        dni="87654321B",
        fecha_nacimiento=date(1980, 7, 22),
        direccion="Avenida Central 15, Madrid",
        telefono="610234567"
    )
    print(f"\nEspecialistas creados:")
    print(f"  - {especialista1.nombre} {especialista1.apellidos} (Urólogo)")
    print(f"  - {especialista2.nombre} {especialista2.apellidos} (Analista Clínico)")

    usuario1 = EntityUsuario(
        id="u1",
        email="carlos.garcia@clinica.com",
        username="cgarcia",
        password_hash=generate_password_hash("password123"),
        especialista=especialista1
    )

    usuario2 = EntityUsuario(
        id="u2",
        email="maria.fernandez@clinica.com",
        username="mfernandez",
        password_hash=generate_password_hash("password456"),
        especialista=especialista2
    )
    repo_usuarios.guardar_usuario(usuario1)
    repo_usuarios.guardar_usuario(usuario2)
    print(f"\nUsuarios creados:")
    print(f"  - {usuario1.username} ({usuario1.email})")
    print(f"  - {usuario2.username} ({usuario2.email})")

    paciente1 = EntityPaciente(
        id="pac1",
        dni="11111111X",
        fecha_nacimiento=date(1960, 5, 10),
        nombre="Juan",
        apellidos="Pérez García",
        direccion="Calle Secundaria 8, Madrid",
        telefono="620111111"
    )

    paciente2 = EntityPaciente(
        id="pac2",
        dni="22222222Y",
        fecha_nacimiento=date(1965, 11, 25),
        nombre="Pedro",
        apellidos="López Martínez",
        direccion="Plaza Mayor 3, Madrid",
        telefono="630222222"
    )
    repo_pacientes.guardar_paciente(paciente1)
    repo_pacientes.guardar_paciente(paciente2)
    print(f"\nPacientes creados:")
    print(f"  - {paciente1.nombre} {paciente1.apellidos} (DNI: {paciente1.dni})")
    print(f"  - {paciente2.nombre} {paciente2.apellidos} (DNI: {paciente2.dni})")

    procedimiento1 = EntityProcedimiento(
        id="proc1",
        paciente=paciente1
    )

    procedimiento2 = EntityProcedimiento(
        id="proc2",
        paciente=paciente2
    )
    repo_procedimientos.guardar_procedimiento(procedimiento1)
    repo_procedimientos.guardar_procedimiento(procedimiento2)
    print(f"\nProcedimientos creados:")
    print(f"  - Procedimiento {procedimiento1.id} para {paciente1.nombre} (Estado: {procedimiento1.estado.value})")
    print(f"  - Procedimiento {procedimiento2.id} para {paciente2.nombre} (Estado: {procedimiento2.estado.value})")

    informe1 = EntityInformeInicial(
        id="inf1",
        fecha=date.today(),
        antecedentes="Hipertensión controlada desde hace 10 años",
        sintomas="Disuria y polaquiuria leve",
        antecedentes_familiares="Padre con cáncer de próstata",
        exploracion_fisica="Próstata aumentada de tamaño",
        autor=especialista1
    )

    informe2 = EntityInformeInicial(
        id="inf2",
        fecha=date.today(),
        antecedentes="Diabetes tipo 2 desde hace 5 años",
        sintomas="Molestias al orinar",
        antecedentes_familiares="Madre con diabetes",
        exploracion_fisica="Normalidad relativa",
        autor=especialista1
    )
    print(f"\nInformes iniciales creados:")
    print(f"  - Informe {informe1.id} por {especialista1.nombre}")
    print(f"  - Informe {informe2.id} por {especialista1.nombre}")

    analitica1 = EntityAnalitica(
        id="anal1",
        fecha=date.today(),
        especialistas=[especialista2],
        pendiente=True
    )

    analitica2 = EntityAnalitica(
        id="anal2",
        fecha=date.today(),
        especialistas=[especialista2],
        pendiente=True
    )
    print(f"\nAnalíticas creadas:")
    print(f"  - Analítica {analitica1.id} (Pendiente)")
    print(f"  - Analítica {analitica2.id} (Pendiente)")

    # 1. Metemos el informe y la analítica dentro del procedimiento 1
    procedimiento1.vincular_informe(informe1)
    procedimiento1.registrar_acto_clinico(analitica1)
    
    # 2. Actualizamos el procedimiento en el repositorio para que guarde los cambios
    repo_procedimientos.guardar_procedimiento(procedimiento1)

    print(f"\n✓ Repositorios poblados y listos para consultas desde Bruno.")


def main():
    config = Config()
    container = Container(config)
    poblar_repositorios_en_memoria(container)

    app = crear_app()
    app.container = container

    print("\nServidor Flask iniciado en http://127.0.0.1:5000")
    print("Manteniendo los repositorios en memoria activos mientras Flask esté en ejecución.")
    app.run(host="localhost", port=5000, debug=True)


if __name__ == "__main__":
    main()
