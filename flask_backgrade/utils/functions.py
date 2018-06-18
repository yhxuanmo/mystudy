import os
from flask import Flask


from App.main_views import main_blueprint
from App.user_views import user_blueprint
from utils.ext_init import ext_init


def create_app():
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(BASE_DIR, 'static')
    templates_dir = os.path.join(BASE_DIR, 'templates')

    app = Flask(__name__,
                static_folder=static_dir,
                template_folder=templates_dir)
    app.register_blueprint(blueprint=main_blueprint,url_prefix='/index')
    app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/db_flask'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    ext_init(app)

    return app
