from flask import Flask
from config import Config
from extensions import db, migrate, bcrypt, jwt
from flask_cors import CORS  # ✅ new import
from app import models  # import all models


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # ✅ Enable CORS so frontend (React/PWA) can make requests
    CORS(app, origins="*")  
    # You can restrict later, for example:
    # CORS(app, origins=["http://localhost:3000", "https://yourfrontend.com"])

    # ✅ Register Blueprints
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
