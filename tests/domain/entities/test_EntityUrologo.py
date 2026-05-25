from datetime import date

from domain.entities.EntityUrologo import EntityUrologo


def test_urologo_hereda_validaciones_y_representacion():
    urologo = EntityUrologo(
        id='uro-1',
        nombre='David',
        apellidos='Gómez',
        dni='12345678A',
        fecha_nacimiento=date(1978, 3, 12),
        direccion='Calle Urología 1',
        telefono='611223344'
    )

    assert urologo.id == 'uro-1'
    assert urologo.dni == '12345678A'
    assert 'David Gómez' in str(urologo)
