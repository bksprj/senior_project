from flask import Flask, render_template, url_for, request, flash, redirect, send_from_directory
from flask_pymongo import PyMongo
import pymongo  # document-oriented database
import urllib  # in coordination with an RFC
import json
from bson import ObjectId
from werkzeug import secure_filename
import os
import sys
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
membership_list = ["Not a part of any Teams"]
group_data = [["No groups"], ["No admin"]]
group_members = ["No members"]
check_group = "not checking a group"
admin = False

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

class FileDeletionForm(FlaskForm):
    class Meta:
        csrf = False
        locales = ('en_US', 'en')
    file_name_delete = StringField('File', validators=[DataRequired()])

class AddNewMemberForm(FlaskForm):
    class Meta:
        csrf = False
        locales = ('en_US', 'en')
    group_name = StringField('Group', validators=[DataRequired()])
    member_input = StringField("New Members", validators=[DataRequired()])


#===============================================================================
# Global functions

def delete_file(filename):
    try:
        path = UPLOAD_FOLDER + "/" +filename
        os.remove(path)
        return [f"Deleted {filename} successfully"]
    except:
        return [f"Unable to delete {filename}; perhaps it isn't stored?"]

def read_csv_file(file):
    with open('uploads/' + file, newline='') as csvfile:
        file_reader = csv.reader(csvfile, delimiter=',')

        testDict = {}
        for row in file_reader:
            # print(row)
            testDict[row[0]] = row[1:]
        print("LOOK HERE")
        print(testDict)
        return testDict

def notify(noto_type:str,name=None,file_name=None) -> str:
    # we want notifications for 2 groups of cases: regarding user and regarding files
    # noto_type can be "add" or "delete"

    # 1. When a user is added or deleted
    if name != None:
        if noto_type == "add":
            return str(name) + " was added."
        elif noto_type == "delete":
            return str(name) + " was deleted."
    # 2. When a file is added or deleted
    if file_name != None:
        if noto_type == "add":
            return "The file * " + str(file_name) + " * was added."
        elif noto_type == "delete":
            return "The file * " + str(file_name) + " * was deleted."

def list_user_groups(email:str) -> list:
    membership_list = ["You are not a part of any group"]  # holds all the groups that the user is a member of
    db = client.groups
    groups = db.list_collection_names()
    checkgroup = "We'll use this variable to have a shorter if statement in the loop"
    existing_membership = False  # if false, then the user is not in any group
                                 # we revert to the default list, if so
    for group_name in groups:
        checkgroup = db[group_name].find_one()
        # print("group_name", group_name, "checkgroup", checkgroup, type(checkgroup))
        if email in checkgroup["Admin"]:
            print(group_name)
            membership_list.append(str(group_name))
            existing_membership = True
        elif email in checkgroup["Standard"]:
            print(group_name)
            membership_list.append(str(group_name))
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
        new_group.insert_one({"Notifications":[]})
        new_group.insert_one({"Files":[]}) # names of files that belong to the group
        new_group.insert_one({"Tasks":[]})
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
            del item["_id"]
            retrieve_data.append(item)
        if count == 0:
            retrieve_data = ["There are no data documents in this group"]

        dirs = os.listdir(UPLOAD_FOLDER)
        file_list = []
        # This would print all the files and directories
        for file in dirs:
            print(file)
            file_list.append(file)
    else:
        file_list = ["Not allowed to see this group's data"]

    return [ [retrieve_data, file_list], admin ]

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

def get_members(group_name:str) -> list:
    returnval = []
    db = client.groups
    names = db.list_collection_names()
    if group_name not in names:
        return [f"The group {group_name} does not exist"]
    query_group = db[group_name]
    member_data = query_group.find_one()
    # print(member_data)
    for rank,user in member_data.items():
        if rank == "Standard" and len(user) == 0:
            returnval.append([rank,["There are no standard users"]])
        else:
            returnval.append([rank,user])
    return returnval[1:]

def add_new_members(group_name:str, member_input:str):
    global check_group
    def list_without_dups(list1:list, list2:list) -> list:
        result = list1
        for i in list2:
            if i not in list1:
                result.append(i)
        return result

    # format: Rank:email,email|Rank:email,email
    # first, get a list of each email input for each rank
    member_input = member_input.replace(" ", "")  # get rid of spaces
    separate_ranks = member_input.split("|")
    # ["rank", "email,email,email"]
    admin_rank_list = separate_ranks[0].split(":")
    if len(admin_rank_list) > 1:
        new_admin_members_list = admin_rank_list[1].split(",")
    standard_rank_list = separate_ranks[1].split(":")
    if len(standard_rank_list) > 1:
        new_standard_members_list = standard_rank_list[1].split(",")

    # The email lists requested to be added:
    # print(f"new_admin_members_list is: {new_admin_members_list}")
    # print(f"new_standard_members_list is: {new_standard_members_list}")

    # now that we have the lists of email addresses to potentially add for each
    # rank, now let's get the current member data
    db = client.groups
    names = db.list_collection_names()
    if group_name not in names:
        return [f"The group {group_name} does not exist"]
    query_group = db[group_name]
    prev_member_data = query_group.find_one()  # here's the object to update
    prev_id_data = prev_member_data["_id"]
    prev_admin = prev_member_data["Admin"]
    prev_standard = prev_member_data["Standard"]




    new_admin_members_list = list_without_dups(prev_admin, new_admin_members_list)
    aset = set(prev_admin) # previous
    amset = set(new_admin_members_list) # new
    anset = aset - amset # difference

    new_notes = []
    db = client.group_data
    for eachadmin in new_admin_members_list:
        new_notes.append(notify("add", eachadmin, None))
    # new_notes = [notify("add","testboi",None)]
    names = db.list_collection_names()
    the_group = db[group_name]
    all_docs = the_group.find()
    group_data_list = [i for i in all_docs]
    notifications = group_data_list[0]
    prev_notes = notifications["Notifications"]
    new_notes = prev_notes + new_notes
    new_notes_dict = {"_id":notifications["_id"], "Notifications":new_notes}
    print(f"Before, notifications were {prev_notes}")
    the_group.find_one_and_replace(notifications, new_notes_dict)

        # notifications = query_group.find_one()
        # for one_admin in anset:
        #     notifications.append(notification("add",one_admin,None))
            # group_note = db[check_group]["Notifications"].append(notification("add",one_admin,None))



    new_standard_members_list = list_without_dups(prev_standard, new_standard_members_list)

    # print(f"Here are the final admin members {new_admin_members_list}")
    # print(f"Here are the final standard members {new_standard_members_list}")


    new_member_info = {"_id":prev_id_data, "Admin":new_admin_members_list, "Standard":new_standard_members_list}
    # print(f"New member info is: {new_member_info}")

    print("Previous member data:",query_group.find_one())
    query_group.find_one_and_replace({"_id":prev_id_data}, new_member_info)
    print("Current member data:",query_group.find_one())

def get_team_member_file(group_name:str):
    member_file = open("uploads/members.txt", "w+")
    for member in get_members(group_name):
        member_file.write()
    return get_members(group_name + "\n")

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

# when you click on a group name this will retrieve that group name
@app.route('/grab_group/<group_name>', methods = ['POST'])
def get_post_group_name(group_name):
    # print(group_name)
    global useremail
    global membership_list
    global group_data
    global group_members
    global check_group
    global admin
    check_group = group_name
    group_data = get_data(group_name)
    group_members = get_members(group_name)
    # admin check
    db = client.groups
    group_collection = db[group_name]
    if useremail in group_collection.find_one()["Admin"]:
        # print("You are an Admin in the group")
        admin = True
    else:
        admin = False

    return "RETRIEVED GROUP NAME"

# index page
@app.route("/", methods=['GET', 'POST'])
def index():
    global useremail
    global membership_list
    global group_data
    global group_members
    global check_group
    global admin


    # get noto_lst
    if check_group != "not checking a group":
        db = client.group_data
        the_group = db[check_group]
        all_docs = the_group.find()
        group_stuff = [i for i in all_docs]
        group_notes = group_stuff[0]
        noto_lst = group_notes["Notifications"]
        if len(noto_lst) == 0:
            noto_lst = ["There are no notifications"]
        print(f" here are the notifications {noto_lst}")
    else:
        noto_lst = ["No Group Selected"]


    response = ["No files here..."]

    file_lst = os.listdir(UPLOAD_FOLDER)
    # members = ["Not looking at any teams..."]

    # forms
    create_group_form = CreateGroup()
    group_deletion_form = GroupDeletionForm()
    add_member_form = AddNewMemberForm()
    file_deletion_form = FileDeletionForm()

    # let's create a group
    if create_group_form.validate_on_submit():
        input_name = create_group_form.group_name.data
        input_email = create_group_form.email.data
        create_group(input_name, input_email)

    elif add_member_form.validate_on_submit():
        print("\n*******************************************")
        group_name = add_member_form.group_name.data
        new_members = add_member_form.member_input.data
        # print(f"\nAttempting member addition with {group_name} and members: {new_members}")
        add_new_member_return_msg = add_new_members(group_name, new_members)  # Currently, this would be None
        members = get_members(group_name)

    elif group_deletion_form.validate_on_submit():
        group_name_delete = group_deletion_form.group_name_delete.data
        response = delete_group(group_name_delete)

    elif file_deletion_form.validate_on_submit():
        file_name_delete = file_deletion_form.file_name_delete.data
        response = delete_file(file_name_delete)
    print("\nGroup data is:\n", group_data)

    dirs = os.listdir(UPLOAD_FOLDER)
    file_lst = []
    for file_name in dirs:
        file_lst.append(file_name)
    print("FILE LIST TO BE PASSED", file_lst)

    return render_template('index.html', membership_list=membership_list, \
        create_group_form=create_group_form, add_member_form=add_member_form, \
        group_deletion_form=group_deletion_form, response=response, file_lst=file_lst, \
        admin=admin, members=group_members, file_deletion_form=file_deletion_form, noto_lst=noto_lst)

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
            return render_template('/includes/uploader.html')
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
    return render_template('includes/uploader.html')

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

@app.route("/team", methods=['GET', 'POST'])
def team():
    return render_template('team.html')

if __name__ == '__main__':
    app.run(debug = True)
