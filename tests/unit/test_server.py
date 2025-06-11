import json
from io import StringIO
import pytest
from server import loadClubs, loadCompetitions


def test_loadClubs(monkeypatch):
    # Mock le contenu du fichier clubs.json
    mock_clubs = {
        "clubs": [
            {"name": "Club A", "email": "clubA@example.com", "points": "10"}
        ]
    }

    # Remplace open par un faux fichier en mémoire
    def mock_open(*args, **kwargs):
        return StringIO(json.dumps(mock_clubs))

    monkeypatch.setattr("builtins.open", mock_open)

    clubs = loadClubs()
    assert isinstance(clubs, list)
    assert len(clubs) == 1
    assert clubs[0]["name"] == "Club A"
    assert clubs[0]["email"] == "clubA@example.com"
    assert clubs[0]["points"] == "10"


def test_loadCompetitions(monkeypatch):
    # Mock le contenu du fichier competitions.json
    mock_competitions = {
        "competitions": [
            {"name": "Competition A", "date": "2025-12-01 10:00:00", "numberOfPlaces": "100"}
        ]
    }

    def mock_open(*args, **kwargs):
        return StringIO(json.dumps(mock_competitions))

    monkeypatch.setattr("builtins.open", mock_open)

    competitions = loadCompetitions()
    assert isinstance(competitions, list)
    assert len(competitions) == 1
    assert competitions[0]["name"] == "Competition A"
    assert competitions[0]["date"] == "2025-12-01 10:00:00"
    assert competitions[0]["numberOfPlaces"] == "100"
