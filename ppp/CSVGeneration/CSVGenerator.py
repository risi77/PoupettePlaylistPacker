from ppp.utils.paths import *
from ppp.CSVGeneration.scoresaberRequests import *
from ppp.utils.miscUtils import *
import pandas as pd
import os
import json
from tqdm import tqdm
tqdm.pandas()


def generateCSV(rankedScores, getCountryRanks=False):
    """
    Creates the .csv file containing info about all the ranked scores of the user.
    File is located at /Results/CSV/Results/CSV/scoresaber_ranked_{LASTUPDATE}.csv .
    Rows are explained in the readme.

    :param rankedScores: a list of ranked scores.
    :param getCountryRanks: wether the country ranks should be fetched, defaulted to False.
    """
    data = []
    for entry in rankedScores:
        score = entry["score"]
        leaderboard = entry["leaderboard"]
        timeset = score["timeSet"]
        data.append({
            "Song": leaderboard["songName"],
            "Artist": leaderboard["songAuthorName"],
            "LevelAuthor": leaderboard["levelAuthorName"],
            "Difficulty": leaderboard["difficulty"]["difficultyRaw"],
            "DiffInt": leaderboard["difficulty"]["difficulty"],
            "Accuracy": round(100*score["modifiedScore"] / leaderboard["maxScore"], 6) if leaderboard["maxScore"] else "err",
            "PP": score["pp"],
            "Rank": score["rank"],
            "Country_Rank": "NotFetched",
            "Score": score["modifiedScore"],
            "Miss": int((score["missedNotes"] + score["badCuts"]) or not score["fullCombo"]),
            "ONLYMiss": score["missedNotes"],
            "ONLYBadCut": score["badCuts"],
            "FullCombo": score["fullCombo"],
            "Weight": score["weight"],
            "Hash": leaderboard["songHash"],
            "Stars": leaderboard["stars"],
            "TimeSet": datetime.strptime(
                timeset, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d_%H-%M-%S"),
            "TimeStamp": int(datetime.strptime(
                timeset, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp())
        })
    df = pd.DataFrame(data)

    LASTUPDATE = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    playerID = load_JSONFile(PLAYERDATA_FILE)["PLAYER_ID"]

    df.to_csv(
        f"Results/CSV/scoresaber_ranked_{playerID}_{LASTUPDATE}.csv", index=False)
    print(
        f"'Results/CSV/scoresaber_ranked_{playerID}_{LASTUPDATE}.csv' file succesfully generated.")

    if getCountryRanks:
        addCountryRankToCSV()


def addCountryRankToCSV(leaderboard="SS"):
    """
    Adds country rank to every score present in the CSV. Must be called after the CSV has been created.
    """
    df = load_LastCSV()
    print("Fetching country ranks")

    def fetch_rank(row):
        return get_country_rank(row['Hash'], row['DiffInt']) or "?"

    df['Country_Rank'] = df.progress_apply(fetch_rank, axis=1)

    df.to_csv(CSV_DIR / get_LastCSVname(leaderboard), index=False)
    print(
        f"Successfully added country ranks to 'Results/CSV/{get_LastCSVname(leaderboard)}'.")
