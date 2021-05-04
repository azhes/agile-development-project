from flask import Flask
from app import app

def test_app_route():

    client = app.test_client()
    url = '/'

    response = client.get(url)
    assert response.status_code == 200



