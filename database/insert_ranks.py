import pymongo  #document-oriented database
import pprint  # "pretty print", allowing us a nicer format printed
import urllib
#import dnspython



username = urllib.parse.quote_plus('debrsa01')
password = urllib.parse.quote_plus('imdaBEST65')
client = pymongo.MongoClient("mongodb://%s:%s@cluster0-shard-00-00-mhqmc.mongodb.net:27017,cluster0-shard-00-01-mhqmc.mongodb.net:27017,cluster0-shard-00-02-mhqmc.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true" % (username, password))
db = client.groups
senior_project_group = db.senior_project_group
print("hello here's the type hopefully: ", type(senior_project_group))

# test_database = db.test_database
if not senior_project_group.find_one({"Admin":["debrsa01@luther.edu"]}):
    # if there does not exist this item in the database, then we'll insert it
    # will need to update this to approprately add groups.
    # this has been added for now to check if users are within a group
    print("inserting senior_project_group")
    Senior_Project_Group = {"Admin":["debrsa01@luther.edu"], "Standard":["ramibr01@luther.edu","husoke01@luther.edu"]}
    Senior_Project_Group_id = senior_project_group.insert_one(Senior_Project_Group).inserted_id



# let's add a second group and see how it goes
db = client.groups  # redundant, I know, but efficiency comes second to clarity!
overseer = db.overseer
if not overseer.find_one({"Admin":["yasiro01@luther.edu"]}):
    print("inserting overseer")
    Overseer = {"Admin":["yasiro01@luther.edu"], "Standard":["ramibr01@luther.edu","husoke01@luther.edu","debrsa01@luther.edu"]}
    Overseer = overseer.insert_one(Overseer).inserted_id

pprint.pprint(senior_project_group.find_one({"Admin":["debrsa01@luther.edu"]}))










# this comment is just to have extra space at the bottom
