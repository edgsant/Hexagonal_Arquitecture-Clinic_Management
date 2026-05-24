from domain.puertos import IRepositorioProcedimiento
from domain.procedimiento import Procedimiento

class ServicioDarAlta:
    def __init__(self, repo_procedimiento: IRepositorioProcedimiento):
        self.repo_procedimiento = repo_procedimiento

    def finalizar_procedimiento(self, id_procedimiento: str) -> Procedimiento:
        """CU07: Finaliza el procedimiento clínico (da de alta al paciente)."""
        
        # 1. Recuperamos el Aggregate Root desde la infraestructura
        procedimiento = self.repo_procedimiento.obtener_por_id(id_procedimiento)
        if not procedimiento:
            raise ValueError(f"No se encontró ningún procedimiento clínico con el ID: {id_procedimiento}")

        # 2. REGLA DE NEGOCIO: Delegamos en el dominio la mutación y sus validaciones
        # (Por ejemplo, el dominio comprobará que no esté ya FINALIZADO o que no tenga pruebas pendientes)
        try:
            procedimiento.finalizar() 
        except Exception as error:
            # Si el dominio deniega el alta (ej: hay analíticas pendientes), lanzamos el error a Flask
            raise ValueError(str(error))

        # 3. Guardamos el estado actualizado del Aggregate Root
        self.repo_procedimiento.guardar(procedimiento)

        return procedimiento