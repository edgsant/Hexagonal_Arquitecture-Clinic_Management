from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token

from application.excepciones import CredencialesInvalidas

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Inicia sesión y devuelve un token JWT.
    """
    datos_json = request.get_json()

    if datos_json is None:
        return jsonify({"error": "El body debe ser JSON"}), 400

    dto = LoginRequestDTO(**datos_jason)
    service = current_app.container.servicioIniciarSesion()
    service_response = service.login(dto)

    token = create_access_token(
        identity=service_response.usuario_id,
        additional_claims={
            "especialista_id": service_response.especialista_id,
            "rol": service_response.rol
        }
    )

    return jsonify({
        "access_token": token,
        "usuario_id": service_response.usuario_id,
        "especialista_id": service_response.especialista_id,
        "rol": service_response.rol
    }), 200