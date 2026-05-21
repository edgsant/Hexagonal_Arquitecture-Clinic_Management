from datetime import date
from .EntityActoClinico import EntityActoClinico
from .EntityEspecialista import EntityEspecialista

class EntityPrueba(EntityActoClinico):
    """
    Entidad que representa una prueba médica genérica en el sistema.
    Hereda la identidad, fecha y especialistas de ActoClinico,
    añadiendo el control de estado de finalización.
    """
    def __init__(self, id: str, fecha: date, especialistas: list[EntityEspecialista], pendiente: bool = True):
        # 1. Llamamos al superconstructor para inicializar las reglas base
        super().__init__(id, fecha, especialistas)
        
        # 2. Encapsulamos el atributo como protegido
        # Se permite inyectarlo (por si viene de la base de datos ya completado),
        # pero por defecto al nacer (crear una nueva) será True.
        self._pendiente = pendiente

    # --- GETTERS ---
    
    @property
    def pendiente(self) -> bool:
        """Permite consultar el estado, pero impide modificarlo directamente."""
        return self._pendiente

    # No creamos un @pendiente.setter. La única forma de cambiarlo es por negocio:

    # --- MÉTODOS DE NEGOCIO ---

    def marcar_completada(self, especialista: EntityEspecialista) -> None:
        """
        Regla de negocio (+marcar_completada): 
        Al completarse, deja de estar pendiente y registra al profesional que la ejecutó.
        """
        if not self._pendiente:
            raise ValueError("La prueba ya estaba completada y no puede volver a marcarse.")
            
        self._pendiente = False
        
        # Reutilizamos el comportamiento seguro heredado de EntityActoClinico
        self.anadir_especialista(especialista)