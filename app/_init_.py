from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    
    load_dotenv(override=True)
    
    flask_app = Flask(__name__)   

    flask_app.config.from_object('app.config.Config')

    # Configure server to accept requests from this origin for all API endpoints.
    # supports_credentials=True means the server will accept and handle cookies or credentials sent from this origin.
    CORS(flask_app, resources={r"/*": {"origins": flask_app.config['FRONTEND_ORIGIN']}}, supports_credentials=True)

    db.init_app(flask_app)

    # all models which needs to be generated into db
    import app.models

    migrate.init_app(flask_app, db)

    from app.middleware.session_verify import session_verify
    session_verify(flask_app)

    from app.routes.auth import auth_bp
    flask_app.register_blueprint(auth_bp, url_prefix='/auth')
    
    return flask_app