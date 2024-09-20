from flask import request, Blueprint, render_template, flash, redirect, url_for, jsonify
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
        duedate = request.form.get('duedate')
        if done_str == "yes":
            done = True
        if done_str == "no":
            done = False
        todo = Todo(title=title, description=description, done=done, due_date=duedate, user_id=current_user.id)
        db.session.add(todo)
        db.session.commit()
        return render_template('todos.html') 

@todos.route('/todos_json')
def get_todos():
    # Assuming you have a function to get the current user's todos
    todos = current_user.todos
    return jsonify(todos)
    
@todos.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if request.method == 'GET':
        todo = Todo.query.filter(Todo.id == id).first()
        return render_template('todos/edit.html', todo=todo)
    elif request.method == 'POST':
        todo = Todo.query.filter(Todo.id == id).first()
        done_str = request.form.get('done')
        if done_str == "yes":
                done = True
        if done_str == "no":
                done = False
        duedate = request.form.get('duedate')
        todo.set_done(done)
        todo.set_duedate(duedate)
        db.session.commit()
        flash('Todo details updated successfully!', 'success')
        return redirect(url_for('todos.index'))
    
@todos.route('/delete/<id>', methods=['DELETE'])
@login_required
def delete(id):
    Todo.query.filter(Todo.id == id).delete()
    db.session.commit()
    return render_template('todos.html')