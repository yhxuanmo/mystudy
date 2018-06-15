from flask import Blueprint, render_template

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
    return render_template('grade.html')
