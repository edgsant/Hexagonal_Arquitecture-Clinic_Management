from datetime import datetime

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt
from application.dtos.PacienteDTOs import RegistrarPacienteRequestDTO

paciente_bp = Blueprint("paciente", __name__)

@paciente_bp.route("/pacientes", methods=["POST"])
@jwt_required()
def registrar_paciente():
    """
    Endpoint para registrar un paciente. Protegido por JWT.
    """
    claims = get_jwt()
    rol_usuario = claims.get("rol")
  
    if rol_usuario != "Urologo":
        return jsonify({"error": "No tienes permisos (rol insuficiente) para realizar esta acción."}), 403

    datos_json = request.get_json()

    if datos_json is None:
        return jsonify({"error": "El body debe ser JSON"}), 400

    # 1. EL MAPEO (Responsabilidad del Blueprint)
    # Extraemos y convertimos el string a Date antes de tocar el DTO
    if 'fecha_nacimiento' in datos_json and isinstance(datos_json['fecha_nacimiento'], str):
        try:
            datos_json['fecha_nacimiento'] = datetime.strptime(datos_json['fecha_nacimiento'], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}), 400

    # 2. INSTANCIACIÓN DEL DTO 
    try:
        dto = RegistrarPacienteRequestDTO(**datos_json)
    except Exception as e:
        # Capturamos cualquier error de validación del DTO (tipos, nulos...)
        return jsonify({"error": str(e)}), 400

    service = current_app.container.servicioRegistrarPaciente()

    try:
        service_response = service.registrar_paciente(dto)

        return jsonify({
            "mensaje": "Paciente registrado exitosamente.",
            "paciente": {
                "id": service_response.id,
                "dni": service_response.dni,
                "nombre": service_response.nombre,
                "apellidos": service_response.apellidos
            }
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # 1. Imprimimos el error real y la línea exacta en la terminal de Flask
        import traceback
        traceback.print_exc() 
        
        # 2. Devolvemos el error real en el JSON para poder leerlo
        return jsonify({
            "error": "Error interno del servidor",
            "detalle_real": str(e),
            "tipo_de_error": e.__class__.__name__
        }), 500
    


@paciente_bp.route("/pacientes/<id>/procedimientos", methods=["GET"])
@jwt_required()
def obtener_procedimientos_paciente(id: str):

    claims = get_jwt()
    rol_usuario = claims.get("rol")
    
    if rol_usuario != "Urologo":
        return jsonify({"error": "No tienes permisos (rol insuficiente) para realizar esta acción."}), 403

    service = current_app.container.servicioConsultarProcedimiento()

    try:
        lista_dtos = service.consultar_procedimientos_paciente(id)
        
        return jsonify([
            {
                "id_procedimiento": dto.id_procedimiento,
                "estado": dto.estado,
                "paciente_id": dto.paciente_id,
                "paciente_nombre_completo": dto.paciente_nombre_completo
            }
            for dto in lista_dtos
        ]), 200

    except (TypeError, ValueError) as e:
        return jsonify({"error": f"Petición inválida: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor al procesar la consulta."}), 500


@paciente_bp.route("/pacientes/<id>/procedimientos/activo", methods=["GET"])
@jwt_required()
def obtener_procedimiento_activo(id: str):
    """
    Busca si un paciente específico tiene un tratamiento/procedimiento clínico en curso actualmente.
    """
    claims = get_jwt()
    rol_usuario = claims.get("rol")
    roles_medicos_permitidos = ["Urologo", "AnalistaClinico"]
    
    if rol_usuario not in roles_medicos_permitidos:
        return jsonify({"error": "Acceso denegado. Se requiere perfil de especialista médico."}), 403
    
    service = current_app.container.servicioConsultarProcedimiento()

    try:
        dto_activo = service.consultar_procedimiento_activo_paciente(id)
        
        return jsonify({
            "id_procedimiento": dto_activo.id_procedimiento,
            "estado": dto_activo.estado,
            "paciente_id": dto_activo.paciente_id,
            "paciente_nombre_completo": dto_activo.paciente_nombre_completo
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor."}), 500


