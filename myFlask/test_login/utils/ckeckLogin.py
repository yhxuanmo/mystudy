from flask import request, redirect, url_for, session



def checkLogin(func):
    def inner():
        s_id = request.cookies.get('s_id')
        if not s_id:
            return redirect(url_for('user.login'))
        if s_id == session.get('s_id'):
            return func()
        else:
            return redirect(url_for('user.login'))
    return inner