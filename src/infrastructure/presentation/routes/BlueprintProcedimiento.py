from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt

from application.dtos.InformeDTOs import RegistrarInformeRequestDTO
from application.dtos.AnaliticaDTOs import RegistrarResultadosRequestDTO

blueprint_procedimiento = Blueprint("procedimiento", __name__)

@blueprint_procedimiento.route("/procedimientos", methods=["POST"])
@jwt_required()
def crear_procedimiento():

    claims = get_jwt()
    if claims.get("rol") != "Urologo":
        return jsonify({"error": "No tienes permisos para realizar esta acción."}), 403

    datos_json = request.get_json()
    if datos_json is None:
        return jsonify({"error": "El cuerpo debe ser un JSON válido."}), 400

    service = current_app.container.servicioCrearProcedimiento()

    try:

        dto_salida = service.crear_procedimiento(**datos_json)

        return jsonify({
            "id_procedimiento": dto_salida.id_procedimiento,
            "estado": dto_salida.estado,
            "paciente_id": dto_salida.paciente_id,
            "paciente_nombre_completo": dto_salida.paciente_nombre_completo
        }), 201
    
    except (TypeError, ValueError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Error interno del servidor."}), 500

@blueprint_procedimiento.route("/procedimientos/<id>", methods=["GET"])
@jwt_required()
def consultar_procedimiento(id: str):

    claims = get_jwt()
    if claims.get("rol") != "Urologo":
        return jsonify({"error": "No tienes permisos para consultar expedientes."}), 403

    service = current_app.container.servicioConsultarProcedimiento()

    try:

        dto_salida = service.consultar_procedimiento(id)

        return jsonify({
            "id_procedimiento": dto_salida.id_procedimiento,
            "estado": dto_salida.estado,
            "paciente_id": dto_salida.paciente_id,
            "paciente_nombre_completo": dto_salida.paciente_nombre_completo
        }), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception:
        return jsonify({"error": "Error interno del servidor."}), 500


@blueprint_procedimiento.route("/procedimientos/<id>/informes", methods=["POST"])
@jwt_required()
def registrar_informe(id: str):

    claims = get_jwt()
    if claims.get("rol") != "Urologo":
        return jsonify({"error": "No tienes permisos para añadir informes clínicos."}), 403

    datos_json = request.get_json()
    if datos_json is None:
        return jsonify({"error": "El cuerpo debe ser un JSON válido."}), 400

    # Inyectamos de forma transparente los datos de contexto (id de la URL y especialista del token)
    datos_json["procedimiento_id"] = id
    datos_json["especialista_id"] = claims.get("especialista_id")

    service = current_app.container.servicioRegistrarInforme()

    try:
        # Instanciamos el DTO de entrada. Su __post_init__ validará la estructura de golpe
        dto_entrada = RegistrarInformeRequestDTO(**datos_json)
        dto_salida = service.registrar_informe(dto_entrada)
        
        return jsonify({
            "informe_id": dto_salida.informe_id,
            "procedimiento_id": dto_salida.procedimiento_id,
            "fecha": dto_salida.fecha.isoformat(),
            "mensaje": dto_salida.mensaje
        }), 201
    
    except (TypeError, ValueError) as e:
        return jsonify({"error": f"Datos de informe inválidos: {str(e)}"}), 400
    except Exception:
        return jsonify({"error": "Error interno al guardar el informe."}), 500


@blueprint_procedimiento.route("/procedimientos/<id>/analiticas", methods=["POST"])
@jwt_required()
def registrar_resultados(id: str):

    claims = get_jwt()
    if claims.get("rol") != "Analista":
        return jsonify({"error": "No autorizado. Solo el personal de laboratorio puede registrar analíticas."}), 403

    datos_json = request.get_json()
    if datos_json is None:
        return jsonify({"error": "El cuerpo debe ser un JSON válido."}), 400

    # Inyectamos de forma transparente los datos de contexto obligatorios
    datos_json["procedimiento_id"] = id
    datos_json["especialista_id"] = claims.get("especialista_id")

    service = current_app.container.servicioRegistrarResultados()

    try:

        dto_entrada = RegistrarResultadosRequestDTO(**datos_json)
        dto_salida = service.registrar_resultados(dto_entrada)
        
        return jsonify({
            "analitica_id": dto_salida.analitica_id,
            "analista_id": dto_salida.analista_id,
            "pendiente": dto_salida.pendiente,
            "observaciones": dto_salida.observaciones
        }), 201
    
    except (TypeError, ValueError) as e:
        return jsonify({"error": f"Datos biomédicos inválidos: {str(e)}"}), 400
    except Exception:
        return jsonify({"error": "Error interno al procesar los resultados analíticos."}), 500


@blueprint_procedimiento.route("/procedimientos/<id>/alta", methods=["PATCH"])
@jwt_required()
def dar_alta(id: str):
    claims = get_jwt()
    if claims.get("rol") != "Urologo":
        return jsonify({"error": "No tienes privilegios para otorgar altas médicas."}), 403

    service = current_app.container.servicioDarAlta()

    try:

        dto_salida = service.finalizar_procedimiento(id)

        return jsonify({
            "mensaje": "El alta se ha procesado correctamente. Procedimiento cerrado.",
            "id_procedimiento": dto_salida.id_procedimiento,
            "estado": dto_salida.estado,
            "paciente_nombre_completo": dto_salida.paciente_nombre_completo
        }), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Error interno al procesar el alta médica."}), 500