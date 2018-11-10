import pymongo  #document-oriented database
import pprint  # "pretty print", allowing us a nicer format printed
import urllib  # in coordination with an RFC



username = urllib.parse.quote_plus('debrsa01')
password = urllib.parse.quote_plus('imdaBEST65')
client = pymongo.MongoClient("mongodb://%s:%s@cluster0-shard-00-00-mhqmc.mongodb.net:27017,cluster0-shard-00-01-mhqmc.mongodb.net:27017,cluster0-shard-00-02-mhqmc.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true" % (username, password))


db = client.test_database
test_database = db.test_database

# Methods for querying
# db.collection.find()
    # you can limit the results with .limit(num) appended
data_received = test_database.find_one({"project":"senior project"})
pprint.pprint(data_received)
# print(type(data_received))  # type: dict
