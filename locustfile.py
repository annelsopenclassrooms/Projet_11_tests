from locust import HttpUser, task, between
import json
from datetime import datetime


class WebsiteUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://127.0.0.1:5000"

    def on_start(self):
        # Charger les clubs et compétitions depuis les fichiers pour avoir des données valides
        with open('clubs.json') as f:
            self.club = json.load(f)["clubs"][0]

        with open('competitions.json') as f:
            competitions = json.load(f)["competitions"]
            # Filtrer les compétitions à venir
            future_comps = [
                c for c in competitions
                if datetime.strptime(c["date"], "%Y-%m-%d %H:%M:%S") > datetime.now()
            ]
            self.competition = future_comps[0] if future_comps else competitions[0]

    @task
    def view_index(self):
        self.client.get("/")

    @task
    def login_and_book(self):
        # Step 1 : login
        with self.client.post("/showSummary", data={"email": self.club["email"]}, catch_response=True) as response:
            if "Welcome" not in response.text:
                response.failure("Login failed")
                return

        # Step 2: Access the booking page
        self.client.get(f"/book/{self.competition['name']}/{self.club['name']}")

        # Step 3 : book the places
        self.client.post("/purchasePlaces", data={
            "competition": self.competition["name"],
            "club": self.club["name"],
            "places": "1"
        })

    @task
    def view_points_board(self):
        self.client.get("/points-board")
