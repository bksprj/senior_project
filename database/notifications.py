import pymongo  # document-oriented database
import pprint  # "pretty print", allowing us a nicer format printed
import urllib
# import dnspython


username = urllib.parse.quote_plus('debrsa01')
password = urllib.parse.quote_plus('imdaBEST65')
client = pymongo.MongoClient("mongodb://%s:%s@cluster0-shard-00-00-mhqmc.mongodb.net:27017,cluster0-shard-00-01-mhqmc.mongodb.net:27017,cluster0-shard-00-02-mhqmc.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true" % (username, password))


db = client.group_data
new_notes = ["Why do owls haunt me?"]
names = db.list_collection_names()
the_group = db["test_noto"]
all_docs = the_group.find()
group_data_list = [i for i in all_docs]
notifications = group_data_list[0]
prev_notes = notifications["Notifications"]
new_notes = prev_notes + new_notes
new_notes_dict = {"_id":notifications["_id"], "Notifications":new_notes}
print(f"Before, notifications were {prev_notes}")
the_group.find_one_and_replace(notifications, new_notes_dict)

all_docs = the_group.find()
new_group_data_list = [i for i in all_docs]
new_notifications = new_group_data_list[0]
print(f"Now, notifications are {new_notifications}")
