import pytest
import json

def test_home(flask_app):
    response = flask_app.get('/')
    assert response.request.path == "/"
    assert response.status_code == 200
    assert response.status == "200 OK"
    assert response.mimetype == "text/html"
    assert response.content_type == "text/html; charset=utf-8"

def test_category(flask_app):
    response = flask_app.get('/category/<id>')
    assert response.request.path == "/category/<id>"
    assert response.status_code == 200
    assert response.status == "200 OK"
    assert response.mimetype == "text/html"
    assert response.content_type == "text/html; charset=utf-8"

def test_delete(flask_app):
    response = flask_app.get('/delete/something')
    assert response.request.path == "/delete/something"
    assert response.status_code == 404
    assert response.status == "404 NOT FOUND"
    assert response.mimetype == "text/html"
    assert response.content_type == "text/html; charset=utf-8"