from flask import *
import json


app = Flask(__name__)

@app.route('/')
def index():
   #return render_template("hello.html")
   return render_template("index.html")

@app.route('/hello')
def hello():
    return render_template("hello.html")

if __name__ == '__main__':
   app.run(debug = True)
