from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from dotenv import load_dotenv
from styleTransfer import *
from datetime import datetime
import filetype
import requests
import pymongo
import base64
import os
import io
import re
import boto3 

session = boto3.Session()
s3 = session.client("s3")

app = Flask(__name__)

model = initialize()

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
    return render_template('home.html') # render the home template

@app.route('/url', methods=["GET", "POST"])
def url():
    if(request.method == "GET"):
        return render_template("url.html")
    acceptedFormats = ["jpg", "jpeg", "png", "bmp"]
    try:
        contentImageContent = requests.get(request.form["contentImageURL"]).content
    except:
        return render_template("url.html", error="Content image url is invalid. Either save and upload the image using the upload option, or pick a different content image with a valid extension in the url.")
    try:
        styleImageContent = requests.get(request.form["styleImageURL"]).content
    except:
        return render_template("url.html", error="Style image url is invalid. Either save and upload the image using the upload option, or pick a different style image with a valid extension in the url.")
    try:
        contentExt = filetype.guess(contentImageContent).extension
    except:
        return render_template("url.html", error="Problem deciphering the filetype of content image, image may be temporarily down or has an invalid extension, use another content image.")
    try:
        styleExt = filetype.guess(styleImageContent).extension
    except:
        return render_template("url.html", error="Problem deciphering the filetype of style image, image may be temporarily down or has an invalid extension, use another style image.")
    if(contentExt not in acceptedFormats or styleExt not in acceptedFormats):
        return render_template("url.html", error="Please enter images in valid formats (.jpg, .jpeg, .png, .bmp)")
    if(request.form["style"] == ""):
        return render_template("url.html", error="Please pick a style")
    contentImageURI = "data:image/" + contentExt + ";base64," + base64.b64encode(contentImageContent).decode()
    styleImageURI = "data:image/" + styleExt + ";base64," + base64.b64encode(styleImageContent).decode()
    stylizedImageURI = url_perform_style_transfer(model, request.form["contentImageURL"], request.form["styleImageURL"])
    if(type(stylizedImageURI) == list):
        if(len(stylizedImageURI) == 2):
            return render_template("url.html", error="Was not able to retrieve content and style images due to a retrieval error. Please use other images.")
        if(len(stylizedImageURI) == 1):
            return render_template("url.html", error="Was not able to retrieve " + stylizedImageURI[0] + " image due to a retrieval error. Please use another image.")
    currentTime = str(datetime.today().timestamp())
    contentKey = 'content' + currentTime + "." + str(contentExt)
    styleKey = 'style' + currentTime + "." + str(styleExt)
    try:
        s3.put_object(Body = contentImageContent, Bucket='kgstyletransfer', Key=contentKey)
        s3.put_object(Body = styleImageContent, Bucket='kgstyletransfer', Key=styleKey)
    except:
        pass
    decodedStylizedImage = base64.b64decode(re.sub('^data:image\/[a-z]+;base64,', "", stylizedImageURI, count=1))
    stylizedKey = 'stylized' + currentTime + ".jpg"
    try:
        s3.put_object(Body = decodedStylizedImage, Bucket='kgstyletransfer', Key=stylizedKey)
    except:
        pass
    baseurl = "https://kgstyletransfer.s3.amazonaws.com/"
    contentImageS3 = baseurl + contentKey
    styleImageS3 = baseurl + styleKey
    stylizedImageS3 = baseurl + stylizedKey
    try:
        db.images.insert_one({
            'contentImageURI': contentImageS3,
            'styleImageURI': styleImageS3,
            'stylizedImageURI': stylizedImageS3,
            'style': request.form["style"]
        })
    except:
        pass
    return render_template('url.html', contentImageURI=contentImageURI, styleImageURI=styleImageURI, stylizedImageURI=stylizedImageURI)

@app.route('/upload', methods=["GET", "POST"])
def upload():
    if(request.method == "GET"):
        return render_template("upload.html")
    if(request.form["contentImageURI"] == "Content Image Error"):
        return render_template("upload.html", error="Could not parse uploaded content image")
    if(request.form["styleImageURI"] == "Style Image Error"):
        return render_template("upload.html", error="Could not parse uploaded style image")
    if(request.form["style"] == ""):
        return render_template("upload.html", error="Please choose a style")
    strippedContentImage = re.sub('^data:image\/[a-z]+;base64,', "", request.form["contentImageURI"], count=1)
    strippedStyleImage = re.sub('^data:image\/[a-z]+;base64,', "", request.form["styleImageURI"], count=1)
    decodedContentImage = base64.b64decode(strippedContentImage)
    decodedStyleImage = base64.b64decode(strippedStyleImage)
    try:
        contentExt = filetype.guess(decodedContentImage).extension
    except:
        return render_template("upload.html", error="Could not identify the type and extension of content image")
    try:
        styleExt = filetype.guess(decodedStyleImage).extension
    except:
        return render_template("upload.html", error="Could not identify the type and extension of style image")
    acceptedFormats = ["jpg", "jpeg", "png", "bmp"]
    if(contentExt not in acceptedFormats):
        return render_template("upload.html", error="Content image is of type " + contentExt + ". Content image must be of type jpg, jpeg, png, or bmp.")
    if(styleExt not in acceptedFormats):
        return render_template("upload.html", error="Style image is of type " + styleExt + ". Style image must be of type jpg, jpeg, png, or bmp.")
    currentTime = str(datetime.today().timestamp())
    contentKey = 'content' + currentTime + "." + str(contentExt)
    styleKey = 'style' + currentTime + "." + str(styleExt)
    try:
        s3.put_object(Body = decodedContentImage, Bucket='kgstyletransfer', Key=contentKey)
        s3.put_object(Body = decodedStyleImage, Bucket='kgstyletransfer', Key=styleKey)
    except:
        pass
    stylizedImageURI = uploaded_perform_style_transfer(model, decodedContentImage, decodedStyleImage)
    decodedStylizedImage = base64.b64decode(re.sub('^data:image\/[a-z]+;base64,', "", stylizedImageURI, count=1))
    stylizedKey = 'stylized' + currentTime + ".jpg"
    try:
        s3.put_object(Body = decodedStylizedImage, Bucket='kgstyletransfer', Key=stylizedKey)
    except:
        pass
    baseurl = "https://kgstyletransfer.s3.amazonaws.com/"
    contentImageS3 = baseurl + contentKey
    styleImageS3 = baseurl + styleKey
    stylizedImageS3 = baseurl + stylizedKey
    try:
        db.images.insert_one({
            'contentImageURI': contentImageS3,
            'styleImageURI': styleImageS3,
            'stylizedImageURI': stylizedImageS3,
            'style': request.form["style"]
        })
    except:
        pass
    return render_template("results.html", contentImageURI=request.form["contentImageURI"], styleImageURI=request.form["styleImageURI"], stylizedImageURI=stylizedImageURI)

if __name__ == "__main__":
   app.run()