from domain.entities.EntityPaciente import EntityPaciente

class RepositorioPacienteMem:
    """
    Repositorio en memoria para pacientes.

    Implementa la interfaz RepositorioPaciente usando un diccionario en memoria.
    """
    def __init__(self):
        """
        Inicializa el repositorio con un diccionario vacío para cada tipo de clave.
        """
        self.pacientes_por_id = {}
        self.pacientes_por_dni = {}
    
    def guardar_paciente(self, paciente: EntityPaciente):
        """
        Agrega un paciente a los repositorios.

        Args:
            paciente: El paciente que se va aguardar.
        """
        self.pacientes_por_id[paciente.id] = paciente
        self.pacientes_por_dni[paciente.dni] = paciente

    def obtener_por_id(self, paciente_id: str):
        """
        Obtiene un paciente por su DNI.

        Args:
            paciente_dni: DNI del paciente.

        Returns:
            Paciente or None: El paciente si existe, None en caso contrario.
        """
        return self.pacientes_por_id.get(paciente_id)
    
    def obtener_por_dni(self, paciente_dni: str):
        """
        Obtiene un ejemplar por su DNI.

        Args:
            ejemplar_id: DNI del ejemplar.

        Returns:
            Paciente or None: El paciente si existe, None en caso contrario.
        """
        return self.pacientes_por_dni.get(paciente_dni)