from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, redirect, url_for
import secrets
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# create the db
db = SQLAlchemy()

# create the app
def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blueprints.db'
    db.init_app(app)
    app.config['SECRET_KEY'] = secrets.token_bytes(32)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from .users.models import User

    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(uid)
    
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for('core.index'))
    
    # hash password when we create users and hash passwords when we store passwords
    # using cryptographically secure bcrypt
    bcrypt = Bcrypt(app)
    app.extensions['BCRYPT'] = bcrypt

    # import and register all blueprints
    from .users.views import users
    from .people.views import people
    from .todos.views import todos
    from .core.views import core
    app.register_blueprint(core)
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(people, url_prefix='/people')
    app.register_blueprint(todos, url_prefix='/todos')

    migrate = Migrate(app, db)

    return app