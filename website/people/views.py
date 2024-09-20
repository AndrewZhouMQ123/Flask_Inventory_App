
from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from website import db
from .models import Person

people = Blueprint('people', __name__, template_folder='templates')

@people.route('/', methods=['GET'])
@login_required
def index():
    if request.method == 'GET':
        people = Person.query.all()
        return render_template('people.html', people=people)
    
@people.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'GET':
        return render_template('profile.html')
    elif request.method == 'POST':
        name = request.form.get('name')
        age = int(request.form.get('age'))
        job = request.form.get('job')

        person = Person(name=name, age=age, job=job, user_id=current_user.id)
        db.session.add(person)
        db.session.commit()
        return render_template('profile.html')

@people.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'GET':
        return render_template('ppl_edit.html')
    elif request.method == 'POST':
        name = request.form.get('name')
        age = int(request.form.get('age'))
        job = request.form.get('job')
        
        # Fetch the existing person record for the current user
        person = Person.query.filter_by(user_id=current_user.id).first()
        
        if person:
            # Update existing person details
            person.name = name
            person.age = age
            person.job = job
            
            db.session.commit()
            flash('Person details updated successfully!', 'success')
        else:
            # Handle the case where there is no person associated with the current user
            flash('No person record found for the current user.', 'error')
        
        return redirect(url_for('people.profile'))

@people.route('/delete/<id>', methods=['DELETE'])
@login_required
def delete(id):
    Person.query.filter(Person.id == id).delete()

    db.session.commit()
    people = Person.query.all()
    return render_template('people.html', people=people)

@people.route('/details/<id>')
@login_required
def details(id):
    person = Person.query.filter(Person.id == id).first()
    return render_template('details.html', person=person)