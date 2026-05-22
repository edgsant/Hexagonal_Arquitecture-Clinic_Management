# src/domain/ports/__init__.py

from .IRepositorioUsuario import IRepositorioUsuario
from .IRepositorioPaciente import IRepositorioPaciente
from .IRepositorioProcedimiento import IRepositorioProcedimiento

__all__ = [
    'IRepositorioUsuario',
    'IRepositorioPaciente',
    'IRepositorioProcedimiento'
]