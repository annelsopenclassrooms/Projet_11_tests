from datetime import datetime, timedelta
import pytest
from server import app


# Test data
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
