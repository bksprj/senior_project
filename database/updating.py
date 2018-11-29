from flask import Flask, render_template, url_for, request, flash, redirect, send_from_directory
from flask_pymongo import PyMongo
import pymongo  #document-oriented database
import urllib  # in coordination with an RFC
import json
from bson import ObjectId
from werkzeug import secure_filename
import os
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import csv

#===============================================================================
# Global variables and setup

def main():
    username = "debrsa01"
    password = "imdaBEST65"
    client = pymongo.MongoClient("mongodb://%s:%s@cluster0-shard-00-00-mhqmc.mongodb.net:27017,cluster0-shard-00-01-mhqmc.mongodb.net:27017,cluster0-shard-00-02-mhqmc.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true" % (username, password))

    db = client.test_database
    test_database = db.test_database

    group_name = "code_cleanup"
    db = client.groups
    names = db.list_collection_names()
    if group_name not in names:
        return [f"The group {group_name} does not exist"]
    query_group = db[group_name]
    data = query_group.find_one()
    prev_admin_data = data["Admin"]
    print(f"Before: {data}")
    new_admin_data = ["mightbesage@gmail.com"] + prev_admin_data
    query_group.replace_one(data, {"Admin":new_admin_data, "Standard":[]})
    data = query_group.find_one()
    print(f"Now: {data}")

if __name__ == "__main__":
    main()
