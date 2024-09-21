from flask import request, Blueprint, render_template, flash, redirect, url_for, jsonify
from website import db
from .models import Todo
from flask_login import login_required, current_user
from datetime import datetime

todos = Blueprint('todos', __name__, template_folder='templates')

@todos.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'GET':
        return render_template('todos.html')
    elif request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        duedate = request.form.get('due_date')
        due_date = datetime.strptime(duedate, '%Y-%m-%dT%H:%M')
        todo = Todo(title=title, description=description, due_date=due_date, user_id=current_user.id)
        db.session.add(todo)
        db.session.commit()
        return render_template('todos.html') 

@todos.route('/todos_json')
def get_todos():
    todos = current_user.todos
    todos_list = [todo.to_dict() for todo in todos]
    return jsonify(todos_list)

@todos.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if request.method == 'GET':
        todo = Todo.query.filter(Todo.id == id).first()
        return render_template('todos_edit.html', todo=todo)
    elif request.method == 'POST':
        todo = Todo.query.filter(Todo.id == id).first()
        title = request.form.get('title')
        description = request.form.get('description')
        done_str = request.form.get('done')
        if done_str == "yes":
                done = True
        if done_str == "no":
                done = False
        duedate = request.form.get('due_date')
        due_date = datetime.strptime(duedate, '%Y-%m-%dT%H:%M')
        todo.set_title(title)
        todo.set_description(description)
        todo.set_done(done)
        todo.set_duedate(due_date)
        db.session.commit()
        flash('Todo details updated successfully!', 'success')
        return redirect(url_for('todos.index'))
    
@todos.route('/delete/<id>', methods=['DELETE'])
@login_required
def delete(id):
    Todo.query.filter(Todo.id == id).delete()
    db.session.commit()
    return {'success': True}, 200