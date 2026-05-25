from datetime import date
import pytest

from domain.entities.EntityInformeInicial import EntityInformeInicial
from domain.entities.EntityUrologo import EntityUrologo


def test_crear_informe_inicial_valido():
    autor = EntityUrologo(
        id='uro-6',
        nombre='Federico',
        apellidos='Pérez',
        dni='55555555A',
        fecha_nacimiento=date(1974, 2, 14),
        direccion='Calle Informes 8',
        telefono='611223344'
    )
    informe = EntityInformeInicial(
        id='inf-3',
        fecha=date.today(),
        antecedentes='Sin alergias.',
        sintomas='Molestia leve.',
        antecedentes_familiares='No aporta.',
        exploracion_fisica='Exploración normal.',
        autor=autor
    )

    assert informe.autor is autor
    assert 'Autor: Federico Pérez' in str(informe)
    assert 'EntityInformeInicial' in repr(informe)


def test_informe_inicial_con_autor_invalido_levanta_error():
    with pytest.raises(ValueError):
        EntityInformeInicial(
            id='inf-4',
            fecha=date.today(),
            antecedentes='Sin alergias.',
            sintomas='Molestia leve.',
            antecedentes_familiares='No aporta.',
            exploracion_fisica='Normal.',
            autor='no es un especialista'
        )
