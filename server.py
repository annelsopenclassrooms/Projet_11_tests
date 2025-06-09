import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime

reservations = {}


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

clubs = loadClubs()
competitions = loadCompetitions()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form['email']
    club = next((c for c in clubs if c['email'] == email), None)

    if club is None:
        flash("Email not found. Please try again.")
        return redirect(url_for('index'))

    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = next((c for c in clubs if c['name'] == club), None)
    foundCompetition = next((c for c in competitions if c['name'] == competition), None)

    if foundClub and foundCompetition:
        competition_date = datetime.strptime(foundCompetition['date'], "%Y-%m-%d %H:%M:%S")
        if competition_date < datetime.now():
            flash("This competition has already taken place. Booking is not allowed.")
            return render_template('welcome.html', club=foundClub, competitions=competitions)
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong - please try again.")
        return render_template('welcome.html', club=foundClub, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs if c['name'] == request.form['club']), None)

    if not competition or not club:
        flash("Invalid competition or club.")
        return redirect(url_for('index'))

    competition_date = datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S")
    if competition_date < datetime.now():
        flash("Cannot book places for a past competition.")
        return render_template('welcome.html', club=club, competitions=competitions)

    placesRequired = int(request.form['places'])

    if placesRequired <= 0:
        flash("Number of places must be a positive number.")
        return render_template('welcome.html', club=club, competitions=competitions)

    club_name = club['name']

    if club_name not in reservations:
        reservations[club_name] = {}

    club_reservations = reservations[club_name]
    already_booked = club_reservations.get(competition['name'], 0)

    if placesRequired + already_booked > 12:
        flash("You cannot book more than 12 places in total for this competition.")
    else:
        if placesRequired > int(competition['numberOfPlaces']):
            flash("Not enough places left in this competition.")
        elif placesRequired > int(club['points']):
            flash("You cannot redeem more points than you have.")
        else:
            flash('Great - booking complete!')
            competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
            club['points'] = int(club['points']) - placesRequired
            club_reservations[competition['name']] = already_booked + placesRequired

    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/points-board')
def points_board():
    return render_template('points_board.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
