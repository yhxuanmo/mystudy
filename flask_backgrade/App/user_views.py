from flask import Blueprint, render_template, request, redirect, url_for

from App.models import db, Role, User, Permission

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/auto_add_permission/')
def auto_add_permission():
    permission_name_list = ['查看班级', '添加班级', '查看学生', '添加学生', '查看角色', '添加角色', '查看权限', '添加权限']
    permission_list = []
    for name in permission_name_list:
        permission_list.append(Permission(name))
    db.session.add_all(permission_list)
    db.session.commit()
    return '自动添加权限成功'


@user_blueprint.route('/permission/')
def show_permission():
    permission_list = Permission.query.order_by('p_id').all()
    return render_template('permissions.html', permission_list=permission_list)


@user_blueprint.route('/add_permission/', methods=['GET', 'POST'])
def add_permission():
    if request.method == 'GET':
        return render_template('addpermission.html')
    if request.method == 'POST':
        p_name = request.form.get('p_name')
        if Permission.query.filter(Permission.p_name == p_name).first():
            return render_template('addpermission.html', msg='该班级已经存在')
        db.session.add(Permission(p_name))
        db.session.commit()
        return redirect(url_for('user.show_permission'))


@user_blueprint.route('/role/')
def show_role():
    role_list = Role.query.order_by('r_id').all()
    return render_template('roles.html', role_list=role_list)


@user_blueprint.route('/add_role/', methods=['GET', 'POST'])
def add_role():
    if request.method == 'GET':
        return render_template('addroles.html')
    if request.method == 'POST':
        r_name = request.form.get('r_name')
        if Role.query.filter(Role.r_name == r_name).first():
            return render_template('addroles.html', msg='该班级已经存在')
        db.session.add(Role(r_name))
        db.session.commit()
        return redirect(url_for('user.show_role'))
