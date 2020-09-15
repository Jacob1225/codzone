import os, math, requests

def time(time_played):
    """Convert seconds to days, hours, minutes"""

    seconds_in_day = 60*60*24
    seconds_in_hour = 60*60

    # Find number of days played
    days = math.floor(time_played / seconds_in_day)

    # Find number of hours played
    hours = math.floor((time_played - (days * seconds_in_day)) / seconds_in_hour)

    # Find number of minutes played
    mins = math.floor((time_played - (days * seconds_in_day) - (hours * seconds_in_hour)) / 60)

    total_time = f"{days}D {hours}H {mins}M"
    return total_time

def format(value):
    """format all values to 2 decimal places"""
    formatted_value = round(value, 2)
    return formatted_value

def comma(value):
    """format all numbers with commas at every thousand"""
    return ("{:,}".format(value))


def assault(weapon_name):
    """format assault rifle weapon names"""
    rifles = {
        "iw8_ar_falima": "FAL",
        "iw8_ar_tango21":"RAM-7",
        "iw8_ar_mike4": "M4A1",
        "iw8_ar_anovember94": "AN-94",
        "iw8_ar_arfalpha": "FR 5.56",
        "iw8_ar_mcharlie": "M13",
        "iw8_ar_akilo47": "AK-47",
        "iw8_ar_kilo433": "Kilo 141",
        "iw8_ar_scharlie": "FN Scar17",
        "iw8_ar_asierra12": "Oden",
        "iw8_ar_galima": "CR-56 AMAX",
        "iw8_ar_sierra552": "Grau 5.56"
    }

    return rifles[weapon_name]

def smg(weapon_name):
    """format smg weapon names"""
    sub_machine = {
        "iw8_sm_mpapa7": "MP7",
        "iw8_sm_augolf": "AUG",
        "iw8_sm_papa90": "P90",
        "iw8_sm_charlie9": "ISO",
        "iw8_sm_mpapa5": "MP5",
        "iw8_sm_smgolif45": "Striker 45",
        "iw8_sm_beta": "PP19 Bizon",
        "iw8_sm_victor": "Fennec",
        "iw8_sm_uzulu": "UZI"
    }

    return sub_machine[weapon_name]

def shotgun(weapon_name):
    """format shotgun weapon names"""
    shotty = {
        "iw8_sh_mike26": "VLK Rogue",
        "iw8_sh_charlie725": "725",
        "iw8_sh_oscar12": "origin 12 shotgun",
        "iw8_sh_romeo970": "Model 680",
        "iw8_sh_dpapa12": "R9-O shotgun"
    }

    return shotty[weapon_name]

def sniper(weapon_name):
    """format sniper weapon names"""
    snipes = {
        "iw8_sn_alpha50": "AX-50",
        "iw8_sn_hdromeo": "HDR",
        "iw8_sn_delta": "Dragunov",
        "iw8_sn_xmike109": "Rytec AMR"
    }

    return snipes[weapon_name]

def lmg(weapon_name):
    """format lmg weapon names"""
    light_machine_guns = {
        "iw8_lm_kilo121": "M91",
        "iw8_lm_lima86": "SA87",
        "iw8_lm_mgolf34": "MG34",
        "iw8_lm_mgolf36": "Holger-26",
        "iw8_lm_pkilo": "PKM",
        "iw8_mkilo3": "Bruen MK9",
        "iw8_lm_sierrax": "FINN"
    }

    return light_machine_guns[weapon_name]

def multiplayer(username, code, platform):
    """returns the users multiplayer stats"""

    url = f"https://call-of-duty-modern-warfare.p.rapidapi.com/multiplayer/{username}%2523{code}/{platform}"

    headers = {
        'x-rapidapi-host': "call-of-duty-modern-warfare.p.rapidapi.com",
        'x-rapidapi-key': "8264ad8a7bmshbb5f2440c32580bp1acd9bjsnb19fc39793df"
    }

    response = requests.request("GET", url, headers=headers)

    # if user was not found or stats could not be retrieve
    if "error" in response.text:
        message = "Could not retrieve stats! Please make sure you have the correct username, hashtag and platform"
        return message

    # If successfully retrieved stats
    r = response.json()

    # Calculate player accuracy
    hits = r["lifetime"]["all"]["properties"]["hits"]
    misses= r["lifetime"]["all"]["properties"]["misses"]
    accuracy = round((hits / misses) * 100, 2)

    # Find the players top weapon
    kills = {
        "assault_rifle": r["lifetime"]["accoladeData"]["properties"]["arKills"],
        "lmg": r["lifetime"]["accoladeData"]["properties"]["lmgKills"],
        "smg": r["lifetime"]["accoladeData"]["properties"]["smgKills"],
        "shotgun": r["lifetime"]["accoladeData"]["properties"]["shotgunKills"],
        "sniper": r["lifetime"]["accoladeData"]["properties"]["sniperKills"]
    }

    # Loop through weapon kills to find the most kills
    topWeaponCategory = "assault_rifle"
    for key in kills:
        if kills[key] > kills[topWeaponCategory]:
            topWeaponCategory = key

    # Loop through weapon class to find top weapon
    weaponClass = r["lifetime"]["itemData"][f"weapon_{topWeaponCategory}"]
    topWeapon = ""
    for weapon in weaponClass:
        if topWeapon == "":
            topWeapon = weapon

        elif weaponClass[weapon]["properties"]["kills"] > weaponClass[topWeapon]["properties"]["kills"]:
            topWeapon = weapon

    # Get top weapon kills k/d deaths and headshots
    topWeaponKills = r["lifetime"]["itemData"][f"weapon_{topWeaponCategory}"][f"{topWeapon}"]["properties"]["kills"]
    topWeaponDeaths = r["lifetime"]["itemData"][f"weapon_{topWeaponCategory}"][f"{topWeapon}"]["properties"]["deaths"]
    topWeaponRatio = r["lifetime"]["itemData"][f"weapon_{topWeaponCategory}"][f"{topWeapon}"]["properties"]["kdRatio"]
    topWeaponHeadshots = r["lifetime"]["itemData"][f"weapon_{topWeaponCategory}"][f"{topWeapon}"]["properties"]["headshots"]

    # Format the top weapon name
    if topWeaponCategory == "assault_rifle":
        topWeapon = assault(topWeapon)

    elif topWeaponCategory == "lmg":
        topWeapon = lmg(topWeapon)

    elif topWeaponCategory == "smg":
        topWeapon = smg(topWeapon)

    elif topWeaponCategory == "sniper":
        topWeapon = sniper(topWeapon)

    elif topWeaponCategory == "shotgun":
        topWeapon = shotgun(topWeapon)

    # Get the user's top killstreak

    # Top lethal killstreak
    lethalKillstreak = r["lifetime"]["scorestreakData"]["lethalScorestreakData"]
    topLethal = ""
    topLethalUses = 0
    topLethalAwarded = 0
    for scorestreak in lethalKillstreak:
        if topLethal == "":
            topLethal = scorestreak
            topLethalUses = lethalKillstreak[scorestreak]["properties"]["uses"]
            topLethalAwarded = lethalKillstreak[scorestreak]["properties"]["awardedCount"]

        elif lethalKillstreak[scorestreak]["properties"]["awardedCount"] > lethalKillstreak[topLethal]["properties"]["awardedCount"]:
            topLethal = scorestreak
            topLethalUses = lethalKillstreak[scorestreak]["properties"]["uses"]
            topLethalAwarded = lethalKillstreak[scorestreak]["properties"]["awardedCount"]

    # Top support killstreak
    supportKillstreak = r["lifetime"]["scorestreakData"]["supportScorestreakData"]
    topSupport = ""
    topSupportUses = 0
    topSupportAwarded = 0

    for killstreak in supportKillstreak:
        if topSupport == "":
            topSupport = killstreak
            topSupportUses = supportKillstreak[killstreak]["properties"]["uses"]
            topSupportAwarded = supportKillstreak[killstreak]["properties"]["awardedCount"]

        elif supportKillstreak[killstreak]["properties"]["awardedCount"] > supportKillstreak[topSupport]["properties"]["awardedCount"]:
            topSupport = killstreak
            topSupportUses = supportKillstreak[killstreak]["properties"]["uses"]
            topSupportAwarded = supportKillstreak[killstreak]["properties"]["awardedCount"]

    # Find the highest award count between the top lethal and top support killstreak
    if topSupportAwarded > topLethalAwarded:
        topKillstreak = topSupport
        topKillstreakUses = topSupportUses
        topKillstreakAwarded = topSupportAwarded

    else:
        topKillstreak = topLethal
        topKillstreakUses = topLethalUses
        topKillstreakAwarded = topLethalAwarded

    # Format the users total time played
    playTime = time(r["lifetime"]["all"]["properties"]["timePlayedTotal"])

    stats = {
        "playTime": playTime,
        "topKillstreak": topKillstreak,
        "topKillstreakUses": topKillstreakUses,
        "topKillstreakAwarded": topKillstreakAwarded,
        "topWeapon": topWeapon,
        "topWeaponKills": topWeaponKills,
        "topWeaponDeaths": topWeaponDeaths,
        "topWeaponRatio": topWeaponRatio,
        "topWeaponHeadshots": topWeaponHeadshots,
        "accuracy": accuracy,
        "selectedView": "multiplayer",
        "response": r
    }

    return stats

def war(username, code, platform):


    """Get user's warzone stats"""
    url = f"https://call-of-duty-modern-warfare.p.rapidapi.com/warzone/{username}%2523{code}/{platform}"

    headers = {
    'x-rapidapi-host': "call-of-duty-modern-warfare.p.rapidapi.com",
    'x-rapidapi-key': "8264ad8a7bmshbb5f2440c32580bp1acd9bjsnb19fc39793df"
    }

    response = requests.request("GET", url, headers=headers)

    # if user was not found or stats could not be retrieve
    if "error" in response.text:
        message = "Could not retrieve stats! Please make sure you have the correct username, hashtag and platform"
        return message

    # If successfully retrieved stats
    r = response.json()

    # Format the users total time played
    playTime = time(r["br_all"]["timePlayed"])

    # Find the user's score per game
    gamesPlayed = r["br_all"]["gamesPlayed"]
    score = r["br_all"]["score"]

    scorePerGame = score / gamesPlayed

    stats = {
        "selectedView": "warzone",
        "playTime": playTime,
        "scorePerGame": scorePerGame,
        "response": r
    }

    return stats

