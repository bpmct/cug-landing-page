from flask import Flask, render_template
import glob, os
from flask_talisman import Talisman

app = Flask(__name__)
Talisman(app, content_security_policy=[])

dir_path = os.path.dirname(os.path.realpath(__file__))

@app.route('/')
def home():
    people_folder = dir_path + "/templates/people"
    people_list = {}
    for file in os.listdir(people_folder):
        if file.endswith(".html") or file.endswith(".jinja"):
            # get their name with some string magic
            route = file.replace(".html", "")
            name = route.replace("_", " ").title()
            people_list[name] = route
    return render_template('index.html', people=people_list)
    
# Custom routes
@app.route('/people/ben_potter')
def ben(name="ben_potter"):
    # some special logic here
    print ("ben's special page")
    return render_template("people/{}.html".format(name), name=name)

# Basic routes with no special logic
@app.route('/people/<name>')
def person(name=None):
    return render_template("people/{}.html".format(name), name=name)