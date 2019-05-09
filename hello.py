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

# Data we'll work with for what's showing on the page
useremail = "No user"
membership_list = ["Not a part of any Teams"]
group_data = [["No groups"], ["No admin"]]
group_members = ["No members"]
check_group = "not checking a group"
admin = False

#===============================================================================
# Class definitions


class AddNewMemberForm(FlaskForm):
    class Meta:
        csrf = False
        locales = ('en_US', 'en')
    # group_name = StringField('Group', validators=[DataRequired()])
    member_input = StringField("New Members", validators=[DataRequired()])

class RemoveMemberForm(FlaskForm):
    class Meta:
        csrf = False
        locales = ('en_US', 'en')
    # group_name = StringField('Group', validators=[DataRequired()])
    member_input_del = StringField("Remove Members", validators=[DataRequired()])

class AddTaskForm(FlaskForm):
    class Meta:
        csrf = False
        locales = ('en_US', 'en')
    new_task = StringField('task', validators=[DataRequired()])

class CreateGroup(FlaskForm):
    class Meta:
        csrf = False
        locales = ('en_US', 'en')
    group_name = StringField('Team', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])

class FileDeletionForm(FlaskForm):
    class Meta:
        csrf = False
        locales = ('en_US', 'en')
    file_name_delete = StringField('File', validators=[DataRequired()])

class GroupDeletionForm(FlaskForm):
    class Meta:
        csrf = False
        locales = ('en_US', 'en')
    group_name_delete = StringField('Team', validators=[DataRequired()])

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

#===============================================================================
# Global functions
def remove_members(group_name:str, member_input:str):
    def list_without_dups(list1:list, list2:list) -> list:
        result = list1
        for i in list2:
            if i in list1:
                result.remove(i)
        return result

    def get_new_member_list(input_string):
        # expects Rank:email or Rank:email,email
        input_string = input_string.replace(" ", "")  # get rid of spaces
        if input_string.count(",") >= input_string.count("@"):
            # The point of this is to prevent random commas messing up processing
            print("Issue: count(',') >= count('@')")
            return ["Issue with extra commas"]
        if "," in input_string:
            new_members = input_string.split(":")[1].split(",")
        else:
            new_members = list(input_string.split(":")) + [""]
            new_members = new_members[1:]
            print(f"what's going on? {new_members}")
        return new_members

    db = client.groups
    names = db.list_collection_names()
    if group_name not in names:
        return [f"The group {group_name} does not exist"]


    new_admin_members = []
    new_standard_members = []

    if "Admin:" in member_input and "Standard:" not in member_input:
        # then we have Admin:email or Admin:email,email
        new_admin_members = get_new_member_list(member_input)
    elif "Admin:" not in member_input and "Standard:" in member_input:
        # then we have Standard:email
        new_standard_members = get_new_member_list(member_input)
    else:
        # Admin:email|Standard:email
        if "|" not in member_input:
            return ["'|' separator missing"]
        new_admin_members = get_new_member_list(member_input.split("|")[0])
        new_standard_members = get_new_member_list(member_input.split("|")[1])
    # Issues?
    if new_standard_members == ["Issue with extra commas"] or new_admin_members == ["Issue with extra commas"]:
        return ["Issue with extra commas"]

    # now that we have the lists of email addresses to potentially remove for each
    # rank, now let's get the current member data

    query_group = db[group_name]
    prev_member_data = query_group.find_one()  # here's the object to update
    prev_id_data = prev_member_data["_id"]
    prev_admin = prev_member_data["Admin"]
    prev_standard = prev_member_data["Standard"]

    new_admin_members_list = list_without_dups(prev_admin, new_admin_members)
    new_standard_members_list = list_without_dups(prev_standard, new_standard_members)

    # notes

    new_notes = []
    db = client.group_data
    for eachadmin in new_admin_members_list:
        new_notes.append(notify("delete", eachadmin, None))
    for eachstandard in new_standard_members_list:
        new_notes.append(notify("delete", eachstandard, None))
    # new_notes = [notify("add","testboi",None)]
    names = db.list_collection_names()
    the_group = db[group_name]
    all_docs = the_group.find()
    group_data_list = [i for i in all_docs]
    notifications = group_data_list[0]
    prev_notes = notifications["Notifications"]

    new_notes = prev_notes + new_notes
    if len(new_notes) > 10:
        new_notes = new_notes[-10:]
    new_notes_dict = {"_id":notifications["_id"], "Notifications":new_notes}
    # print(f"Before, notifications were {prev_notes}")
    if len(new_notes) > 0:
        the_group.find_one_and_replace(notifications, new_notes_dict)

    # new_standard_members_list = list_without_dups(prev_standard, new_standard_members_list)

    # print(f"Here are the final admin members {new_admin_members_list}")
    # print(f"Here are the final standard members {new_standard_members_list}")

    new_member_info = {"_id":prev_id_data, "Admin":new_admin_members_list, "Standard":new_standard_members_list}
    # print(f"New member info is: {new_member_info}")

    # print("Previous member data:",query_group.find_one())
    query_group.find_one_and_replace({"_id":prev_id_data}, new_member_info)
    # print("Current member data:",query_group.find_one())

def add_new_members(group_name:str, member_input:str):
    def list_without_dups(list1:list, list2:list) -> list:
        result = list1
        for i in list2:
            if i not in list1:
                result.append(i)
        return result

    def get_new_member_list(input_string):
        # expects Rank:email or Rank:email,email
        input_string = input_string.replace(" ", "")  # get rid of spaces
        if input_string.count(",") >= input_string.count("@"):
            # The point of this is to prevent random commas messing up processing
            print("Issue: count(',') >= count('@')")
            return ["Issue with extra commas"]
        if "," in input_string:
            new_members = input_string.split(":")[1].split(",")
        else:
            new_members = list(input_string.split(":")) + [""]
            new_members = new_members[1:]
            # print(f"what's going on? {new_members}")
        return new_members

    db = client.groups
    names = db.list_collection_names()
    if group_name not in names:
        return [f"The group {group_name} does not exist"]


    new_admin_members = []
    new_standard_members = []

    if "Admin:" in member_input and "Standard:" not in member_input:
        # then we have Admin:email or Admin:email,email
        new_admin_members = get_new_member_list(member_input)
    elif "Admin:" not in member_input and "Standard:" in member_input:
        # then we have Standard:email
        new_standard_members = get_new_member_list(member_input)
    else:
        # Admin:email|Standard:email
        if "|" not in member_input:
            return ["'|' separator missing"]
        new_admin_members = get_new_member_list(member_input.split("|")[0])
        new_standard_members = get_new_member_list(member_input.split("|")[1])
    # Issues?
    if new_standard_members == ["Issue with extra commas"] or new_admin_members == ["Issue with extra commas"]:
        return ["Issue with extra commas"]

    # admin_rank_list = separate_ranks[0].split(":")
    # if len(admin_rank_list) > 1:
    #     new_admin_members_list = admin_rank_list[1].split(",")
    # standard_rank_list = separate_ranks[1].split(":")
    # if len(standard_rank_list) > 1:
    #     new_standard_members_list = standard_rank_list[1].split(",")


    # now that we have the lists of email addresses to potentially add for each
    # rank, now let's get the current member data

    query_group = db[group_name]
    prev_member_data = query_group.find_one()  # here's the object to update
    prev_id_data = prev_member_data["_id"]
    prev_admin = prev_member_data["Admin"]
    prev_standard = prev_member_data["Standard"]

    new_admin_members_list = list_without_dups(prev_admin, new_admin_members)
    new_standard_members_list = list_without_dups(prev_standard, new_standard_members)

    # notes

    new_notes = []
    db = client.group_data
    for eachadmin in new_admin_members_list:
        new_notes.append(notify("add", eachadmin, None))
    for eachstandard in new_standard_members_list:
        new_notes.append(notify("add", eachstandard, None))
    # new_notes = [notify("add","testboi",None)]
    names = db.list_collection_names()
    the_group = db[group_name]
    all_docs = the_group.find()
    group_data_list = [i for i in all_docs]
    notifications = group_data_list[0]
    prev_notes = notifications["Notifications"]

    new_notes = prev_notes + new_notes
    if len(new_notes) > 10:
        new_notes = new_notes[-10:]
    new_notes_dict = {"_id":notifications["_id"], "Notifications":new_notes}
    # print(f"Before, notifications were {prev_notes}")
    if len(new_notes) > 0:
        the_group.find_one_and_replace(notifications, new_notes_dict)

    # new_standard_members_list = list_without_dups(prev_standard, new_standard_members_list)

    # print(f"Here are the final admin members {new_admin_members_list}")
    # print(f"Here are the final standard members {new_standard_members_list}")

    new_member_info = {"_id":prev_id_data, "Admin":new_admin_members_list, "Standard":new_standard_members_list}
    # print(f"New member info is: {new_member_info}")

    # print("Previous member data:",query_group.find_one())
    query_group.find_one_and_replace({"_id":prev_id_data}, new_member_info)
    # print("Current member data:",query_group.find_one())

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
        return [f"The team {new_group_name} has been created"]
    else:
        print("That team already exists!")
        return ["That team already exists."]

def delete_file(filename):
    try:
        path = UPLOAD_FOLDER + "/" + filename
        os.remove(path)
        return [f"Deleted {filename} successfully"]
    except:
        return [f"Unable to delete {filename}; perhaps it isn't stored?"]

def delete_group(group_name_delete:str):
    db_groups = client.groups
    db_group_data = client.group_data
    listed_group_names = db_groups.list_collection_names()
    if group_name_delete in listed_group_names:
        db_groups_collection = db_groups[group_name_delete]
        db_group_data_collection = db_group_data[group_name_delete]
        drop1 = db_groups_collection.drop()
        drop2 = db_group_data_collection.drop()
        return [f"The group {group_name_delete} has been deleted."]
    else:
        return [f"The group {group_name_delete} does not exist."]

def get_data(group_name:str):
    # first, let's check for permissions
    allowed_to_see_data = False  # start off as False
    admin = False
    db = client.groups
    names = db.list_collection_names()
    if group_name not in names:
        # retrieve_data = ["The group: " + group_name + " does not exist."]
        return [["The group: " + group_name + " does not exist."], admin]
    # Group exists, moving on to the next check."


    # Okay, so the group exists
    # Now, let's check to see if the person has the permission to add data
    group_collection = db[group_name]
    if useremail == "No user":
        # retrieve_data = ["You need to be logged in."]
        return [["You need to be logged in."], admin]
    else:
        # this is to determine the rank, in case different actions are allowed
        # print("Useremail to check is: ", useremail)
        if useremail in group_collection.find_one()["Admin"]:
            # print("You are an Admin in the group")
            allowed_to_see_data = True
            admin = True
        elif useremail in group_collection.find_one()["Standard"]:
            # print("You are a Standard in the group")
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


        db = client.group_data
        the_group = db[group_name]
        all_docs = the_group.find()

        group_stuff = [i for i in all_docs]
        # print("Data for", group_name, " is ", group_stuff)
        file_list = []
        for i in group_stuff:
            try:
                file_list = i['Files']
                prev_files = i
                # print("printing prev_files ", prev_files)
            except:
                pass


        # dirs = os.listdir(UPLOAD_FOLDER)
        # file_list = []
        # # This would print all the files and directories
        # for file in dirs:
        #     # print(file)
        #     file_list.append(file)
    else:
        file_list = ["Not allowed to see this group's data"]

    return [ [retrieve_data, file_list], admin ]

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

def get_team_member_file(group_name:str):
    member_file = open("uploads/members.txt", "w+")
    for member in get_members(group_name):
        member_file.write()
    return get_members(group_name + "\n")

def list_user_groups(email:str) -> list:
    membership_list = ["You are not a part of any group"]  # holds all the groups that the user is a member of
    db = client.groups
    groups = db.list_collection_names()
    # checkgroup = "We'll use this variable to have a shorter if statement in the loop"
    existing_membership = False  # if false, then the user is not in any group
                                 # we revert to the default list, if so
    for group_name in groups:
        checkgroup = db[group_name].find_one()
        # print("\nHEY\ngroup_name", group_name, "checkgroup", checkgroup, type(checkgroup))
        if email in checkgroup["Admin"]:
            # print(group_name)
            membership_list.append(str(group_name))
            existing_membership = True
        elif email in checkgroup["Standard"]:
            # print(group_name)
            membership_list.append(str(group_name))
            existing_membership = True
        else:
            print("User not in", group_name)
    if not existing_membership:
        membership_list = ["You are not a part of any group"]
    else:
        membership_list = membership_list[1:]
    return membership_list

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
    # return jsdata
    user = jsdata.split("@")[0]

    print("USERNAME", user)

    return redirect(url_for('user', username=user))

@app.route('/user/<username>', methods = ['GET', 'POST'])
def user(username):
    print("IN USER ROUTE", username)
    useremail = request.form['myData']
    print(useremail, "has logged in")
    global membership_list
    membership_list = list_user_groups(useremail)
    return useremail

@app.route('/loggedin/<email>/<group_name>', methods = ['GET', 'POST'])
def loggedin(email, group_name):
    # build membership_list
    db = client.groups
    list_all_groups = db.list_collection_names()
    membership_list = [group for group in list_all_groups]

    # forms
    create_group_form = CreateGroup()
    group_deletion_form = GroupDeletionForm()
    add_member_form = AddNewMemberForm()
    remove_member_form = RemoveMemberForm()
    file_deletion_form = FileDeletionForm()
    add_task_form = AddTaskForm()


    # was there a group selected?
    if group_name == "no_group":
        members = ['No Team Selected']
    else:
        members = get_members(group_name)

    # file uploads
    if request.method == 'POST':
        # let's create a group
        if create_group_form.validate_on_submit():
            input_name = create_group_form.group_name.data
            input_email = create_group_form.email.data
            create_group(input_name, input_email)
            return redirect(url_for('index'))

        elif add_member_form.validate_on_submit():
            # print("\n*******************************************")
            # group_name = add_member_form.group_name.data
            new_members = add_member_form.member_input.data
            # print(f"\nAttempting member addition with {group_name} and members: {new_members}")
            add_new_member_return_msg = add_new_members(group_name, new_members)  # Currently, this would be None
            members = get_members(group_name)

        elif remove_member_form.validate_on_submit():
            print("\n*******************************************")
            # group_name = remove_member_form.group_name.data
            removed_members = remove_member_form.member_input_del.data
            print(f"\nAttempting member removal with {group_name} and members: {removed_members}")
            removed_member_return_msg = remove_members(group_name, removed_members)  # Currently, this would be None
            members = get_members(group_name)

        elif group_deletion_form.validate_on_submit():
            group_name_delete = group_deletion_form.group_name_delete.data
            response = delete_group(group_name_delete)
            return redirect(url_for('index'))

        elif file_deletion_form.validate_on_submit():
            file_name_delete = file_deletion_form.file_name_delete.data
            response = delete_file(file_name_delete)
            db = client.group_data
            the_group = db[group_name]
            all_docs = the_group.find()

            group_stuff = [i for i in all_docs]
            # print("Data for", group_name, " is ", group_stuff)
            files = []
            prev_files = {}
            new_files_list = []
            for i in group_stuff:
                try:
                    files = i['Files']
                    prev_files = i
                    # print("printing prev_files ", prev_files)
                except:
                    pass

            # creating a new notification
            for i in group_stuff:
                try:
                    notes = i['Notifications']
                    prev_notes = i
                    # print("printing prev_files ", prev_files)
                except:
                    pass
                new_notes_list = [n for n in notes] + [notify("delete",None,file_name_delete)]
                new_notes = {"_id":prev_notes["_id"], "Notifications":new_notes_list}
                the_group.replace_one(prev_notes,new_notes)


            if file_name_delete in files:
                new_files_list = [i for i in files]
                new_files_list.remove(file_name_delete)
                new_files = {"_id":prev_files["_id"],"Files":new_files_list}

                # print("printing new_files ", new_files)
                the_group.replace_one(prev_files,new_files)

        elif add_task_form.validate_on_submit():
            new_task_submit = add_task_form.new_task.data
            print("Received task: ", new_task_submit)
            db = client.group_data
            the_group = db[group_name]
            all_docs = the_group.find()
            group_stuff = [i for i in all_docs]
            print("group stuff", group_stuff)
            prev_tasks = {}
            print("Entering task for loop")
            if group_name != "no_group":
                for i in group_stuff:
                    try:
                        tasks = i['Tasks']
                        prev_tasks = i
                        # print("printing prev_tasks ", prev_tasks)
                    except:
                        pass
                # new_tasks_list = [i for i in tasks] + [new_task_submit]
                new_tasks_list = [i for i in tasks]
                if new_task_submit not in tasks:
                    new_tasks_list.append(new_task_submit)
                new_tasks = {"_id":prev_tasks["_id"],"Tasks":new_tasks_list}
                the_group.replace_one(prev_tasks,new_tasks)
        elif request.values != None and request.values["del_task"]:
            # print(f"request.values is {request.values}")
            print(f"request.values['del_task'] is {request.values['del_task']}")
            task_name = request.values['del_task']

            db = client.group_data
            the_group = db[group_name]
            all_docs = the_group.find()
            group_stuff = [i for i in all_docs]

            tasks = []
            prev_tasks = {}
            new_tasks_list = []
            notes = []
            for i in group_stuff:
                try:
                    tasks = i['Tasks']
                    prev_tasks = i
                    # print("printing prev_files ", prev_files)
                except:
                    pass
            # try:
            #     if task_name[-1] in tasks:
            #         print("Look it's in there!!")
            #     else:
            #         print("What the heck?!")
            #         print(f"len: {len(i)} and {len(task_name[-1])}")
            #     tasks.remove(task_name[])
            #     new_tasks_list = tasks
            # except:
            #     new_tasks_list = tasks
            for j in tasks:
                print(f"len: {str(j)} and {str(task_name)}")
                if str(j) != str(task_name):
                    # print(f"Types: {type(j)} and {type(task_name)}")
                    new_tasks_list.append(j)
            new_tasks = {"_id":prev_tasks["_id"],"Tasks":new_tasks_list}
            print("prev_tasks", prev_tasks)
            print("new_tasks", new_tasks)
            the_group.replace_one(prev_tasks,new_tasks)

        else: # we must be dealing with file uploads
            file = request.files['file']
            filename = secure_filename(file.filename)
            print("Attempting to post: " + filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # now let's save the name to the group
            db = client.group_data
            the_group = db[group_name]
            all_docs = the_group.find()

            group_stuff = [i for i in all_docs]
            # print("Data for", group_name, " is ", group_stuff)
            files = []
            prev_files = {}
            new_files_list = []
            notes = []
            for i in group_stuff:
                try:
                    files = i['Files']
                    prev_files = i
                    # print("printing prev_files ", prev_files)
                except:
                    pass
            # creating a new notification
            for i in group_stuff:
                try:
                    notes = i['Notifications']
                    prev_notes = i
                    # print("printing prev_files ", prev_files)
                except:
                    pass
                new_notes_list = [n for n in notes] + [notify("add",None,filename)]
                new_notes = {"_id":prev_notes["_id"], "Notifications":new_notes_list}
                the_group.replace_one(prev_notes,new_notes)

            if filename not in files:
                print("filename,files", filename, files)
                new_files_list = [i for i in files] + [filename]
                new_files = {"_id":prev_files["_id"],"Files":new_files_list}

                # print("printing new_files ", new_files)
                the_group.replace_one(prev_files,new_files)

                all_docs = the_group.find()
                group_stuff = [i for i in all_docs]
                print("Data for", group_name, " is ", group_stuff)
            else:
                # handle duplicate file names
                # we'll still need to test this though
                done = False
                num = 0
                new_files_list = []
                while not done:
                    # tryfile = filename + str(num)
                    tryfile = filename.split(".")[0] + str(num) + "." + filename.split(".")[1]
                    print("Trying to input: ", tryfile)
                    if tryfile not in files:
                        # files.append(tryfile)
                        new_files_list = [i for i in files] + [tryfile]
                        new_files = {"_id":prev_files["_id"],"Files":new_files_list}
                        print("new_files with dup", new_files)
                        the_group.replace_one(prev_files,new_files)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], tryfile))
                        done = True
                    else:
                        num += 1

    # Grab task data
    tasks = ["No tasks"]
    if group_name != "no_group":
        db = client.group_data
        the_group = db[group_name]
        all_docs = the_group.find()
        group_stuff = [i for i in all_docs]
        for i in group_stuff:
            try:
                tasks = i['Tasks']
            except:
                pass
        if len(tasks) == 0:
            tasks = []

    # grabbing files
    files = ["No group selected"]
    check_missing = []
    if group_name != "no_group":
        for i in group_stuff:
            try:
                files = i['Files']
                for j in files:
                    print("os.listdir: ", os.listdir("uploads"))
                    if j not in os.listdir("uploads"):
                        check_missing.append(j)
                files = set(files)-set(check_missing)
            except:
                pass
    if len(files) == 0:
        files = ["No files uploaded"]
        # print(group_name, "files are: ", files )


    # grabbing notifications
    noto_lst = ["No group selected"]
    if group_name != "no_group":
        for i in group_stuff:
            try:
                noto_lst = i['Notifications']
            except:
                pass
        if len(noto_lst) == 0:
            noto_lst = ["No notifications"]


    # admin boolean
    admin_list = members[0][1]
    admin = False
    for user in admin_list:
        if email in user:
            admin = True
    # print("admin is", admin)

    return render_template("user.html", email=email, membership_list=membership_list, \
    members=members, group_name=group_name, create_group_form=create_group_form, \
    remove_member_form=remove_member_form, add_member_form=add_member_form, \
    group_deletion_form=group_deletion_form, file_deletion_form=file_deletion_form, \
    add_task_form=add_task_form, tasks=tasks, admin=admin, files=files, noto_lst=noto_lst)


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
@app.route("/index")
@app.route("/")
def start():
    return redirect("/no_group")


@app.route("/index/<group_name>", methods=['GET', 'POST'])
@app.route("/<group_name>", methods=['GET', 'POST'])
def index(group_name):
    # email = "debrsa01@luther.edu"
    # group_name = "new_team"

    # build membership_list
    db = client.groups
    list_all_groups = db.list_collection_names()
    membership_list = [group for group in list_all_groups]

    # forms
    create_group_form = CreateGroup()
    group_deletion_form = GroupDeletionForm()
    add_member_form = AddNewMemberForm()
    remove_member_form = RemoveMemberForm()
    file_deletion_form = FileDeletionForm()
    add_task_form = AddTaskForm()


    # was there a group selected?
    if group_name == "no_group":
        members = ['No Team Selected']
    else:
        members = get_members(group_name)

    # Grab task data
    tasks = ["No tasks"]
    if group_name != "no_group":
        db = client.group_data
        the_group = db[group_name]
        all_docs = the_group.find()
        group_stuff = [i for i in all_docs]
        for i in group_stuff:
            try:
                tasks = i['Tasks']
            except:
                pass
        if len(tasks) == 0:
            tasks = []

    # grabbing files
    files = ["No group selected"]
    check_missing = []
    if group_name != "no_group":
        for i in group_stuff:
            try:
                files = i['Files']
                for j in files:
                    print("os.listdir: ", os.listdir("uploads"))
                    if j not in os.listdir("uploads"):
                        check_missing.append(j)
                files = set(files)-set(check_missing)
            except:
                pass
    if len(files) == 0:
        files = ["No files uploaded"]
        # print(group_name, "files are: ", files )


    # grabbing notifications
    noto_lst = ["No group selected"]
    if group_name != "no_group":
        for i in group_stuff:
            try:
                noto_lst = i['Notifications']
            except:
                pass
        if len(noto_lst) == 0:
            noto_lst = ["No notifications"]

    return render_template("redirect_index.html", membership_list=membership_list, \
    members=members, group_name=group_name, tasks=tasks, files=files, noto_lst=noto_lst)

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
    print("Yes hello i see you're trying to upload something right?")
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
