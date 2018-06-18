from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Student(db.Model):
    s_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    s_name = db.Column(db.String(16))
    grades = db.Column(db.Integer, db.ForeignKey('grade.g_id'), nullable=True)

    def __init__(self, name):
        self.s_name = name

    __tablename__ = 'student'


class Grade(db.Model):
    g_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    g_name = db.Column(db.String(32), unique=True)
    g_create_time = db.Column(db.DateTime, default=datetime.now)
    students = db.relationship('Student', backref='grade', lazy=True)

    def __init__(self, name):
        self.g_name = name

    __tablename__ = 'grade'


class User(db.Model):
    u_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    u_name = db.Column(db.String(16), unique=True)
    u_permission = db.Column(db.String(64),nullable=True)
    roles = db.Column(db.Integer, db.ForeignKey('role.r_id'), nullable=True)

    __tablename__ = 'user'


role_permission = db.Table('role_permission',
                           db.Column('r_id', db.Integer, db.ForeignKey('role.r_id'), primary_key=True),
                           db.Column('p_id', db.Integer, db.ForeignKey('permission.p_id'), primary_key=True)
                           )

class Role(db.Model):
    r_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    r_name = db.Column(db.String(16),unique=True)
    users = db.relationship('User', backref='role', lazy=True)
    permissions = db.relationship('Permission',secondary=role_permission,backref='role')

    def __init__(self, name):
        self.r_name = name

    __tablename__ = 'role'


class Permission(db.Model):
    p_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    p_name = db.Column(db.String(32), unique=True)

    def __init__(self, name):
        self.p_name = name

    __tablename__ = 'permission'



