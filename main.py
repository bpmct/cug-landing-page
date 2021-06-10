from flask import Flask, render_template
import glob, os
from flask_talisman import Talisman
import re

app = Flask(__name__)
Talisman(app, content_security_policy=[])

# helpers
dir_path = os.path.dirname(os.path.realpath(__file__))
def replace_url_to_link(value):
    # Replace url to link
    urls = re.compile(r"((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)", re.MULTILINE|re.UNICODE)
    value = urls.sub(r'<a href="\1" target="_blank">\1</a>', value)
    # Replace email to mailto
    urls = re.compile(r"([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)", re.MULTILINE|re.UNICODE)
    value = urls.sub(r'<a href="mailto:\1">\1</a>', value)
    return value

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
    
# Custom pages and routes
@app.route('/people/ben_potter')
def ben(name="ben_potter"):
    # some special logic here
    print ("ben's special page")

    tweets_list = []
    import twint

    c = twint.Config()
    c.Username = "bpmct"
    c.Limit = 5
    c.Store_object = True
    c.Store_object_tweets_list = tweets_list

    # Run
    twint.run.Search(c)

    # tweets_list = twint.output.tweets_list
    # print(tweets_list)

    return render_template("people/{}.html".format(name), name=name, tweets=tweets_list[:10], replaceUrl=replace_url_to_link)

# Basic user routes with no special logic
@app.route('/people/<name>')
def person(name=None):
    return render_template("people/{}.html".format(name), name=name)