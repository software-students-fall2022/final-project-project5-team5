import pytest
import json

def test_home(flask_app):
    response = flask_app.get('/')
    assert response.request.path == "/"
    assert response.status_code == 200

