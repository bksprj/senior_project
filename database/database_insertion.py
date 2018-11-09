import pymongo  #document-oriented database
import pprint  # "pretty print", allowing us a nicer format printed
import urllib
#import dnspython



username = urllib.parse.quote_plus('debrsa01')
password = urllib.parse.quote_plus('imdaBEST65')


# working with Mongo Atlas (cloud storage)
# client = pymongo.MongoClient(<Atlas connection string>)
#client = pymongo.MongoClient("mongodb://%s:%s@mycluster0-shard-00-00.mongodb.net:27017,mycluster0-shard-00-01.mongodb.net:27017,mycluster0-shard-00-02.mongodb.net:27017/admin?ssl=true&replicaSet=Mycluster0-shard-0&authSource=admin" % (username, password))
#client = Mongo::Client.new("mongodb://%s:%s@cluster0-shard-00-00-mhqmc.mongodb.net:27017,cluster0-shard-00-01-mhqmc.mongodb.net:27017,cluster0-shard-00-02-mhqmc.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true" % (username, password))


client = pymongo.MongoClient("mongodb://%s:%s@cluster0-shard-00-00-mhqmc.mongodb.net:27017,cluster0-shard-00-01-mhqmc.mongodb.net:27017,cluster0-shard-00-02-mhqmc.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true" % (username, password))
#client = pymongo.MongoClient("mongodb+srv://%s:%s@cluster0-mhqmc.mongodb.net/test?retryWrites=true" % (username, password))


# "mongodb://%s:%s@mycluster0-shard-00-00.mongodb.net:27017,mycluster0-shard-00-01.mongodb.net:27017,mycluster0-shard-00-02.mongodb.net:27017/admin?ssl=true&replicaSet=Mycluster0-shard-0&authSource=admin" % (username, password)


# local db
# client = MongoClient('localhost', 27017) # default host and port

db = client.test_database
# or db = client['test_database']


# A collection is a group of documents stored in MongoDB,
# and can be thought of as roughly the equivalent of a
# table in a relational database.

collection = db.test_collection
# or collection = db['test_collection']


# IMPORTANT: Collections (and databases) are created lazily!
# They are created once the first document is inserted

'''
Objects
MongoDB works with JSON Objects
'''
test_data = {"message":"hello world", "project":"senior project"}


'''
Insertion
To insert a document into a collection we can use the insert_one() method
'''

test_database = db.test_database

test_data_id = test_database.insert_one(test_data).inserted_id
# print(test_data_id)


# To verify the creation of the collection, we can use
# we'll wait on this


'''
Retrieving
The most basic type of query that can be performed in MongoDB is find_one().
This method returns a single document matching a query (or None if there are
no matches). It is useful when you know there is only one matching document,
or are only interested in the first match.
'''

pprint.pprint(test_database.find_one({"message":"hello world"}))
