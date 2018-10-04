from flask import Flask, jsonify
from flask_pymongo import PyMongo
import pymongo  #document-oriented database
import pprint  # "pretty print", allowing us a nicer format printed
import urllib  # in coordination with an RFC
import json

app = Flask(__name__)

username = "debrsa01"
password = "imdaBEST65"
client = pymongo.MongoClient("mongodb://%s:%s@cluster0-shard-00-00-mhqmc.mongodb.net:27017,cluster0-shard-00-01-mhqmc.mongodb.net:27017,cluster0-shard-00-02-mhqmc.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true" % (username, password))


db = client.test_database
test_database = db.test_database
pprint.pprint(test_database.find_one({"project":"senior project"}))

@app.route("/")
def dbret():
    hello_world = test_database.find_one({"project":"senior project"})
    # jsonify(hello_world)

    # test_obj = {"test": 69}
    # whatever = json.loads(test_obj)
    # print(type(whatever))
    
    return json.dumps(hello_world)



# username = urllib.parse.quote_plus('debrsa01')
# password = urllib.parse.quote_plus('imdaBEST65')

if __name__ == '__main__':
    app.run(debug = True)
