import os
from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from .routes.BlueprintAuth import auth_bp
from .routes.BlueprintPaciente import paciente_bp
from .routes.BlueprintProcedimiento import procedimiento_bp


def crear_app():
    """
    Crea y configura la aplicación Flask.

    Registra los blueprints y configura JWT.
    """
    load_dotenv()

    jwt_secret_key = os.getenv("JWT_SECRET_KEY")

    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = jwt_secret_key
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False

    JWTManager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(paciente_bp)
    app.register_blueprint(procedimiento_bp)

    @app.route('/health')
    def health():
        return {'status': 'ok'}, 200
    
    return app
