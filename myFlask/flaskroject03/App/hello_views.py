from flask import Blueprint, request, render_template

hello_blueprint = Blueprint('hello',__name__)


@hello_blueprint.route('/')
def hello():
    return 'hello'



