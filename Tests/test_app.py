import pytest
from flask import Flask
from app import app, expense


@pytest.fixture
def client():
    return app.test_client()


def test_home_route(client):
    """ 
    Tests for the home route
    """
    req = client.get('/')

    # Checks if correct html page has loaded
    assert b'Balance' in req.data
    assert b'Budget' in req.data
    assert b'Expenses' in req.data
    assert b'Analysis' in req.data

    # Checks that route loads with no errors
    assert req.status_code == 200

def test_update_route(client):
    """ 
    Tests for the update route
    """
    req = client.get("/update/1?ID=UPDATE")

    assert req.status_code == 200


