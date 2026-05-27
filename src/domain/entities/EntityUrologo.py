from .EntityEspecialista import EntityEspecialista


class EntityUrologo(EntityEspecialista):
    """
    Entidad que representa a un urólogo.

    No añade atributos propios respecto a EntityEspecialista, pero permite
    distinguir por tipo a los especialistas responsables de registrar informes
    clínicos iniciales, crear procedimientos o realizar acciones propias del
    urólogo dentro del sistema.
    """
    pass