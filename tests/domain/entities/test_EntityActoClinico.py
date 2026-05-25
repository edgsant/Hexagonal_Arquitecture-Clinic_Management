from datetime import date
import pytest

from domain.entities.EntityPrueba import EntityPrueba
from domain.entities.EntityAnalistaClinico import EntityAnalistaClinico


def test_anadir_especialista_y_no_duplicar():
    analista = EntityAnalistaClinico(
        id='ana-6',
        nombre='Patricia',
        apellidos='López',
        dni='66666666A',
        fecha_nacimiento=date(1984, 6, 6),
        direccion='Calle Salud 6',
        telefono='611223344'
    )
    prueba = EntityPrueba('pr-5', date.today(), [analista])

    assert prueba.especialistas == [analista]

    prueba.anadir_especialista(analista)
    assert prueba.especialistas == [analista]

    especialista_nuevo = EntityAnalistaClinico(
        id='ana-7',
        nombre='Andrés',
        apellidos='Delgado',
        dni='77777777B',
        fecha_nacimiento=date(1981, 1, 1),
        direccion='Calle Salud 7',
        telefono='611223344'
    )
    prueba.anadir_especialista(especialista_nuevo)

    assert especialista_nuevo in prueba.especialistas
    assert len(prueba.especialistas) == 2

    with pytest.raises(ValueError):
        prueba.anadir_especialista('no es especialista')
