from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import getenv, path

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # Use a simpler database path for development
    db_path = getenv("DATABASE_URL", "sqlite:///dev.db")
    
    app.config.from_mapping(
        SECRET_KEY=getenv("SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI=db_path,
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    from .models import Patient, Sample, TestOrder  # noqa: F401
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # Create tables if they don't exist (for Railway deployment)
        try:
            db.create_all()
        except Exception as e:
            print(f"Database initialization warning: {e}")
        
        from .routes import bp
        app.register_blueprint(bp)

    @app.context_processor
    def inject_globals():
        return {"APP_NAME": "Specimen Tracker"}

    return app
