# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
import pymongo

# Define the WSGI application object
app = Flask(__name__)


# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers

try:
    conn=pymongo.MongoClient()
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
   print "Could not connect to MongoDB: %s" % e

db = conn.test


restaurantes =db.restaurants



post =restaurantes.find()[:2]
for d in post:
    print d
# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module

# Register blueprint(s)
app.register_blueprint(auth_module)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
