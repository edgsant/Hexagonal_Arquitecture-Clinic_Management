from enum import Enum
from typing import Optional
from .EntityPaciente import EntityPaciente
from .EntityInformeInicial import EntityInformeInicial
from .EntityActoClinico import EntityActoClinico
from .EntityConsulta import EntityConsulta
from .EntityPrueba import EntityPrueba

class EstadoProcedimiento(Enum): 
    """<<enumeration>> según el DCD."""
    ACTIVO = "Activo"
    FINALIZADO = "Finalizado"

class EntityProcedimiento:
    """
    Aggregate Root principal del Dominio.
    Orquesta el expediente médico, garantizando sus invariantes y ciclo de vida.
    """
    def __init__(self, id: str, paciente: EntityPaciente):
        if not id:
            raise ValueError("El procedimiento debe tener un ID válido.")
        if not isinstance(paciente, EntityPaciente):
            raise ValueError("El procedimiento debe pertenecer a un EntityPaciente válido.")

        self._id = id
        self._paciente = paciente
        self._estado = EstadoProcedimiento.ACTIVO
        
        # Colecciones y referencias encapsuladas (Composiciones en el DCD)
        self._actos_clinicos: list[EntityActoClinico] = []
        self._informe_inicial: Optional[EntityInformeInicial] = None

    # --- GETTERS ---

    @property
    def id(self) -> str: return self._id

    @property
    def paciente(self) -> EntityPaciente: return self._paciente

    @property
    def estado(self) -> EstadoProcedimiento: return self._estado

    @property
    def informe_inicial(self) -> Optional[EntityInformeInicial]: return self._informe_inicial

    @property
    def actos_clinicos(self) -> list[EntityActoClinico]: 
        """Devuelve copia de los actos para evitar manipulaciones externas."""
        return list(self._actos_clinicos)


    # --- MÉTODOS DE NEGOCIO (Estrictamente según el DCD) ---

    def vincular_informe(self, informe: EntityInformeInicial) -> None:
        """
        +vincularInforme(informe : InformeInicial)
        Relaciona el informe inicial de valoración con este procedimiento.
        """
        if self._estado != EstadoProcedimiento.ACTIVO:
            raise ValueError("Regla de Negocio: No se puede alterar un procedimiento finalizado.")
        if not isinstance(informe, EntityInformeInicial):
            raise ValueError("El informe debe ser una instancia válida de EntityInformeInicial.")
            
        self._informe_inicial = informe

    def obtener_consulta(self) -> Optional[EntityConsulta]:
        """
        +obtenerConsulta() : EntityConsulta
        Recupera la consulta médica asociada a este procedimiento (si existe).
        """
        for acto in self._actos_clinicos:
            if isinstance(acto, EntityConsulta):
                return acto
        return None

    def obtener_pruebas_pendientes(self) -> list[EntityPrueba]:
        """
        +obtenerPruebasPendientes() : EntityPrueba[*]
        Filtra el historial devolviendo únicamente las pruebas que no están completadas.
        """
        # Usamos List Comprehension Pythónica, validando el tipo y la propiedad 'pendiente'
        return [acto for acto in self._actos_clinicos 
                if isinstance(acto, EntityPrueba) and acto.pendiente]

    def finalizar(self) -> None:
        """
        +finalizar() : void
        Cambia el estado del procedimiento garantizando la invariante de negocio.
        """
        if self.obtener_pruebas_pendientes():
            raise ValueError("Regla de Negocio: No se puede dar de alta al paciente si existen pruebas pendientes.")
            
        self._estado = EstadoProcedimiento.FINALIZADO


    # --- MÉTODOS DE GESTIÓN INTERNA DEL AGREGADO ---

    def registrar_acto_clinico(self, acto: EntityActoClinico) -> None:
        """
        Método necesario para alimentar el rombo negro de composición del DCD.
        Añade consultas o pruebas al historial del procedimiento.
        """
        if self._estado != EstadoProcedimiento.ACTIVO:
            raise ValueError("No se pueden añadir actos a un procedimiento finalizado.")
        if not isinstance(acto, EntityActoClinico):
            raise ValueError("Debe ser un EntityActoClinico válido.")
            
        if acto not in self._actos_clinicos:
            self._actos_clinicos.append(acto)


    # --- MÉTODOS MÁGICOS (Identidad DDD) ---

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EntityProcedimiento): return NotImplemented
        return self._id == other.id

    def __hash__(self) -> int: return hash(self._id)

    def __str__(self) -> str:
        """
        Representación legible y resumida del expediente clínico.
        Ideal para mostrar en interfaces de usuario o logs generales.
        """
        return f"Procedimiento {self._id} | Paciente: {self._paciente.dni} | Estado: {self._estado.value}"

    def __repr__(self) -> str:
        return f"<EntityProcedimiento id={self._id} estado={self._estado.value}>"