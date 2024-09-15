from flask import request, Blueprint
from website import db
from .models import Todo

todos = Blueprint('todos', __name__, template_folder='templates')

@todos.route('/')
def index():
    todos = Todo.query.all()
    return todos

@todos.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return "GET"
    elif request.method == 'POST':
        return "POST"