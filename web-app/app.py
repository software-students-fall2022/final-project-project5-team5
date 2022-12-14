from flask import Flask, render_template, request, redirect, url_for, make_response
from dotenv import load_dotenv
import pymongo
import os

app = Flask(__name__)

def is_docker():
    path = '/proc/self/cgroup'
    return (
        os.path.exists('/.dockerenv') or
        os.path.isfile(path) and any('docker' in line for line in open(path))
    )

if(is_docker()):
    client = pymongo.MongoClient("db", 27017)
else:
    client = pymongo.MongoClient("127.0.0.1", 27017)

db=client["Team5"]

# route for the home page
@app.route('/')
def home():
    """
    Route for the home page
    """
    try:
        if(db.images.count_documents({}) == 0):
            return render_template('index.html', message="No images in database")
        return render_template('index.html', images=db.images.find({}))
    except:
        pass
    return render_template('index.html', message="No images retrieved, failure to perform find method on database") # render the home template