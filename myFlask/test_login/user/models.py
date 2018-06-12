from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    s_id = db.Column(db.INTEGER, autoincrement=True, primary_key=True)
    s_name = db.Column(db.String(16), unique=True)
    s_password = db.Column(db.String(32))
    s_sex = db.Column(db.Boolean, default=1)
    s_age = db.Column(db.INTEGER)

    __tablename__ = 'user'