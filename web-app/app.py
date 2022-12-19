from flask import Flask, render_template, request, redirect, url_for, make_response
from dotenv import load_dotenv
import pymongo
import os
from bson import ObjectId

app = Flask(__name__)

# load credentials and configuration options from .env file
# if you do not yet have a file named .env, make one based on the template in env.example
load_dotenv()  # take environment variables from .env.

cxn = pymongo.MongoClient("mongodb+srv://kevin:gong@cluster0.bhbmpmp.mongodb.net/?retryWrites=true&w=majority", serverSelectionTimeoutMS=5000)

try:
    # verify the connection works by pinging the database
    cxn.admin.command('ping') # The ping command is cheap and does not require auth.
    # db = cxn[os.getenv('MONGO_DBNAME')] # store a reference to the database
    db = cxn["styleTransfer"] # store a reference to the database
    print(' *', 'Connected to MongoDB!') # if we get here, the connection worked!
except Exception as e:
    # the ping command failed, so the connection is not available.
    print('', "Failed to connect to MongoDB at", os.getenv('MONGO_URI'))
    print('Database connection error:', e) # debug'

# route for the home page
@app.route('/')
def home():
    """
    Route for the home page
    """
    try:
        if(db.images.count_documents({}) == 0):
            return render_template('index.html', message="No images in database")
        return render_template('index.html', images=db.images.find({}).limit(5))
    except:
        pass
    return render_template('index.html', message="No images retrieved, failure to perform find method on database") # render the home template

@app.route('/category/<id>')
def category(id):
    """
    Route for the home page
    """
    try:
        print(id)
        if(id==""):
            return home()
        if(db.images.count_documents({'style': id}) == 0):
            return render_template('categorized.html', message="No images in database",category=id)
        return render_template('categorized.html', images=db.images.find({'style': id}),category=id)
    except:
        pass
    return render_template('index.html', message="No images retrieved, failure to perform find method on database") # render the home template

@app.route('/delete/<id>',methods=['GET', 'POST'])
def delete(id):
    print("deleting "+ id)
    try:
        
        db.images.delete_one({
           "_id": ObjectId(id)
        })
        return home(), 200
    except:
        return "Error", 404
    

