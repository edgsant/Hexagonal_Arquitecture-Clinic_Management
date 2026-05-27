from .EntityEspecialista import EntityEspecialista


class EntityAnalistaClinico(EntityEspecialista):
    """
    Entidad que representa a un analista clínico.

    No añade atributos propios respecto a EntityEspecialista, pero permite
    distinguir por tipo a los especialistas encargados de registrar resultados
    de analíticas dentro del sistema.
    """
    pass