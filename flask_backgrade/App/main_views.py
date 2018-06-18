from flask import Blueprint, render_template, request, redirect, url_for
from flask_sqlalchemy import Pagination

from random import randint, choice

from App.models import db, Grade, Student

main_blueprint = Blueprint('main',__name__)


@main_blueprint.route('/')
def show_index():
    return render_template('index.html')


@main_blueprint.route('/head/')
def show_head():
    return render_template('head.html')


@main_blueprint.route('/left/')
def show_left():
    return render_template('left.html')


@main_blueprint.route('/grade/')
def show_grade():
    grade_list = Grade.query.all()
    return render_template('grade.html', grade_list=grade_list)


@main_blueprint.route('/student/', methods=['GET', 'POST'])
def show_student():
    if request.method == 'GET':
        page = int(request.args.get('page',1))
        page_count = 10
        paginate = Student.query.order_by('s_id').paginate(page, page_count,error_out=False)
        student_list = paginate.items

        return render_template('student.html', student_list=student_list, paginate=paginate)


@main_blueprint.route('/stu_of_grade/',methods=['GET'])
def stu_of_grade():
    if request.method == 'GET':
        g_id = request.args.get('g_id')
        page = int(request.args.get('page',1))
        page_count = 10
        grade = Grade.query.get(g_id)
        paginate = Student.query.filter_by(grades=g_id).paginate(page, page_count,error_out=False)
        student_list = paginate.items
        return render_template('stu_of_grade.html',grade=grade, student_list=student_list, paginate=paginate)


@main_blueprint.route('/add_grade/', methods=['GET', 'POST'])
def add_grade():
    if request.method == 'GET':
        return render_template('addgrade.html')
    if request.method == 'POST':
        g_name = request.form.get('grade_name')
        if Grade.query.filter(Grade.g_name == g_name).first():
            return render_template('addgrade.html', msg='该班级已经存在')
        db.session.add(Grade(g_name))
        db.session.commit()
        return redirect(url_for('main.show_grade'))


@main_blueprint.route('/add_student/', methods=['GET', 'POST'])
def add_student():
    if request.method == 'GET':
        grades = Grade.query.all()
        return render_template('addstu.html', grades=grades)
    if request.method == 'POST':
        s_name = request.form.get('s_name')
        g_id = request.form.get('g_id')
        stu = Student(s_name)
        stu.grades = g_id

        db.session.add(stu)
        db.session.commit()
        return redirect(url_for('main.show_student'))



@main_blueprint.route('/create_table/')
def create_table():
    db.create_all()
    return '创建成功'


@main_blueprint.route('/auto_add_grade/')
def auto_add_grade():
    grade_name_list = ['python', 'java', 'php', 'c', 'c++', 'js']
    grade_list = []
    for name in grade_name_list:
        grade_list.append(Grade(name))
    db.session.add_all(grade_list)
    db.session.commit()
    return '自动添加班级成功'

@main_blueprint.route('/auto_add_student/')
def auto_add_student():
    firstname_list = ['赵', '钱', '孙', '李', '周', '武', '郑', '王', '杨', '唐', '刘','方']
    lastname_list = ['倩倩', '微微', '萌萌', '珠珠', '点点', '姗姗', '娜娜', '玉玉', '婉婉', '琪琪', '依依', '思思', '迪迪', '霏霏', '珂珂', '乐乐', '米米']
    student_list = []
    for i in range(100):
        name = choice(firstname_list)+choice(lastname_list)
        stu = Student(name)
        stu.grades = randint(1,6)
        student_list.append(stu)

    db.session.add_all(student_list)
    db.session.commit()
    return '自动添加学生成功'