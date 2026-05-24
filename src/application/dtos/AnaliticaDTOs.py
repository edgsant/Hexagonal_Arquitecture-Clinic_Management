from dataclasses import dataclass

@dataclass(frozen=True)
class RegistrarResultadosRequestDTO:
    """DTO de entrada: Todos los datos que rellenará el Analista en su pantalla."""
    procedimiento_id: str
    analitica_id: str
    especialista_id: str # Extraído del token de sesión
    psa: str
    leucocitos: str
    hemoglobina: str
    hematocrito: str
    plaquetas: str
    creatinina: str
    glucosa: str
    colesterol: str
    observaciones: str

    def __post_init__(self):
        # En Python podemos iterar los campos para acortar las líneas repetitivas de strings
        campos_str = [
            ("procedimiento_id", self.procedimiento_id),
            ("analitica_id", self.analitica_id),
            ("especialista_id", self.especialista_id),
            ("psa", self.psa),
            ("leucocitos", self.leucocitos),
            ("hemoglobina", self.hemoglobina),
            ("hematocrito", self.hematocrito),
            ("plaquetas", self.plaquetas),
            ("creatinina", self.creatinina),
            ("glucosa", self.glucosa),
            ("colesterol", self.colesterol),
            ("observaciones", self.observaciones)
        ]

        for nombre, valor in campos_str:
            if not isinstance(valor, str):
                raise TypeError(f"El campo '{nombre}' debe ser un string.")

        # Validamos los IDs obligatorios que guían el dominio
        if not self.procedimiento_id.strip(): raise ValueError("El campo 'procedimiento_id' es obligatorio.")
        if not self.analitica_id.strip(): raise ValueError("El campo 'analitica_id' es obligatorio.")
        if not self.especialista_id.strip(): raise ValueError("El campo 'especialista_id' es obligatorio.")


@dataclass(frozen=True)
class AnaliticaResponseDTO:
    """DTO de salida: Devuelve el estado actualizado de la analítica."""
    analitica_id: str
    analista_id: str
    pendiente: bool
    psa: str
    leucocitos: str
    hemoglobina: str
    hematocrito: str
    plaquetas: str
    creatinina: str
    glucosa: str
    colesterol: str
    observaciones: str

    def __post_init__(self):
        if not isinstance(self.pendiente, bool):
            raise TypeError("El campo 'pendiente' debe ser un booleano.")
            
        campos_str = [
            ("analitica_id", self.analitica_id), ("analista_id", self.analista_id),
            ("psa", self.psa), ("leucocitos", self.leucocitos), ("hemoglobina", self.hemoglobina),
            ("hematocrito", self.hematocrito), ("plaquetas", self.plaquetas), ("creatinina", self.creatinina),
            ("glucosa", self.glucosa), ("colesterol", self.colesterol), ("observaciones", self.observaciones)
        ]

        for nombre, valor in campos_str:
            if not isinstance(valor, str):
                raise TypeError(f"El campo '{nombre}' debe ser un string.")
        
        if not self.analitica_id.strip(): raise ValueError("El campo 'analitica_id' es obligatorio.")