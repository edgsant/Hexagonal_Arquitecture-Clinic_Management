from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt

blueprint_paciente = Blueprint("paciente", __name__)

@blueprint_paciente.route("/pacientes", methods=["POST"])
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

    dto = RegistrarPacienteRequestDTO(**datos_json)
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
        return jsonify({"error": "Error interno del servidor"}), 500
    


@blueprint_paciente.route("/pacientes/<id>/pocedimientos", methods=["GET"])
@jwt_required()
def obtener_procedimiento_paciente(id: str):
    
    claims = get_jwt()
    rol_usuario = claims.get("rol")
  
    if rol_usuario != "Urologo":
        return jsonify({"error": "No tienes permisos (rol insuficiente) para realizar esta acción."}), 403

    datos_json = request.get_json()

    if datos_json is None:
        return jsonify({"error": "El body debe ser JSON"}), 400
    


