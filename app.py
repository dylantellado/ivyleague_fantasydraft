import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

from datetime import datetime

import pycountry

import random

import json

def share_common_element(list1, list2):
    for element in list1:
        if element in list2:
            return True
    return False

def generate_country_flags_dict():
    # Create a dictionary with country names and their flag URLs
    country_flags = {country.name: f"https://flagcdn.com/w320/{country.alpha_2.lower()}.png" for country in pycountry.countries}
    return country_flags

# Generate the dictionary
country_flags = generate_country_flags_dict()

# Dictionary for school images
ivy_league_badges = {
    "Brown": "static/images/Brown_Bears_logo.png",
    "Columbia": "static/images/Columbia_Lions_logo.png",
    "Cornell": "static/images/Cornell_Bears_logo.png",
    "Dartmouth": "static/images/Dartmouth_BigGreen_logo.png",
    "Harvard": "static/images/Harvard_Crimson_logo.png",
    "Penn": "static/images/Penn_Quakers_logo.png",
    "Princeton": "static/images/Princeton_Tigers_logo.png",
    "Yale": "static/images/Yale_Bulldogs_logo.png"
}


# Configure application
app = Flask(__name__)



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///players.db")




@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show homepage"""
    return render_template(
        "index.html",

    )


mf_list = []
df_list =[]
fw_list = []
gk_list = []

rows = db.execute("SELECT * FROM players")

for row in rows:
    if row['position'][0] == "F":
        fw_list.append(str(row["id"]))
    elif row['position'][0] == "M":
        mf_list.append(str(row['id']))
    elif row['position'][0] == "D":
        df_list.append(str(row['id']))
    elif row['position'][0] == "G":
        gk_list.append(str(row['id']))





@app.route("/playerselection", methods=["GET", "POST"])
@login_required
def playerselection():
    """Gives user their 4 options"""
    #if request.method == "POST":

    if request.method == "GET":
        return render_template("playerselection.html")



@app.route("/leaderboard", methods=["GET"])
@login_required
def leaderboard():
    """Displays Leaderboard"""

    # Execute the query and get the list directly
    user_rating_list = db.execute("SELECT * FROM UserRatings")

    # Sort the list in descending order by rating
    sorted_user_rating_list = sorted(user_rating_list, key=lambda x: x['teamRating'], reverse=True)

    # Now sorted_user_rating_list contains the sorted data



    return render_template("leaderboard.html", users = sorted_user_rating_list)

draft_players_dict = {}
team_rating = 0
id_used_list = []
print(id_used_list)

@app.route("/draft", methods=["GET", "POST"])
@login_required
def draft():
    """Handle player drafting on GET and POST requests."""

    # Handle POST requests for drafting players
    if request.method == "POST":
        button_id = request.form['player_id']

        # Check if the button pressed corresponds to a specific player position
        if button_id[0] in ["F", "M", "D", "G"]:
            # Reassign the button_id for clarity
            button_id = request.form['player_id']
            random_players = []

            # Draft players based on the position (Forward, Midfielder, Defender, Goalkeeper)
            if button_id in ['F1', 'F2', 'F3']:
                # Avoid repeating previously used players
                random_players = random.sample(fw_list, 4)
                while share_common_element(id_used_list,random_players):
                    print("DUPLICATE FORWARD")
                    random_players= random.sample(fw_list, 4)
                    #overlap = set(random_players) & set(id_used_list)
            elif button_id in ['M1', 'M2', 'M3']:

                random_players = random.sample(mf_list, 4)
                while share_common_element(id_used_list,random_players):
                    print("DUPLICATE MIDFIELDER")
                    random_players= random.sample(mf_list, 4)
                    #random_players = random.sample(mf_list, 4)

                    overlap = set(random_players) & set(id_used_list)
            elif button_id in ['D1', 'D2', 'D3', 'D4']:
                random_players = random.sample(df_list, 4)
                overlap = bool(set(random_players) & set(id_used_list))
                print("used list", id_used_list)
                print("players list", random_players)
                print(overlap)
                while overlap:
                    print("DUPLICATE DEFENDER")
                    random_players= random.sample(df_list, 4)
                    overlap = bool(set(random_players) & set(id_used_list))
                    #overlap = set(random_players) & set(id_used_list)
            elif button_id == 'G':
                random_players = random.sample(gk_list, 4)

            # Process the drafted players
            player_list = []
            for player in random_players:
                # Retrieve additional player information from the database
                college = db.execute("SELECT college FROM players WHERE id = ?", player)[0]["college"]
                badge = ivy_league_badges[college]
                country_name = db.execute("SELECT country FROM players WHERE id = ?", player)[0]["country"]

                # Standardize country names for consistency
                if country_name == "USA":
                    country_name = "United States"
                if country_name in ["England", "Scotland", "Republic of Ireland", "Wales", "Northern Ireland"]:
                    country_name = "United Kingdom"
                flag_url = country_flags[country_name]

                # Compile player information
                player_dict = db.execute("SELECT * FROM players WHERE id = ?", player)[0]
                player_dict["badge"] = badge
                player_dict["country"] = flag_url
                player_dict["slot"] = button_id
                player_name = player_dict["p_name"]
                rating = db.execute("SELECT points FROM playerpoints WHERE name = ?", player_name)
                if rating:
                    rating = rating[0]["points"]
                else:
                    rating = 55
                player_dict["rating"] = rating
                player_list.append(player_dict)

            # Render the player selection template with the list of players
            return render_template("playerselection.html", player_list=player_list)

        else:
            # Process the player ID for drafted players
            button_id = request.form['player_id']
            id_used_list.append(button_id)
            # Extract additional data for the drafted player
            slot = request.form['slot']
            player_dict = db.execute("SELECT * FROM players WHERE id = ?", button_id)[0]
            college = db.execute("SELECT college FROM players WHERE id = ?", button_id)[0]["college"]
            badge = ivy_league_badges[college]
            country_name = db.execute("SELECT country FROM players WHERE id = ?", button_id)[0]["country"]

            # Standardize country names
            if country_name == "USA":
                country_name = "United States"
            if country_name in ["England", "Scotland", "Republic of Ireland", "Wales", "Northern Ireland"]:
                country_name = "United Kingdom"
            flag_url = country_flags[country_name]

            # Update the player dictionary with additional information
            player_dict["badge"] = badge
            player_dict["country"] = flag_url
            player_dict["slot"] = slot
            player_name = player_dict["p_name"]
            rating = db.execute("SELECT points FROM playerpoints WHERE name = ?", player_name)
            if rating:
                rating = rating[0]["points"]
            else:
                rating = 55
            player_dict["rating"] = rating




            draft_players_dict[slot] = player_dict

            team_rating = 0
            for player in draft_players_dict:
                team_rating = team_rating + draft_players_dict[player]["rating"]

            if(len(draft_players_dict) > 0):
                team_rating_avg = team_rating / len(draft_players_dict)
            else:
                team_rating_avg = 0

            team_rating_avg = round(team_rating_avg)

            # Render the draft template with the drafted players' information
            # draft_players_dict is a dictionary of dictionaries
            return render_template("draft.html", draft_players_dict=draft_players_dict, team_rating = team_rating_avg)

    # Handle GET requests to display the draft page
    else:
        team_rating = 0
        for player in draft_players_dict:
            team_rating = team_rating + draft_players_dict[player]["rating"]
        if(len(draft_players_dict) > 0):
            team_rating_avg = team_rating / len(draft_players_dict)
        else:
            team_rating_avg = 0
        team_rating_avg = round(team_rating_avg)
        return render_template("draft.html", draft_players_dict=draft_players_dict, team_rating = team_rating_avg)


# A dictionary to store player information for the viewteam route
view_players_dict = {}

@app.route('/viewteam', methods=['GET'])
@login_required
def viewteam():
    """Display the user's team based on their saved selections."""

    # Retrieve the drafted players for the current user from the database
    players = db.execute("SELECT * FROM drafts WHERE user_id = ?", session["user_id"])

    # Iterate through each drafted player
    for player in players:
        # Get the slot the player is assigned to (e.g., F1, M2, etc.)
        slot = player["slot"]
        # Store the player's details in the view_players_dict under their slot
        view_players_dict[slot] = player

        # Get the college information of the player and find the corresponding badge
        college = player["college"]
        badge = ivy_league_badges[college]
        # Assign the badge to the player's information in the dictionary
        view_players_dict[slot]["badge"] = badge

        # Retrieve the image URL for the player from the database
        image = db.execute("SELECT * FROM players WHERE p_name = ?", player["p_name"])
        image_url = image[0]["image_url"]
        # Store the player's image URL in the dictionary
        view_players_dict[slot]["image_url"] = image_url
        rating = db.execute("SELECT points FROM playerpoints WHERE name = ?", player["p_name"])
        if rating:
            rating = rating[0]["points"]
        else:
            rating = 55
        view_players_dict[slot]["rating"] = rating

    team_rating = 0
    for player in view_players_dict:
        team_rating = team_rating + view_players_dict[player]["rating"]

        if(len(view_players_dict) > 0):
            team_rating_avg = team_rating / len(view_players_dict)
        else:
            team_rating_avg = 0

    team_rating_avg = round(team_rating_avg)
    # Render the viewteam template, passing the view_players_dict to display the team
    return render_template("viewteam.html", view_players_dict=view_players_dict, team_rating = team_rating_avg)





@app.route('/save', methods=['POST'])
def save():
    """Stores drafted player information in a database."""

    # Remove existing draft data for the current user
    db.execute("DELETE FROM drafts WHERE user_id = ?", session["user_id"])

    # Check if the draft_players_dict contains 11 players (a complete team)
    if len(draft_players_dict) == 11:
        # Iterate through each player in the drafted players dictionary
        for player in draft_players_dict:
            # Extract player information
            slot = player
            p_name = draft_players_dict[player]['p_name']
            position = draft_players_dict[player]['position']
            college = draft_players_dict[player]['college']
            country = draft_players_dict[player]['country']
            grade = draft_players_dict[player]['grade']
            number = draft_players_dict[player]['number']
            user_id = session["user_id"]

            # Insert the player's data into the drafts table in the database
            db.execute("INSERT INTO drafts (user_id, slot, p_name, position, college, country, grade, number) VALUES (:user_id,:slot,:p_name,:position,:college,:country,:grade,:number)", user_id=user_id, slot=slot, p_name=p_name, position=position, college=college, country=country, grade=grade, number=number)

        team_rating = 0
        for player in draft_players_dict:
            team_rating = team_rating + draft_players_dict[player]["rating"]

        if(len(draft_players_dict) > 0):
            team_rating_avg = team_rating / len(draft_players_dict)
        else:
            team_rating_avg = 0

        team_rating_avg = round(team_rating_avg)
        username = db.execute("SELECT username FROM users WHERE id = ?", user_id)
        username = username[0]["username"]
        db.execute("INSERT INTO UserRatings (username, teamRating) VALUES (:user_id, :rating)", user_id = username, rating=team_rating_avg,)

    # Redirect to the draft page after saving
    return redirect(url_for('draft'))


@app.route('/reset', methods=['POST'])
def reset():
    """Handles the resetting of the draft selections."""

    # Clear the current draft selections from the draft_players_dict
    draft_players_dict.clear()


    # Clear the list of used player IDs
    id_used_list.clear()

    # Render the draft page with an empty draft_players_dict
    # This effectively resets the draft selections on the page
    return render_template('draft.html', draft_players_dict=draft_players_dict)



@app.route("/standings", methods=["GET"])
def standings():
    """Renders the standings page"""
    return render_template("standings.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    draft_players_dict.clear()

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/searchplayer", methods=["GET", "POST"])
@login_required
def searchplayer():
    """Route to enable users to search for Ivy League players."""

    # Handle POST requests when a user submits the player search form
    if request.method == "POST":
        # Retrieve the name of the player from the form
        name = request.form.get("playername")

        # Query the database for the player's image using a case-insensitive search
        image = db.execute("SELECT image_url FROM players WHERE LOWER(p_name) = ?", name.lower())

        # Check if the player is found in the database
        if not image:
            # Return an error message if the player is not found
            return apology("Player not found", 400)

        # Extract the image URL from the query result
        image_url = image[0]["image_url"]

        # Query for additional details of the player
        player_name = db.execute("SELECT p_name FROM players WHERE LOWER(p_name) = ?", name.lower())[0]["p_name"]
        jerseynum = db.execute("SELECT number FROM players WHERE LOWER(p_name) = ?", name.lower())[0]["number"]
        position = db.execute("SELECT position FROM players WHERE LOWER(p_name) = ?", name.lower())[0]["position"]
        rating = db.execute("SELECT points FROM playerpoints WHERE name = ?", player_name)
        if rating:
            rating = rating[0]["points"]
        else:
            rating = 55


        # Adjust the position value for goalkeepers
        if position == "G":
            position = "GK"

        # Query for the player's country and standardize its name
        country_name = db.execute("SELECT country FROM players WHERE LOWER(p_name) = ?", name.lower())[0]["country"]
        if country_name == "USA":
            country_name = "United States"
        if country_name == "England":
            country_name = "United Kingdom"
        flag_url = country_flags[country_name]

        # Query for the player's college and retrieve the corresponding badge
        college = db.execute("SELECT college FROM players WHERE LOWER(p_name) = ?", name.lower())[0]["college"]
        badge = ivy_league_badges[college]

        # Render the player card with all the retrieved information
        return render_template(
            "playercards.html",
            name=player_name,
            image_url=image_url,
            number=jerseynum,
            position=position,
            flag_url=flag_url,
            badge=badge,
            rating=rating
        )

    # Handle GET requests to show the player search form
    else:
        return render_template("searchplayer.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        # Ensure password was confirmed
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)
        elif not (request.form.get("password") == request.form.get("confirmation")):
            return apology("passwords must match", 400)
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if user:
            return apology("username already taken", 400)

        # Adding a user

        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            request.form.get("username"),
            generate_password_hash(request.form.get("password")),
        )

        rows = db.execute(
            "SELECT id FROM users WHERE username = ?", request.form.get("username")
        )
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
