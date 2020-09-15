from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from tempfile import mkdtemp
import requests, ctypes, os, sys
from helpers import time, format, comma, assault, smg, lmg, sniper, shotgun, multiplayer, war
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError


# Configure the application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filters
app.jinja_env.filters["format"] = format
app.jinja_env.filters["comma"] = comma

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        username = request.form.get("username")
        code = request.form.get("code")

        # Set the proper platform text
        platform = request.form.get("platform")
        if platform == "Battle Net":
            platform = "battle"

        elif platform == "Playstation Network":
            platform = "psn"

        elif platform == "Xbox Live":
            platform = "xbl"

        # Else user did not provide a valid choice
        else :
            return render_template("apology.html", message="You must chose a platform")

        #Remember which user has been searched
        session["username"] = username
        session["code"] = code
        session["platform"] = platform
        session["multiplayer"] = True
        session["warzone"] = False

        # Retrieve user multiplayer stats
        stats = multiplayer(username, code, platform)

        # Verify if stats were retrieved
        if type(stats) is not dict:
            return render_template("apology.html", message=stats)


        return render_template("response.html", response=stats["response"], accuracy=stats["accuracy"], topWeapon=stats["topWeapon"],
            topWpnKills=stats["topWeaponKills"], topWpnHs=stats["topWeaponHeadshots"], topWpnDeaths=stats["topWeaponDeaths"],
            topWpnRatio=stats["topWeaponRatio"], topKillstreak=stats["topKillstreak"], topKillstreakUses=stats["topKillstreakUses"],
            topKillstreakAwarded=stats["topKillstreakAwarded"], playTime=stats["playTime"], selectedView=stats["selectedView"])

    else:
        # Forget any user searched
        session.clear()
        return render_template("index.html")

@app.route("/warzone")
def warzone():
    """Display the user's warzone stats"""

    # Retrieve user multiplayer stats
    warStats = war(session["username"], session["code"], session["platform"])
    multiStats = multiplayer(session["username"], session["code"], session["platform"])


    # Verify if warzone stats were retrieved
    if type(warStats) is not dict:
        return render_template("apology.html", message=warStats)

     # Verify if multiplayer stats were retrieved
    if type(multiStats) is not dict:
        return render_template("apology.html", message=multiStats)

    # Create a session view
    session["warzone"] = True
    session["multiplayer"] = False


    return render_template("warzone.html", response=warStats["response"], multiResponse=multiStats["response"], selectedView=warStats["selectedView"],
        playTime=warStats["playTime"], scorePerGame=warStats["scorePerGame"])

@app.route("/multiplayer")
def multi():
    """Retrieve multiplayer stats"""

    # Retrieve user multiplayer stats
    stats = multiplayer(session["username"], session["code"], session["platform"])

     # Verify if multiplayer stats were retrieved
    if type(stats) is not dict:
        return render_template("apology.html", message=tats)

    # Create a session view
    session["multiplayer"] = True
    session["warzone"] = False

    return render_template("response.html", response=stats["response"], accuracy=stats["accuracy"], topWeapon=stats["topWeapon"],
            topWpnKills=stats["topWeaponKills"], topWpnHs=stats["topWeaponHeadshots"], topWpnDeaths=stats["topWeaponDeaths"],
            topWpnRatio=stats["topWeaponRatio"], topKillstreak=stats["topKillstreak"], topKillstreakUses=stats["topKillstreakUses"],
            topKillstreakAwarded=stats["topKillstreakAwarded"], playTime=stats["playTime"], selectedView=stats["selectedView"])


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("apology.html", message=f"Error: {e.name}, {e.code}")


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
