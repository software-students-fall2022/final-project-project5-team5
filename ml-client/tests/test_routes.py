import pytest
import json

def test_home(flask_app):
    response = flask_app.get('/')
    assert response.request.path == "/"
    assert response.status_code == 200

def test_url(flask_app):
    response = flask_app.get('/url')
    assert response.request.path == "/url"
    assert response.status_code == 200
    contentURL = 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/Golden_Gate_Bridge_from_Battery_Spencer.jpg/640px-Golden_Gate_Bridge_from_Battery_Spencer.jpg'
    styleURL = 'https://upload.wikimedia.org/wikipedia/commons/0/0a/The_Great_Wave_off_Kanagawa.jpg'
    responseData = {'contentImageURL': contentURL, 'styleImageURL': styleURL}
    response = flask_app.post('url', data=responseData)
    assert response.status_code == 200
    assert response.request.path == "/url"

def test_upload(flask_app):
    response = flask_app.get('/upload')
    assert response.request.path == "/upload"
    assert response.status_code == 200
    contentImage = "oceanbeach+-+9.jpeg"
    styleImage = "pngtree-tennis-ball-png-image_1078825.jpeg"
    responseData = {'contentImage': contentImage, 'styleImage': styleImage}
    response = flask_app.post('upload', data=responseData)
    assert response.status_code == 200
    assert response.request.path == "/upload"

