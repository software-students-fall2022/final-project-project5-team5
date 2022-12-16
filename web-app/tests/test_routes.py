import pytest
import json

def test_home(flask_app):
    response = flask_app.get('/')
    assert response.request.path == "/"
    assert response.status_code == 200

def test_category(flask_app):
    response = flask_app.get('/category/')
    assert response.request.path == "/category/"
    assert response.status_code == 200

def test_search(flask_app):
    response = flask_app.get('/search')
    assert response.request.path == "/search"
    assert response.status_code == 200

def test_delete(flask_app):
    response = flask_app.get('/delete')
    assert response.request.path == "/delete"
    assert response.status_code == 200