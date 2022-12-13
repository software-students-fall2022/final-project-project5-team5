from flask import Flask, render_template, request, redirect, url_for, make_response
from dotenv import load_dotenv
from styleTransfer import *
import requests
import pymongo
import base64
import imghdr
import os

app = Flask(__name__)

model = initialize()

# load credentials and configuration options from .env file
# if you do not yet have a file named .env, make one based on the template in env.example
load_dotenv()  # take environment variables from .env.

# turn on debugging if in development modeflas
#if os.getenv('FLASK_ENV', 'development') == 'development':
 #   # turn on debugging, if in development
  #  app.debug = True # debug mode

cxn = pymongo.MongoClient(os.getenv('MONGO_URI'), serverSelectionTimeoutMS=5000)
try:
    # verify the connection works by pinging the database
    cxn.admin.command('ping') # The ping command is cheap and does not require auth.
    # db = cxn[os.getenv('MONGO_DBNAME')] # store a reference to the database
    db = cxn[os.getenv('MONGO_DBNAME')] # store a reference to the database
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
    return render_template('home.html') # render the hone template

@app.route('/url', methods=["GET", "POST"])
def url():
    if(request.method == "GET"):
        return render_template("url.html")
    acceptedFormats = ["jpg", "jpeg", "png", "bmp"]
    contentExt = request.form["contentImageURL"][request.form["contentImageURL"].rfind(".")+1:].lower()
    styleExt = request.form["styleImageURL"][request.form["styleImageURL"].rfind(".")+1:].lower()
    contentImageContent = requests.get(request.form["contentImageURL"]).content
    styleImageContent = requests.get(request.form["styleImageURL"]).content
    if(contentExt not in acceptedFormats or styleExt not in acceptedFormats):
        print(imghdr.what(None, contentImageContent))
        print(imghdr.what(None, styleImageContent))
        return render_template("url.html", error="Please enter images in valid formats (.jpg, .jpeg, .png, .bmp)")
    try:
        contentImageURI = "data:image/" + contentExt + ";base64," + base64.b64encode(contentImageContent).decode()
        styleImageURI = "data:image/" + styleExt + ";base64," + base64.b64encode(styleImageContent).decode()
        print(request.form["contentImageURL"])
        print(request.form["styleImageURL"])
        stylizedImageURI = url_perform_style_transfer(model, request.form["contentImageURL"], request.form["styleImageURL"])
    except:
        return render_template("url.html", error="Something went wrong during the image generation process. Images may be invalid despite a proper extension, please pick different images")
    try:
        db.images.insert_one({
            'contentImageURI': contentImageURI,
            'styleImageURI': styleImageURI,
            'stylizedImageURI': stylizedImageURI
        })
    except:
        pass
    return render_template('url.html', contentImageURI=contentImageURI, styleImageURI=styleImageURI, stylizedImageURI=stylizedImageURI)

@app.route('/upload', methods=["GET", "POST"])
def upload():
    if(request.method == "GET"):
        return render_template("upload.html")
    basepath = "./static/images/"
    contentImage = basepath + request.form["contentImage"]
    styleImage = basepath + request.form["styleImage"]
    acceptedFormats = ["jpg", "jpeg", "png", "bmp"]
    if(contentImage[contentImage.rfind(".")+1:].lower() not in acceptedFormats or styleImage[styleImage.rfind(".")+1:].lower() or imghdr.what(contentImage) not in acceptedFormats or imghdr.what(styleImage) not in acceptedFormats):
        return render_template("upload.html", error="Upload images in one of these formats (.jpg, .jpeg, .png, .bmp)")
    images = uploaded_perform_style_transfer(model, contentImage, styleImage)
    try:
        db.images.insert_one({
            'contentImageURI': images[0],
            'styleImageURI': images[1],
            'stylizedImageURI': images[2]
        })
    except:
        pass
    return render_template("upload.html", contentImageURI=images[0], styleImageURI=images[1], stylizedImageURI=images[2])
    # todo backend code