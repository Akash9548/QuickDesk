from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from .routes.user import user_bp
    app.register_blueprint(user_bp)

    from .routes.agent import agent_bp
    app.register_blueprint(agent_bp)
    
    from .routes.comment import comment_bp
    app.register_blueprint(comment_bp)
    
    from .routes.admin import admin_bp
    app.register_blueprint(admin_bp)

    return app
