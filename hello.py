from flask import Flask, render_template, url_for
from flask_pymongo import PyMongo
import pymongo  #document-oriented database
# import urllib  # in coordination with an RFC
import json
from bson import ObjectId


app = Flask(__name__, static_url_path='/static')

username = "debrsa01"
password = "imdaBEST65"
client = pymongo.MongoClient("mongodb://%s:%s@cluster0-shard-00-00-mhqmc.mongodb.net:27017,cluster0-shard-00-01-mhqmc.mongodb.net:27017,cluster0-shard-00-02-mhqmc.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true" % (username, password))

db = client.test_database
test_database = db.test_database

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@app.route("/", methods=['GET', 'POST'])
def index():
    result_dict = test_database.find_one({"project":"senior project"})
    return render_template('index.html', result=result_dict)

@app.route("/google08f628c29bd0d05f.html")
def aftersignin():
    return render_template('google08f628c29bd0d05f.html')

@app.route("/about.html", methods=['GET', 'POST'])
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug = True)