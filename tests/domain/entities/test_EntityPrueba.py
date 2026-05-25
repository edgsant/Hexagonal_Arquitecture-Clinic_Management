from datetime import date
import pytest

from domain.entities.EntityPrueba import EntityPrueba
from domain.entities.EntityAnalistaClinico import EntityAnalistaClinico


def test_marcar_prueba_completada_y_estado():
    analista = EntityAnalistaClinico(
        id='ana-8',
        nombre='Sergio',
        apellidos='Torres',
        dni='88888888C',
        fecha_nacimiento=date(1976, 10, 10),
        direccion='Calle Prueba 20',
        telefono='611223344'
    )
    prueba = EntityPrueba('pr-6', date.today(), [analista])

    assert prueba.pendiente is True

    prueba.marcar_completada(analista)

    assert prueba.pendiente is False
    assert analista in prueba.especialistas

    with pytest.raises(ValueError):
        prueba.marcar_completada(analista)
