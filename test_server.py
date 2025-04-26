import pytest
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_show_summary_valid_email(client):
    response = client.post('/showSummary', data={'email': 'admin@irontemple.com'})
    assert response.status_code == 200
    assert b"Welcome" in response.data or b"Points" in response.data  # dépend du contenu de welcome.html

def test_show_summary_invalid_email(client):
    response = client.post('/showSummary', data={'email': 'fake@email.com'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Email not found" in response.data
