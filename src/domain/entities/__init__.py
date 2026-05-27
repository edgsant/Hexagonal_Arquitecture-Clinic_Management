# src/domain/entities/__init__.py

from .EntityEspecialista import EntityEspecialista
from .EntityUrologo import EntityUrologo
from .EntityAnalistaClinico import EntityAnalistaClinico
from .EntityUsuario import EntityUsuario
from .EntityPaciente import EntityPaciente
from .EntityInformeInicial import EntityInformeInicial
from .EntityActoClinico import EntityActoClinico
from .EntityPrueba import EntityPrueba
from .EntityAnalitica import EntityAnalitica
from .EntitySolicitud import EntitySolicitud
from .EntityConsulta import EntityConsulta
from .EntityProcedimiento import EntityProcedimiento, EstadoProcedimiento

# El __all__ asegura que solo se exporte lo que nosotros queremos
__all__ = [
    'EntityEspecialista',
    'EntityUrologo',
    'EntityAnalistaClinico',
    'EntityUsuario',
    'EntityPaciente',
    'EntityInformeInicial',
    'EntityActoClinico',
    'EntityPrueba',
    'EntityAnalitica',
    'EntitySolicitud',
    'EntityConsulta',
    'EntityProcedimiento',
    'EstadoProcedimiento'
]