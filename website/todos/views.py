from flask import request, Blueprint
from website import db
from .models import Todo
from flask_login import login_required

todos = Blueprint('todos', __name__, template_folder='templates')

@todos.route('/')
@login_required
def index():
    todos = Todo.query.all()
    return todos

@todos.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'GET':
        return "GET"
    elif request.method == 'POST':
        return "POST"