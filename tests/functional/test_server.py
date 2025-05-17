from datetime import datetime, timedelta
import pytest
from server import app
import server

import pytest
from flask import Flask
from server import app as flask_app

@pytest.fixture(autouse=True)
def clear_reservations():
    server.reservations.clear()

# Données de test (utilisées avec monkeypatch)
test_club = {'name': 'Test Club', 'email': 'test@club.com', 'points': '30'}
test_competition = {'name': 'Test Competition', 'date': '2025-10-10 10:00:00', 'numberOfPlaces': '25'}
# Données de test
test_club = {'name': 'Test Club', 'email': 'test@club.com', 'points': '30'}
past_competition = {
    'name': 'Past Competition',
    'date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
    'numberOfPlaces': '10'
}

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
    assert b"Great - booking complete!" in response.data

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

@pytest.fixture
def past_test_data(monkeypatch):
    monkeypatch.setattr('server.clubs', [test_club.copy()])
    monkeypatch.setattr('server.competitions', [past_competition.copy()])

def test_cannot_book_past_competition(client, past_test_data):
    response = client.get(f"/book/{past_competition['name']}/{test_club['name']}", follow_redirects=True)

    assert response.status_code == 200
    assert b"This competition has already taken place" in response.data

def test_cannot_purchase_places_for_past_competition(client, past_test_data):
    response = client.post('/purchasePlaces', data={
        'club': 'Test Club',
        'competition': 'Past Competition',
        'places': '2'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Cannot book places for a past competition." in response.data

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_purchase_places_deducts_points(client, monkeypatch):
    test_clubs = [{'name': 'Test Club', 'email': 'test@club.com', 'points': '10'}]
    test_competitions = [{'name': 'Test Competition', 'date': '2025-12-12 10:00:00', 'numberOfPlaces': '20'}]

    monkeypatch.setattr('server.clubs', test_clubs)
    monkeypatch.setattr('server.competitions', test_competitions)

    response = client.post('/purchasePlaces', data={
        'competition': 'Test Competition',
        'club': 'Test Club',
        'places': '3'
    })

    assert response.status_code == 200
    assert int(test_clubs[0]['points']) == 7  # 10 - 3
    assert int(test_competitions[0]['numberOfPlaces']) == 17  # 20 - 3


@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client
        


def test_points_board_displays_clubs_and_points(client, monkeypatch):
    test_clubs = [
        {'name': 'Test Club A', 'email': 'a@test.com', 'points': '15'},
        {'name': 'Test Club B', 'email': 'b@test.com', 'points': '30'}
    ]

    monkeypatch.setattr('server.clubs', test_clubs)

    response = client.get('/points-board')
    html = response.data.decode()

    assert response.status_code == 200
    assert 'Test Club A' in html
    assert '15' in html
    assert 'Test Club B' in html
    assert '30' in html

