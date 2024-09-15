from flask import render_template, Blueprint

core = Blueprint('core', __name__, template_folder='templates')

@core.route('/')
def index():
    return render_template('index.html')

@core.route('/about')
def about():
    return render_template('about.html')

@core.route('/contact')
def contact():
    return render_template('contact.html')