from flask import Flask, render_template
from flask_talisman import Talisman

app = Flask(__name__)
Talisman(app, content_security_policy=[])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/people')
def people():
    return render_template('list_people.html')

@app.route('/people/<name>')
def person(name=None):
    return render_template('person.html', name=name)