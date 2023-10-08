from flask import Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__, static_folder='static')
# app.config["MONGO_URI"] = "mongodb+srv://dlovej009:Dheeraj2006@cluster0.dnu8vna.mongodb.net/?retryWrites=true&w=majority/myDb"
url="mongodb+srv://dlovej009:Dheeraj2006@cluster0.dnu8vna.mongodb.net/?retryWrites=true&w=majority"

cluster=MongoClient(url)
db=cluster['myDb']
collection=db['users']


collection.insert_one({"datw":"132424","name":"Dheeraj"})
app.secret_key = 'smart_card'
