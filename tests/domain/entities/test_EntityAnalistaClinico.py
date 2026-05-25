from datetime import date

from domain.entities.EntityAnalistaClinico import EntityAnalistaClinico


def test_analista_clinico_hereda_validaciones_y_representacion():
    analista = EntityAnalistaClinico(
        id='ana-1',
        nombre='Elena',
        apellidos='Ruiz',
        dni='87654321Z',
        fecha_nacimiento=date(1988, 12, 5),
        direccion='Calle Analítica 5',
        telefono='+34611223344'
    )

    assert analista.id == 'ana-1'
    assert analista.dni == '87654321Z'
    assert 'Elena Ruiz' in str(analista)
