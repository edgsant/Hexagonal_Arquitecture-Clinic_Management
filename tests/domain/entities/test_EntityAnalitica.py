from datetime import date
import pytest

from domain.entities.EntityAnalitica import EntityAnalitica
from domain.entities.EntityAnalistaClinico import EntityAnalistaClinico


def test_crear_analitica_y_registrar_resultados():
    analista = EntityAnalistaClinico(
        id='ana-10',
        nombre='María',
        apellidos='Ruiz',
        dni='12345678A',
        fecha_nacimiento=date(1987, 9, 9),
        direccion='Calle del Laboratorio 2',
        telefono='611223344'
    )
    analitica = EntityAnalitica('an-1', date.today(), [analista])

    assert analitica.pendiente is True
    assert analitica.psa is None

    analitica.registrar_resultados(
        psa='1.4 ng/mL',
        leucocitos='6.5 x10^3/µL',
        hemoglobina='14.2 g/dL',
        hematocrito='42.5 %',
        plaquetas='250 x10^3/µL',
        creatinina='0.9 mg/dL',
        glucosa='95 mg/dL',
        colesterol='185 mg/dL',
        observaciones='Resultados normales.',
        analista=analista
    )

    assert analitica.pendiente is False
    assert analitica.psa == '1.4 ng/mL'
    assert analitica.leucocitos == '6.5 x10^3/µL'
    assert analitica.observaciones == 'Resultados normales.'

    with pytest.raises(ValueError):
        analitica.registrar_resultados(
            psa='1.5 ng/mL',
            leucocitos='6.4 x10^3/µL',
            hemoglobina='14.0 g/dL',
            hematocrito='42.0 %',
            plaquetas='240 x10^3/µL',
            creatinina='0.8 mg/dL',
            glucosa='90 mg/dL',
            colesterol='180 mg/dL',
            observaciones='Repetición de resultados.',
            analista=analista
        )
