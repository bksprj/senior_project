import pymongo  # document-oriented database
import pprint  # "pretty print", allowing us a nicer format printed
import urllib
# import dnspython


username = urllib.parse.quote_plus('debrsa01')
password = urllib.parse.quote_plus('imdaBEST65')
client = pymongo.MongoClient("mongodb://%s:%s@cluster0-shard-00-00-mhqmc.mongodb.net:27017,cluster0-shard-00-01-mhqmc.mongodb.net:27017,cluster0-shard-00-02-mhqmc.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true" % (username, password))
db = client.groups

group_name = input("Enter in the name for your group to create")

names = db.list_collection_names()
if group_name not in names:
    print("We'll have to create the group")
    new_group = db[group_name]
    new_group.insert_one({"Group creation":"Completed"})
else:
    print("That group already exists!")

# group_try = db[group_name]  # this will create a database, given this name!
# if group_try:
#     print("it exists yay")
# else:
#     print("we'll have to create the group")
#
# group_try.insert_one({"Database creation":"True"})
