import math
import requests
from tqdm import tqdm
import json
import time
from ppp.utils.miscUtils import *
from ppp.utils.paths import *


def get_playerStats(PLAYER_ID):
    """
    Asks Scoresaber for full player info

    :param Player_ID: The player ID you want info on
    :return: Full player info formatted in JSON
    """
    url = f"https://scoresaber.com/api/player/{PLAYER_ID}/full"
    return (requests.get(url, timeout=10))


def get_all_scores():
    """
    Asks Scoresaber for N scores from the player's profile

    :return: Full player scores, as a list of scores
    """
    playerdata = load_JSONFile(PLAYERDATA_FILE)
    MAX_MAPS = playerdata["TOTALPLAYCOUNT"]
    PLAYER_ID = playerdata["PLAYER_ID"]
    RATELIMITER = playerdata["RATELIMITER"]
    all_scores = []
    seen_keys = set()
    page = 1

    with tqdm(total=MAX_MAPS) as pbar:
        while len(all_scores) < MAX_MAPS:
            url = f"https://scoresaber.com/api/player/{PLAYER_ID}/scores?sort=recent&page={page}&limit=100"
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                print(f"Error at page {page} (status {response.status_code})")
                break

            scores = response.json().get("playerScores", [])
            if not scores:
                print("No more scores returned.")
                break

            added_this_page = 0
            for s in scores:
                key = (s["leaderboard"]["songHash"], s["leaderboard"]
                       ["difficulty"]["difficultyRaw"])
                if key not in seen_keys:
                    seen_keys.add(key)
                    all_scores.append(s)
                    pbar.update(1)
                    added_this_page += 1

                    if len(all_scores) >= MAX_MAPS:
                        break

            if added_this_page == 0:
                print("All scores in this page are duplicates. Ending.")
                break

            page += 1
            time.sleep(RATELIMITER)

    print(f"Total unique scores collected: {len(all_scores)}")
    return all_scores


def get_country_rank(hash_, DiffInt):
    """
    Asks Scoresaber for the player's country rank on one map

    :param hash_: the hash of the map you want the country rank on
    :param DiffInt: the difficulty of the score you want the country rank on

    :return: the country rank of the given difficulty
    """
    page = 1
    COUNTRY = load_JSONFile(PLAYERDATA_FILE)["COUNTRY"]
    PLAYER_ID = load_JSONFile(PLAYERDATA_FILE)["PLAYER_ID"]
    RATELIMITER = load_JSONFile(PLAYERDATA_FILE)["RATELIMITER"]
    while True:
        url = f"https://scoresaber.com/api/leaderboard/by-hash/{hash_}/scores?difficulty={DiffInt}&countries={COUNTRY}&page={page}"
        response = requests.get(url)
        time.sleep(RATELIMITER)
        if response.status_code == 200:
            data = response.json()
            scores = data.get("scores", [])

            for score in scores:
                if score["leaderboardPlayerInfo"]["id"] == PLAYER_ID:
                    return score["rank"]

            if not scores or len(scores) < 1:
                return None
            else:
                page += 1
        else:
            print(
                f"Getting country rank: request error at page {page} (code: {response.status_code})")
            return None


def IsCSVRefreshNeeded(leaderboard="SS"):
    """
    Checks if last score uploaded to the leaderboard is older than the last CSV generation

    :return:
    """
    playerData = load_JSONFile(PLAYERDATA_FILE)
    playerID = playerData["PLAYER_ID"]
    if (get_LastCSVname(leaderboard) != None):
        from ppp.playlistGeneration.specsHandler import PrePassChecks
        csv_path = CSV_DIR / get_LastCSVname(leaderboard)
        lastUpdate = get_LastCSVdate(leaderboard)
        df = load_LastCSV()
        scores = df.to_dict(orient="records")

        # checks if last refresh has been done in the previous 24 hours, else tells to refresh
        if (str_to_timestamp(lastUpdate)+86400) < int(datetime.now().timestamp()):
            return True
        # if the country rank is needed, returns wether the countryrank has already been fetched
        if PrePassChecks():
            return not (isinstance(scores[1]["Country_Rank"], int))
        # if file exists, has been refreshed in the last 24 hours and has country ranks if needed but last score still is fresher, then refresh
        if (get_timestamp_last_score() > str_to_timestamp(lastUpdate)):
            return True
    else:
        return True

    return (get_timestamp_last_score() > str_to_timestamp(lastUpdate))


def get_timestamp_last_score():
    rateLimiter = load_JSONFile(PLAYERDATA_FILE)["RATELIMITER"]
    PLAYER_ID = load_JSONFile(PLAYERDATA_FILE)["PLAYER_ID"]
    url = f"https://scoresaber.com/api/player/{PLAYER_ID}/scores?sort=recent&page=1&limit=1"
    response = requests.get(url, timeout=10)
    LastScore = (response.json().get("playerScores", []))[
        0]["score"]["timeSet"]

    time.sleep(rateLimiter)

    timestamp_LastScore = datetime.strptime(
        LastScore, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()

    return int(timestamp_LastScore)


def filter_ranked(scores):
    """
    filters out any unranked scores from a list of scores.

    :param scores: list of scores
    :return: list of only ranked scores
    """
    ranked_scores = []
    paranked = 0
    for entry in scores:
        if entry["leaderboard"]["ranked"]:
            ranked_scores.append(entry)
        else:
            paranked += 1
    print(str(paranked)+" unranked scores , " +
          str(len(ranked_scores))+" ranked scores.")
    return ranked_scores


def Generate_RankedMapsCSV():
    csv_path = (SCORESABER_RANKEDMAPS_FILE)
    if not csv_path.is_file():
        raise FileNotFoundError(f"CSV not found at : {csv_path}")
