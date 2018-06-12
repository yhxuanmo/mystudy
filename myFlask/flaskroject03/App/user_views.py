from flask import Blueprint, request, render_template, make_response, session

from App.models import db, Student

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/setcookie/')
def set_cookie():
    temp = render_template('cookies.html')
    # 创建响应时可以绑定页面
    response = make_response(temp)
    # set_cookie(key, value, max_age, expires)
    response.set_cookie('ticket', '123123', max_age=10)

    return response


@user_blueprint.route('/delcookie/')
def del_cookie():
    temp = render_template('cookies.html')
    # 创建响应时可以绑定页面
    response = make_response(temp)
    response.delete_cookie('ticket')

    return response


@user_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        passwd = request.form.get('passwd')
        session['username'] = username
        session['password'] = passwd

        return render_template('login.html', username=username, passwd=passwd)


@user_blueprint.route('/scores/', methods=['GET'])
def stu_scores():
    scores = [90, 80, 68, 97, 77]
    content_h2 = '<h2>仙剑奇侠传</h2>'
    return render_template('scores.html', scores=scores, content_h2=content_h2)


@user_blueprint.route('/create_db/')
def create_db():
    db.create_all()
    return '创建成功'


@user_blueprint.route('/drop_db/')
def drop_db():
    db.drop_all()
    return '删除成功'


@user_blueprint.route('/create_stu/', methods=['GET'])
def create_stu():
    stu = Student()
    stu.s_name = 'yy'
    stu.s_age = '21'

    db.session.add(stu)
    db.session.commit()
    return '添加学生成功'


@user_blueprint.route('/select_stu/', methods=['GET'])
def select_stu():
    # stus = Student.query.filter(Student.s_name == 'xx')
    # stus = Student.query.filter_by(s_name='yy')
    # stus = Student.query.all()
    # stus = Student.query

    # 改
    # stu = Student.query.filter_by(s_name='xx').first()
    # stu.s_age = 18
    # db.session.add(stu)
    # db.session.commit()
    # 删
    # stu = Student.query.filter_by(s_name='xx').first()
    # db.session.delete(stu)
    # db.session.commit()
    # return render_template('students.html', stus=stus)
    return '操作成功'
