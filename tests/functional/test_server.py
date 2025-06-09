
import pytest
from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
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