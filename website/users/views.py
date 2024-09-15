# views.py or routes.py
import os
import uuid
import pandas as pd
from flask import render_template, request, Response, flash, make_response, send_from_directory, session, redirect, url_for, Blueprint, current_app
from flask_login import login_user, logout_user, current_user, login_required

from website import db
from .models import User

users = Blueprint('users', __name__, template_folder='templates')
# def register_routes(app, db, bcrypt):
        # by default methods only get
@users.route('/', methods=['GET', 'POST'])
def index():
    return render_template('users.html')

@users.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        bcrypt = current_app.extensions['BCRYPT']
        hashed_password = bcrypt.generate_password_hash(password)

        user = User(username=username, password=hashed_password)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.login'))

@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter(User.username == username).first()
        bcrypt = current_app.extensions['BCRYPT']
        if bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Successful Login!')
            return redirect(url_for('core.index'))
        else:
            flash('Login failed. username or password is wrong.')
            return redirect(url_for('login'))

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.index'))

@users.route('/secret')
@login_required
def secret():
    if current_user.role == 'admin':
        return 'My secret message!'
    else:
        return 'No Permission'
    
@users.route('/booking')
@login_required
def booking():
    return render_template('booking.html', user=current_user)

@users.route('/file_upload', methods=['GET', 'POST'])
@login_required
def file_upload():
    if request.method == 'GET':
        return render_template('fileupload.html')
    elif request.method == 'POST':
        file = request.files['file']
        if file.content_type == 'text/plain':
            return file.read().decode()
        elif file.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" or file.content_type == "application/vnd.ms-excel":
            df = pd.read_excel(file)
            return df.to_html()
        
@users.route('/convert_csv', methods=['POST'])
@login_required
def convert_csv():
    file = request.files['file']
    df = pd.read_excel(file)
    response = Response(
        df.to_csv(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachement; filename=result.csv'}
    )
    return response

@users.route('/convert_csv_two', methods=['POST'])
@login_required
def convert_csv_two():
    file = request.files['file']
    df = pd.read_excel(file)

    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    filename = f'{uuid.uuid4()}.csv'
    df.to_csv(os.path.join('downloads', filename))

    return render_template('download.html', filename=filename)

@users.route('/download')
@login_required
def download(filename):
    return send_from_directory('downloads', filename, download_name='result.csv')

# sessions and cookies
@users.route('/set_data')
def set_data():
    # session data is something sensitive, should not be changed by user, should not be seen by the user
    session['name'] = 'Andrew'
    return render_template('index.html', message='Session data set.')

@users.route('/get_data')
def get_data():
    if 'name' in session.keys():
        name = session['name']
        return render_template('index.html', message= f'name {name}')
    else:
        return render_template('index.html', message= 'No session found')
    
@users.route('/clear_session')
def clear_session():
    session.clear()
    return render_template('index.html', message='Session cleared')

@users.route('/set_cookie')
def set_cookie():
    # instruct browser to set cookie on client side
    response = make_response(render_template('index.html', message='Cookie set.'))
    response.set_cookie('cookie_name', 'cookie_value')
    return response

@users.route('/get_cookie')
def get_cookie():
    cookie_value = request.cookies['cookie_name']
    return render_template('index.html', message=f'Cookie Value: {cookie_value}')

@users.route('/remove_cookie')
def remove_cookie():
    response = make_response(render_template('index.html', message='Cookie removed.'))
    response.set_cookie('cookie_name', expires=0)
    return response