import pytest
from server import app
import server

@pytest.fixture(autouse=True)
def clear_reservations():
    server.reservations.clear()

# Données de test (utilisées avec monkeypatch)
test_club = {'name': 'Test Club', 'email': 'test@club.com', 'points': '30'}
test_competition = {'name': 'Test Competition', 'date': '2025-10-10 10:00:00', 'numberOfPlaces': '25'}

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def test_data(monkeypatch):
    # On injecte les données test dans server.clubs et server.competitions
    monkeypatch.setattr('server.clubs', [test_club.copy()])
    monkeypatch.setattr('server.competitions', [test_competition.copy()])

def test_purchase_valid_places(client, test_data):
    response = client.post('/purchasePlaces', data={
        'club': 'Test Club',
        'competition': 'Test Competition',
        'places': '5'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data

def test_purchase_over_limit(client, test_data):
    response = client.post('/purchasePlaces', data={
        'club': 'Test Club',
        'competition': 'Test Competition',
        'places': '13'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"You cannot book more than 12 places" in response.data

def test_purchase_accumulated_limit(client, test_data):
    # Premier achat : 10 places
    client.post('/purchasePlaces', data={
        'club': 'Test Club',
        'competition': 'Test Competition',
        'places': '10'
    }, follow_redirects=True)

    # Deuxième tentative : 3 places (total = 13)
    response = client.post('/purchasePlaces', data={
        'club': 'Test Club',
        'competition': 'Test Competition',
        'places': '3'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"You cannot book more than 12 places in total for this competition." in response.data

