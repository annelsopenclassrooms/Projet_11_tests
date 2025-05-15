import pytest
from server import app  # L'import reste le même si server.py est à la racine

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_show_summary_with_monkeypatch(client, monkeypatch):
    fake_clubs = [
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "13"}
    ]
    fake_competitions = [
        {"name": "Spring Festival", "date": "2025-03-27 10:00:00", "numberOfPlaces": "25"}
    ]

    monkeypatch.setattr('server.clubs', fake_clubs)
    monkeypatch.setattr('server.competitions', fake_competitions)

    response = client.post('/showSummary', data={'email': 'admin@irontemple.com'})
    assert response.status_code == 200
    assert b"admin@irontemple.com" in response.data
    assert b"Spring Festival" in response.data

def test_show_summary_invalid_email_with_monkeypatch(client, monkeypatch):
    fake_clubs = [
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "13"}
    ]

    monkeypatch.setattr('server.clubs', fake_clubs)

    response = client.post('/showSummary', data={'email': 'wrong@email.com'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Email not found" in response.data
