from App.models import db


def ext_init(app):
    db.init_app(app=app)