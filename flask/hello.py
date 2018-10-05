from flask import Flask, jsonify, render_template
from flask_pymongo import PyMongo
import pymongo  #document-oriented database
import pprint  # "pretty print", allowing us a nicer format printed
import urllib  # in coordination with an RFC
import json
from bson import ObjectId


app = Flask(__name__)

username = "debrsa01"
password = "imdaBEST65"
client = pymongo.MongoClient("mongodb://%s:%s@cluster0-shard-00-00-mhqmc.mongodb.net:27017,cluster0-shard-00-01-mhqmc.mongodb.net:27017,cluster0-shard-00-02-mhqmc.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true" % (username, password))


db = client.test_database
test_database = db.test_database
pprint.pprint(test_database.find_one({"project":"senior project"}))

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@app.route("/")
def dbret():
    hello_world_dict = test_database.find_one({"project":"senior project"})
    hello_world_encoded = JSONEncoder().encode(hello_world_dict)
    return hello_world_encoded

@app.route("/index")
def index():
    result_dict = test_database.find_one({"project":"senior project"})
    result_encoded = JSONEncoder().encode(result_dict)
    return render_template('index.html', result=result_encoded)

if __name__ == '__main__':
    app.run(debug = True)