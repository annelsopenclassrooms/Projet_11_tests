import pytest

from server import app as flask_app  # Assurez-vous que le fichier s'appelle `server.py`

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client
        
def test_points_board_route(client):
    response = client.get('/points-board')
    assert response.status_code == 200
    assert b"Club Points Board" in response.data