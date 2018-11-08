from flask import Flask, render_template, url_for, request, flash, redirect, send_from_directory
from flask_pymongo import PyMongo
import pymongo  #document-oriented database
import urllib  # in coordination with an RFC
import json
from bson import ObjectId
from werkzeug import secure_filename
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xml', 'csv'])

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

username = "debrsa01"
password = "imdaBEST65"
client = pymongo.MongoClient("mongodb://%s:%s@cluster0-shard-00-00-mhqmc.mongodb.net:27017,cluster0-shard-00-01-mhqmc.mongodb.net:27017,cluster0-shard-00-02-mhqmc.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true" % (username, password))

db = client.test_database
test_database = db.test_database

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)



@app.route("/", methods=['GET', 'POST'])
def index():
    result_dict = test_database.find_one({"project":"senior project"})
    return render_template('index.html', result=result_dict)


# working with uploads

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   # if request.method == 'POST':
   #    f = request.files['file']
   #    file1 = f.save(secure_filename(f.filename))
   #    return 'file uploaded successfully'
    if request.method == 'POST':
    # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

# let's try some rank checking
@app.route('/rankinput')
def my_form():
    return render_template('rankinput.html')

@app.route("/rankinput", methods=['POST'])
def rank_check():
    username = urllib.parse.quote_plus('debrsa01')
    password = urllib.parse.quote_plus('imdaBEST65')
    client = pymongo.MongoClient("mongodb://%s:%s@cluster0-shard-00-00-mhqmc.mongodb.net:27017,cluster0-shard-00-01-mhqmc.mongodb.net:27017,cluster0-shard-00-02-mhqmc.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true" % (username, password))
    db = client.groups
    # dictionary for all the groups that we have
    group_dict = {"aniministry":db.aniministry,"bigbrother":db.bigbrother}
    # let' get the text from the input box
    text = request.form['text']
    group,email = text.split(",")
    # print("group, email:", group, email)

    # Now let's see if the user is in the group
    if group_dict[group].find_one():
        check_group = group_dict[group].find_one()
        if email in check_group['Senpai']:
            result = "You are a Senpai"
        elif email in check_group['Kouhai']:
            result = "You are a Kouhai"
        elif email in check_group['Senpai'] and email in check_group['Kouhai']:
            # We don't yet have a way to prevent names from being in both, so this'll be our reminder
            result = "Somehow, you are both a senpai AND a kouhai. We should probably get that fixed."
        else:
            result = "You are not registered in this group"
    else:
        result = "Group name not found"

    return result
    # aniministry = db.aniministry
    # if group.find_one({"Senpai":["debrsa01@luther.edu"]}):
    #     result = group.find_one({"Kouhai":["debrsa01@luther.edu"]})
    # if group.find_one({"Senpai":["debrsa01@luther.edu"]}):
    #     result = group.find_one({"Senpai":["debrsa01@luther.edu"]})


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/google08f628c29bd0d05f.html")
def aftersignin():
    return render_template('google08f628c29bd0d05f.html')

@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html')

# @app.route('/getmethod/<jsdata>')
# def get_javascript_data(jsdata):

#     return jsdata

# @app.route('/test')
# def get_request_form():
#     text = request.form['text']
#     return 

if __name__ == '__main__':
    app.run(debug = True)
