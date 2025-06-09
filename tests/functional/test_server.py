import pytest
from server import app as flask_app


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
