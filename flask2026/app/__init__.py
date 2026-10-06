import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from app.extensions import db, migrate
from flasgger import Swagger

load_dotenv()

def create_app():
    app = Flask(__name__)

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set")

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": "http://localhost:5173"
            }
        }
    )

    # ВАЖНО: импортируем модели,
    # чтобы Alembic их увидел
    from app import models

    from app.api.employees.routes import employees_bp
    from app.api.vacations.routes import vacations_bp

    swagger = Swagger(app)

    app.register_blueprint(employees_bp)
    app.register_blueprint(vacations_bp)

    return app
