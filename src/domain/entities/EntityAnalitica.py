from datetime import date
from typing import Optional
from .EntityPrueba import EntityPrueba
from .EntityEspecialista import EntityEspecialista

class EntityAnalitica(EntityPrueba):
    """
    Entidad que representa una prueba analítica de sangre/orina.
    Hereda de EntityPrueba (y a su vez de EntityActoClinico).
    """
    def __init__(self, id: str, fecha: date, especialistas: list[EntityEspecialista], pendiente: bool = True):
        # Llamamos al superconstructor de la clase padre
        super().__init__(id, fecha, especialistas, pendiente)
        
        # Inicializamos los biomarcadores vacíos protegidos (se rellenarán en CU05)
        # Usamos Optional[str] porque nacen siendo None hasta que se registran
        self._psa: Optional[str] = None
        self._leucocitos: Optional[str] = None
        self._hemoglobina: Optional[str] = None
        self._hematocrito: Optional[str] = None
        self._plaquetas: Optional[str] = None
        self._creatinina: Optional[str] = None
        self._glucosa: Optional[str] = None
        self._colesterol: Optional[str] = None
        self._observaciones: Optional[str] = None

    # --- GETTERS ---
    
    @property
    def psa(self) -> Optional[str]: return self._psa
    
    @property
    def leucocitos(self) -> Optional[str]: return self._leucocitos

    @property
    def hemoglobina(self) -> Optional[str]: return self._hemoglobina

    @property
    def hematocrito(self) -> Optional[str]: return self._hematocrito

    @property
    def plaquetas(self) -> Optional[str]: return self._plaquetas

    @property
    def creatinina(self) -> Optional[str]: return self._creatinina

    @property
    def glucosa(self) -> Optional[str]: return self._glucosa

    @property
    def colesterol(self) -> Optional[str]: return self._colesterol

    @property
    def observaciones(self) -> Optional[str]: return self._observaciones

    # --- MÉTODOS DE NEGOCIO ---

    def registrar_resultados(self, psa: str, leucocitos: str, hemoglobina: str, 
                             hematocrito: str, plaquetas: str, creatinina: str, 
                             glucosa: str, colesterol: str, observaciones: str, 
                             analista: EntityEspecialista) -> None:
        """
        Regla de negocio: Guarda los resultados médicos y, automáticamente, 
        marca la prueba como completada registrando la firma del analista.
        """
        # 1. Asignamos los valores a los atributos internos
        self._psa = psa
        self._leucocitos = leucocitos
        self._hemoglobina = hemoglobina
        self._hematocrito = hematocrito
        self._plaquetas = plaquetas
        self._creatinina = creatinina
        self._glucosa = glucosa
        self._colesterol = colesterol
        self._observaciones = observaciones
        
        # 2. Delega el cambio de estado y la firma a la clase padre
        # Si la prueba ya estaba completada, este método lanzará ValueError
        # abortando la operación antes de que se guarde en la BD.
        self.marcar_completada(analista)

    # Nota: No necesitamos reescribir __eq__ ni __hash__ porque ya los 
    # hereda perfectamente de EntityActoClinico basados en el ID.