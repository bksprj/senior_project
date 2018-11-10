import pymongo  # document-oriented database
import pprint  # "pretty print", allowing us a nicer format printed
import urllib
# import dnspython


username = urllib.parse.quote_plus('debrsa01')
password = urllib.parse.quote_plus('imdaBEST65')
client = pymongo.MongoClient("mongodb://%s:%s@cluster0-shard-00-00-mhqmc.mongodb.net:27017,cluster0-shard-00-01-mhqmc.mongodb.net:27017,cluster0-shard-00-02-mhqmc.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true" % (username, password))
db = client.groups

group_dict = {}
print(group_dict)
print("All right, let's make a group!")

group_name = input("Enter in the name for your group")
try:
    # try a find for the collection

if group_name not in group_dict and not db.:
    print("Oh please work")
    new_collection = pymongo.collection.Collection(db,group_name,create=True)
    db.new_collection.insert_one({"Collection created":"True"})
    group_dict[group_name] = new_collection
    print("inserted new group")



# aniministry = db.aniministry
# print("hello here's the type hopefully: ", type(aniministry))

# # test_database = db.test_database
# if not aniministry.find_one({"Senpai":["debrsa01@luther.edu"]}):
#     # if there does not exist this item in the database, then we'll insert it
#     # will need to update this to approprately add groups.
#     # this has been added for now to check if users are within a group
#     print("inserting AniMinistry")
#     AniMinistry = {"Senpai":["debrsa01@luther.edu"], "Kouhai":["ramibr01@luther.edu","husoke01@luther.edu"]}
#     AniMinistry_id = aniministry.insert_one(AniMinistry).inserted_id
#
#
#
# # let's add a second group and see how it goes
# db = client.groups  # redundant, I know, but efficiency comes second to clarity!
# bigbrother = db.bigbrother
# if not bigbrother.find_one({"Senpai":["yasiro01@luther.edu"]}):
#     print("inserting BigBrother")
#     BigBrother = {"Senpai":["yasiro01@luther.edu"], "Kouhai":[]}
#     BigBrother_id = bigbrother.insert_one(BigBrother).inserted_id

# pprint.pprint(aniministry.find_one({"Senpai":["debrsa01@luther.edu"]}))










# this comment is just to have extra space at the bottom
