import os

from flask import Flask
from flask_session import Session
import redis
from flask_sqlalchemy import SQLAlchemy

from App.hello_views import hello_blueprint

from App.user_views import user_blueprint

from App.models import db

def create_app():

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(BASE_DIR, 'static')
    templates_dir = os.path.join(BASE_DIR, 'templates')
    app = Flask(__name__,
                static_folder=static_dir,
                template_folder=templates_dir)
    app.register_blueprint(blueprint=hello_blueprint, url_prefix='/hello')
    app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')

    # 秘钥
    app.config['SECRET_KEY'] = 'secret_key'
    # session类型
    app.config['SESSION_TYPE'] = 'redis'
    # redis ip和端口，默认127.0.0.1:6379
    app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)
    # 配置数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/db_flask'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 第一种
    # sess = Session()
    # sess.init_app(app=app)
    # 第二种
    Session(app=app)
    db.init_app(app=app)

    return app
