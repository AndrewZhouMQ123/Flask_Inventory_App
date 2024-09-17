from flask import request, Blueprint, render_template
from website import db
from .models import Todo
from flask_login import login_required, current_user

todos = Blueprint('todos', __name__, template_folder='templates')

@todos.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'GET':
        return render_template('todos.html')
    elif request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        done_str = request.form.get('done')
        if done_str == "yes":
            done = True
        if done_str == "no":
            done = False
        todo = Todo(title=title, description=description, done=done, user_id=current_user.id)
        db.session.add(todo)
        db.session.commit()
        return render_template('todos.html') 
    
@todos.route('/details/<id>')
@login_required
def details(id):
    todo = Todo.query.filter(Todo.id == id).first()
    return render_template('details.html', todo=todo)