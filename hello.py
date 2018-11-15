from flask import Flask, render_template, url_for, request, flash, redirect, send_from_directory
from flask_pymongo import PyMongo
import pymongo  #document-oriented database
import urllib  # in coordination with an RFC
import json
from bson import ObjectId
from werkzeug import secure_filename
import os
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import csv

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

useremail = "No user"


# when you log in, we will get that email address here
@app.route('/getemail', methods = ['POST'])
def get_post_javascript_data():
    jsdata = request.form['myData']
    print(jsdata, "has logged in")
    global useremail
    useremail = jsdata
    return jsdata


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

class MyOtherForm(FlaskForm):
    class Meta:
        csrf = False
        locales = ('en_US', 'en')
    group_name = StringField('Team', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])

class GetDataForGroupForm(FlaskForm):
    class Meta:
        csrf = False
        locales = ('en_US', 'en')
    group_name = StringField('Group', validators=[DataRequired()])

def read_csv_file(file):
    with open('uploads/' + file, newline='') as csvfile:
        file_reader = csv.reader(csvfile, delimiter=',')

        testDict = {}
        for row in file_reader:
            # print(', '.join(row))
            # print(row)
            testDict[row[0]] = row[1]
        print(testDict)
        return testDict

@app.route("/", methods=['GET', 'POST'])
def index():
    global useremail
    retrieve_data = "Not allowed to see this group's data"
    # forms
    otherform = MyOtherForm()
    getdataforgroupform = GetDataForGroupForm()
    if otherform.validate_on_submit():
        db = client.groups
        names = db.list_collection_names()
        if otherform.group_name.data not in names:
            # We'll want to create the group in the groups database
            print("We'll have to create the group")
            print("type of group_name is: ", type(otherform.group_name.data))
            new_group = db[otherform.group_name.data]
            new_group.insert_one({"Admin":[otherform.email.data], "Standard":[]})
            # Then we'll want to create a collection for that new group's data in the group_data database
            db = client.group_data
            new_group = db[otherform.group_name.data]
            new_group.insert_one({"Group creation":"Completed"})
        else:
            print("That team already exists!")
        return redirect('/')
    elif getdataforgroupform.validate_on_submit():
        # first, let's check for permissions
        allowed_to_see_data = False  # start off as False
        db = client.groups
        names = db.list_collection_names()
        group_name = getdataforgroupform.group_name.data
        if group_name not in names:
            retrieve_data = "The group: ", group_name, "doesn't exist."
        else:
            print("Group exists, moving on to the next check.")
        # Okay, so the group exists
        # Now, let's check to see if the person has the permission to add data
        group_collection = db[group_name]
        if useremail == "No user":
            retrieve_data = "You need to be logged in."
            return render_template('index.html', otherform=otherform, getdataforgroupform=getdataforgroupform, retrieve_data=retrieve_data)
        else:
            print("Useremail to check is: ", useremail)
            if useremail in group_collection.find_one()["Admin"]:
                print("You are a Admin in the group")
                allowed_to_see_data = True
            elif useremail in group_collection.find_one()["Standard"]:
                print("You are a Standard in the group")
                allowed_to_see_data = True
            else:
                retrieve_data = "You are not a part of the group."
                return render_template('index.html', otherform=otherform, getdataforgroupform=getdataforgroupform, retrieve_data=retrieve_data)

        if allowed_to_see_data:
            retrieve_data = []
            db = client.group_data
            group_collection = db[getdataforgroupform.group_name.data]
            info_list = []
            # print(group_collection)
            for item in group_collection.find():
                retrieve_data.append(item)
            # print("retrieve_data is: ", retrieve_data)
            #del retrieve_data['_id']
            return render_template('index.html', otherform=otherform, getdataforgroupform=getdataforgroupform, retrieve_data=retrieve_data)
        else:
            return render_template('index.html', otherform=otherform, getdataforgroupform=getdataforgroupform, retrieve_data=retrieve_data)
    return render_template('index.html', otherform=otherform, getdataforgroupform=getdataforgroupform)

@app.route("/profile", methods=['GET', 'POST'])
def profile():
	return render_template('profile.html')

# working with uploads
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    global useremail
    if request.method == 'POST':
        print("Let's do some checking first")
        # first, check to see if the user is even allowed to post to this group
        allowed_to_add_data = False  # start off as False
        group_name = request.form['group_insert']
        db = client.groups
        names = db.list_collection_names()
        if group_name not in names:
            print("The group: ", group_name, "doesn't exist.")
            return render_template('uploader.html')
        else:
            print("Group exists, moving on to the next check.")
        # Okay, so the group exists
        # Now, let's check to see if the person has the permission to add data
        group_collection = db[group_name]
        if useremail == "No user":
            print("The user needs to be logged in.")
            return render_template('uploader.html')
        else:
            print("Useremail to check is: ", useremail)
            if useremail in group_collection.find_one()["Admin"]:
                print("The user is a Admin in the group")
                allowed_to_add_data = True
            elif useremail in group_collection.find_one()["Standard"]:
                print("The user is a Standard in the group")
                allowed_to_add_data = True
            else:
                print("The user is not a part of the group.")
                return render_template('uploader.html')
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
        if file and allowed_file(file.filename) and allowed_to_add_data:
            print("Everything checks out, let's get the data")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # print(filename[-3:])
            db = client.group_data
            groupDataCollection = db[group_name]
            if filename[-3:] == "csv":
                processfile = read_csv_file(filename)  # type is a dictionary

                # put in database
                groupDataCollection.insert_one(processfile)
                # print(processfile)

                return redirect(url_for('index'))
            # return redirect(url_for('uploaded_file',filename=filename)) # perhaps we don't need to redirect again
    return render_template('uploader.html')

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

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
        if email in check_group['Admin']:
            result = "You are a Admin"
        elif email in check_group['Standard']:
            result = "You are a Standard"
        elif email in check_group['Admin'] and email in check_group['Standard']:
            # We don't yet have a way to prevent names from being in both, so this'll be our reminder
            result = "Somehow, you are both an Admin AND a Standard. We should probably get that fixed."
        else:
            result = "You are not registered in this group"
    else:
        result = "Group name not found"

    return result

@app.route("/google08f628c29bd0d05f.html")
def aftersignin():
    return render_template('google08f628c29bd0d05f.html')

@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html')




if __name__ == '__main__':
    app.run(debug = True)
