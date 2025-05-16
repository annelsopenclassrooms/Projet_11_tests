from server import app
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_redeem_more_than_points(monkeypatch, client):
    test_club = {'name': 'Test Club', 'email': 'test@club.com', 'points': '2'}
    test_competition = {'name': 'Test Comp', 'date': '2025-12-01 10:00:00', 'numberOfPlaces': '10'}

    monkeypatch.setattr('server.clubs', [test_club])
    monkeypatch.setattr('server.competitions', [test_competition])

    response = client.post('/purchasePlaces', data={
        'club': 'Test Club',
        'competition': 'Test Comp',
        'places': '5'
    })

    assert b"You cannot redeem more points than you have." in response.data

def test_redeem_more_than_available_places(monkeypatch, client):
    test_club = {'name': 'Test Club', 'email': 'test@club.com', 'points': '20'}
    test_competition = {'name': 'Test Comp', 'date': '2025-12-01 10:00:00', 'numberOfPlaces': '3'}

    monkeypatch.setattr('server.clubs', [test_club])
    monkeypatch.setattr('server.competitions', [test_competition])

    response = client.post('/purchasePlaces', data={
        'club': 'Test Club',
        'competition': 'Test Comp',
        'places': '5'
    })

    assert b"Not enough places left in this competition." in response.data

def test_successful_booking(monkeypatch, client):
    test_club = {'name': 'Test Club', 'email': 'test@club.com', 'points': '10'}
    test_competition = {'name': 'Test Comp', 'date': '2025-12-01 10:00:00', 'numberOfPlaces': '10'}

    monkeypatch.setattr('server.clubs', [test_club])
    monkeypatch.setattr('server.competitions', [test_competition])

    response = client.post('/purchasePlaces', data={
        'club': 'Test Club',
        'competition': 'Test Comp',
        'places': '5'
    })

    assert b"Great - booking complete!" in response.data
    assert test_competition['numberOfPlaces'] == 5  # Mise à jour bien faite
import pytest
from server import app  # L'import reste le même si server.py est à la racine



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
