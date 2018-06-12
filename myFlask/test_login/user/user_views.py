from flask import Blueprint, request, render_template, redirect, url_for, session, make_response

from user.models import db, User
from utils.ckeckLogin import checkLogin


user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/')
def hello():
    return 'hello'


@user_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('passwd')
        user = User.query.filter_by(s_name=username).all()
        if not user:
            return render_template('login.html', msg='用户名或密码错误')
        if password != user[0].s_password:
            return render_template('login.html', msg='用户名或密码错误')
        session['s_id'] = str(user[0].s_id)
        # temp = redirect(url_for('user.success'))
        temp = redirect('/user/success/')
        response = make_response(temp)
        response.set_cookie('s_id',str(user[0].s_id))
        return response



@user_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('passwd')
        repassword = request.form.get('repasswd')
        if not all([username, password, password]):
            return render_template('register.html', msg='请填写所有内容')
        if User.query.filter_by(s_name=username).all():
            return render_template('register.html', msg='用户名已存在')
        if password != repassword:
            return render_template('register.html', msg='两次密码不一致')
        user = User(s_name=username, s_password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.login'))


@user_blueprint.route('/logout/', methods=['GET'])
def logout():
    if request.method == 'GET':
        temp = redirect(url_for('user.login'))
        response = make_response(temp)
        response.delete_cookie('s_id')
        return response



@user_blueprint.route('/success/', methods=['GET'])
@checkLogin
def success():
    if request.method == 'GET':
        return render_template('other.html')


@user_blueprint.route('/create_db/', methods=['GET'])
def create_db():
    db.create_all()
    return '创建成功'

