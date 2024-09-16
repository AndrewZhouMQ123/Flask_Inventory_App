
from flask import render_template, Blueprint, request
from flask_login import login_required
from website import db
from .models import Person

people = Blueprint('people', __name__, template_folder='templates')

@people.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'GET':
        people = Person.query.all()
        return render_template('peoples.html', people=people)
    elif request.method == 'POST':
        name = request.form.get('name')
        age = int(request.form.get('age'))
        job = request.form.get('job')

        person = Person(name=name, age=age, job=job)
        db.session.add(person)
        db.session.commit()

        people = Person.query.all()
        return render_template('people.html', people=people)
        
@people.route('/delete/<pid>', methods=['DELETE'])
@login_required
def delete(pid):
    Person.query.filter(Person.pid == pid).delete()

    db.session.commit()
    people = Person.query.all()
    return render_template('people.html', people=people)

@people.route('/details/<pid>')
@login_required
def details(pid):
    person = Person.query.filter(Person.pid == pid).first()
    return render_template('details.html', person=person)