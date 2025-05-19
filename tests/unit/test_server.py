import pytest
from datetime import datetime, timedelta
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

# 1. Recherche d'un club par email
def find_club_by_email(clubs, email):
    return next((club for club in clubs if club['email'] == email), None)

def test_find_club_by_email_found():
    clubs = [{'email': 'test@example.com'}, {'email': 'other@example.com'}]
    result = find_club_by_email(clubs, 'test@example.com')
    assert result == {'email': 'test@example.com'}

def test_find_club_by_email_not_found():
    clubs = [{'email': 'test@example.com'}]
    result = find_club_by_email(clubs, 'nope@example.com')
    assert result is None

# 2. Recherche d'un club ou compétition par nom
def find_by_name(items, name):
    return next((item for item in items if item['name'] == name), None)

def test_find_by_name_found():
    data = [{'name': 'Club A'}, {'name': 'Club B'}]
    assert find_by_name(data, 'Club B') == {'name': 'Club B'}

def test_find_by_name_not_found():
    assert find_by_name([{'name': 'X'}], 'Y') is None

# 3. Vérification si une date est passée
def is_past(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    return date < datetime.now()

def test_is_past_true():
    old_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    assert is_past(old_date) is True

def test_is_past_false():
    future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    assert is_past(future_date) is False

# 4. Logique d’achat : validation
def validate_purchase(club, competition, requested_places, already_booked):
    errors = []

    if requested_places <= 0:
        errors.append("Invalid number of places.")
    if already_booked + requested_places > 12:
        errors.append("You cannot book more than 12 places in total.")
    if requested_places > int(competition['numberOfPlaces']):
        errors.append("Not enough places left in this competition.")
    if requested_places > int(club['points']):
        errors.append("You cannot redeem more points than you have.")

    return errors

def test_validate_purchase_success():
    club = {'points': 10}
    competition = {'numberOfPlaces': '10'}
    errors = validate_purchase(club, competition, 5, 3)
    assert errors == []

def test_validate_purchase_too_many_total():
    club = {'points': 20}
    competition = {'numberOfPlaces': '20'}
    errors = validate_purchase(club, competition, 10, 5)
    assert "You cannot book more than 12 places in total." in errors

def test_validate_purchase_not_enough_places():
    club = {'points': 10}
    competition = {'numberOfPlaces': '3'}
    errors = validate_purchase(club, competition, 5, 0)
    assert "Not enough places left in this competition." in errors

def test_validate_purchase_not_enough_points():
    club = {'points': 2}
    competition = {'numberOfPlaces': '10'}
    errors = validate_purchase(club, competition, 5, 0)
    assert "You cannot redeem more points than you have." in errors

def test_validate_purchase_invalid_number():
    club = {'points': 10}
    competition = {'numberOfPlaces': '10'}
    errors = validate_purchase(club, competition, 0, 0)
    assert "Invalid number of places." in errors
