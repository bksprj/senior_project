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




app = Flask(__name__, static_url_path='/static')

username = "debrsa01"
password = "imdaBEST65"
client = pymongo.MongoClient("mongodb://%s:%s@cluster0-shard-00-00-mhqmc.mongodb.net:27017,cluster0-shard-00-01-mhqmc.mongodb.net:27017,cluster0-shard-00-02-mhqmc.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true" % (username, password))

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

class MyOtherForm(FlaskForm):
    group = StringField('group', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])

@app.route('/', methods=('GET', 'POST'))
def submit():
    form = MyForm(csrf_enabled=False)
    otherform = MyOtherForm(csrf_enabled=False)
    if form.validate_on_submit():
        return redirect('/success')
    if otherform.validate_on_submit():
        return redirect('/othersuccess')
    return render_template('index.html', form=form, otherform=otherform)

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/othersuccess')
def othersuccess():
    return render_template('othersuccess.html')



if __name__ == '__main__':
    app.run(debug = True)
