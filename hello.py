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

#===============================================================================
# Global variables and setup

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
membership_list = ["Not a part of any groups"]

#===============================================================================
# Class definitions
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

class CreateGroup(FlaskForm):
    class Meta:
        csrf = False
        locales = ('en_US', 'en')
    group_name = StringField('Team', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])

class GroupDeletionForm(FlaskForm):
    class Meta:
        csrf = False
        locales = ('en_US', 'en')
    group_name_delete = StringField('Team', validators=[DataRequired()])

class GetDataForGroupForm(FlaskForm):
    class Meta:
        csrf = False
        locales = ('en_US', 'en')
    group_name = StringField('Group', validators=[DataRequired()])

class AddNewMember(FlaskForm):
    class Meta:
        csrf = False
        locales = ('en_US', 'en')
    group_name = StringField('Group', validators=[DataRequired()])
    member_input = StringField("New Members", validators=[DataRequired()])


#===============================================================================
# Global functions
def read_csv_file(file):
    with open('uploads/' + file) as csvfile:
        file_reader = csv.reader(csvfile, delimiter=',')

        testDict = {}
        for row in file_reader:
            # print(row)
            testDict[row[0]] = row[1:]
        print(testDict)
        return testDict

def list_user_groups(email:str) -> list:
    membership_list = ["You are not a part of any group"]  # holds all the groups that the user is a member of
    db = client.groups
    groups = db.list_collection_names()
    checkgroup = "We'll use this variable to have a shorter if statement in the loop"
    existing_membership = False  # if false, then the user is not in any group
                                 # we revert to the default list, if so
    for group_name in groups:
        checkgroup = db[group_name].find_one()
        print("group_name", group_name, "checkgroup", checkgroup, type(checkgroup))
        if email in checkgroup["Admin"]:
            print("Admin in", group_name)
            membership_list.append("Admin in " + str(group_name))
            existing_membership = True
        elif email in checkgroup["Standard"]:
            print("Standard in", group_name)
            membership_list.append("Standard in " + str(group_name))
            existing_membership = True
        else:
            print("User not in", group_name)
    if not existing_membership:
        membership_list = ["You are not a part of any group"]
    else:
        membership_list = membership_list[1:]
    return membership_list

def create_group(new_group_name:str, admin_email:str):
    db = client.groups
    listed_group_names = db.list_collection_names()
    if new_group_name not in listed_group_names:
        # We'll want to create the group in the groups database
        # print("Let's create the group")
        new_group = db[new_group_name]
        new_group.insert_one({"Admin":[admin_email], "Standard":[]})
        # Then we'll want to create a collection for that new group's data in the group_data database
        db = client.group_data
        new_group = db[new_group_name]
        new_group.insert_one({"Group creation":"Completed"})
    else:
        print("That team already exists!")

def get_data(group_name:str):
    # first, let's check for permissions
    allowed_to_see_data = False  # start off as False
    admin = False
    db = client.groups
    names = db.list_collection_names()
    if group_name not in names:
        # retrieve_data = ["The group: " + group_name + " does not exist."]
        return [["The group: " + group_name + " does not exist."], admin]
    else:
        print("Group exists, moving on to the next check.")

    # Okay, so the group exists
    # Now, let's check to see if the person has the permission to add data
    group_collection = db[group_name]
    if useremail == "No user":
        # retrieve_data = ["You need to be logged in."]
        return [["You need to be logged in."], admin]
    else:
        # this is to determine the rank, in case different actions are allowed
        print("Useremail to check is: ", useremail)
        if useremail in group_collection.find_one()["Admin"]:
            print("You are an Admin in the group")
            allowed_to_see_data = True
            admin = True
        elif useremail in group_collection.find_one()["Standard"]:
            print("You are a Standard in the group")
            allowed_to_see_data = True
        else:
            retrieve_data = ["You are not a part of the group."]
    if allowed_to_see_data:
        retrieve_data = []
        db = client.group_data
        group_collection = db[group_name]
        info_list = []
        # print(group_collection)
        count = 0
        for item in group_collection.find():
            count += 1
            # print("Item is: ", item, type(item))
            del item["_id"]
            retrieve_data.append(item)
        if count == 0:
            retrieve_data = ["There are no data documents in this group"]
    return [retrieve_data, admin]

def delete_group(group_name_delete:str) -> list:
    db_groups = client.groups
    db_group_data = client.group_data
    db_groups_collection = db_groups[group_name_delete]
    db_group_data_collection = db_group_data[group_name_delete]

    allowed_to_see_data = False  # start off as False
    # Does the group exist?
    names = db_groups.list_collection_names()
    if group_name_delete not in names:
        server_message = ["The group: " + group_name_delete + " doesn't exist."]
        return server_message
    else:
        print("Group exists, moving on to the next check.")

    # Okay, so the group exists
    # Now, let's check to see if the person has the permission to add data
    if useremail == "No user":
        server_message = ["You need to be logged in."]
        return server_message
    else:
        print("Useremail to check is: ", useremail)
        if useremail in db_groups_collection.find_one()["Admin"]:
            print("You are an Admin in the group")
            allowed_to_see_data = True
            admin = True
        elif useremail in db_groups_collection.find_one()["Standard"]:
            print("You are a Standard in the group")
            allowed_to_see_data = True
        else:
            server_message = ["You are not a part of the group."]
            return server_message
    print("Attempting to delete")
    # drop the group
    drop1 = db_groups_collection.drop()
    drop2 = db_group_data_collection.drop()
    print("Well, let's hope it worked", drop1, drop2)
    server_message = ["Group '" + str(group_name_delete) + "' has been deleted"]
    return server_message

#===============================================================================
# Routes

# when you log in, we will get that email address here
@app.route('/getemail', methods = ['POST'])
def get_post_javascript_data():
    jsdata = request.form['myData']
    print(jsdata, "has logged in")
    global useremail
    global membership_list
    useremail = jsdata
    membership_list = list_user_groups(useremail)
    return jsdata

# index page
@app.route("/", methods=['GET', 'POST'])
def index():
    global useremail
    global membership_list
    response = ["Not allowed to see this group's data"]
    admin = False

    # forms
    create_group_form = CreateGroup()
    getdataforgroupform = GetDataForGroupForm()
    group_deletion_form = GroupDeletionForm()
    add_member_form = AddNewMember()

    # let's create a group
    if create_group_form.validate_on_submit():
        input_name = create_group_form.group_name.data
        input_email = create_group_form.email.data
        create_group(input_name, input_email)

    # let's get data from the group
    elif getdataforgroupform.validate_on_submit():
        group_name = getdataforgroupform.group_name.data
        response, admin = get_data(group_name)

    # admin group deletion
    elif group_deletion_form.validate_on_submit():
        group_name_delete = group_deletion_form.group_name_delete.data
        response = delete_group(group_name_delete)

    return render_template('index.html',membership_list=membership_list, \
        create_group_form=create_group_form, group_deletion_form=group_deletion_form, \
        getdataforgroupform=getdataforgroupform, response=response, admin=admin)

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
                print("The user is an Admin in the group")
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
            result = "You are an Admin"
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
