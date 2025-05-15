import pytest
from flask import Flask
from server import app as flask_app  # Assurez-vous que le fichier s'appelle `server.py`

def test_points_board_route(client):
    response = client.get('/points-board')
    assert response.status_code == 200
    assert b"Club Points Board" in response.data