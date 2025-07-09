from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from dotenv import load_dotenv
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()  # Initialize Flask-Mail instance

def create_app():
    load_dotenv(override=True)

    flask_app = Flask(__name__)
    flask_app.config.from_object('app.config.Config')

    # Initialize extensions with app
    db.init_app(flask_app)
    migrate.init_app(flask_app, db)
    mail.init_app(flask_app)   # Initialize mail with app

    # CORS setup
    CORS(flask_app, resources={r"/*": {"origins": flask_app.config['FRONTEND_ORIGIN']}}, supports_credentials=True)

    # Import all models
    import app.models

    # Middleware
    from app.middleware.session_verify import session_verify
    session_verify(flask_app)

    # Blueprints
    from app.routes.auth import auth_bp
    from app.routes.organizations import organization_bp
    from app.routes.clinical_trials import clinicaltrials_bp
    from app.routes.researchers import researchers_bp

    flask_app.register_blueprint(auth_bp, url_prefix='/auth')
    flask_app.register_blueprint(organization_bp, url_prefix='/api')
    flask_app.register_blueprint(clinicaltrials_bp, url_prefix='/api')
    flask_app.register_blueprint(researchers_bp, url_prefix='/api')

    return flask_app
