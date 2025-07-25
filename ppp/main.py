from ppp.CSVGeneration.CSVGenerator import *
from ppp.utils.paths import *
from ppp.playlistGeneration.playlistGenerator import *
from ppp.playlistGeneration.specsHandler import *
import requests
import pandas as pd
import sys
import time
import os


"""
Poupette Playlist Packer
Copyright (c) 2025 risi
Licensed under the MIT License
"""

######################################################################################################################################################
#   ____   __   _  _  ____  ____  ____  ____  ____        ____  __     __   _  _  __     __   ____  ____        ____   __    ___  __ _  ____  ____   #
#  (  _ \ /  \ / )( \(  _ \(  __)(_  _)(_  _)(  __)      (  _ \(  )   / _\ ( \/ )(  )   (  ) / ___)(_  _)      (  _ \ / _\  / __)(  / )(  __)(  _ \  #
#   ) __/(  O )) \/ ( ) __/ ) _)   )(    )(   ) _)        ) __// (_/\/    \ )  / / (_/\  )(  \___ \  )(         ) __//    \( (__  )  (  ) _)  )   /  #
#  (__)   \__/ \____/(__)  (____) (__)  (__) (____)      (__)  \____/\_/\_/(__/  \____/ (__) (____/ (__)       (__)  \_/\_/ \___)(__\_)(____)(__\_)  #
#                                                                                                                                                    #
######################################################################################################################################################


CSV_DIR.mkdir(parents=True, exist_ok=True)
PLAYLISTS_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

Json_config = get_config()
config = load_JSONFile("playerData")

PLAYER_ID = config["PLAYER_ID"]
PLAYER = config["PLAYER"]
TOTALPLAYCOUNT = config["TOTALPLAYCOUNT"]
RANKEDPLAYCOUNT = config["RANKEDPLAYCOUNT"]
COUNTRY = config["COUNTRY"]
RATELIMITER = config["RATELIMITER"]


def main():
    """
    Main method, orchestrates the whole project
    """
    if (TOTALPLAYCOUNT == -1 or RANKEDPLAYCOUNT == -1):
        print("Error while getting playcount stats.")
        return
    if IsCSVRefreshNeeded():
        print("Collecting scores...")
        scores = get_all_scores()
        print("filtering ranked scores")
        rankedScores = filter_ranked(scores)
        print("")

        generateCSV(rankedScores, PrePassChecks())
    print("")
    SpecsAndScoresDict = complete_spec_handler()
    print("")
    gen_multi_playlist(SpecsAndScoresDict)
    print("")

    df = load_LastCSV()
    scores = df.to_dict(orient="records")
    countrankfetched = isinstance(scores[1]["Country_Rank"], int)
    sumcountrank = 0
    sumrank = 0
    filtered_scores = []
    for score in scores:
        if countrankfetched:
            sumcountrank = sumcountrank+score["Country_Rank"]
        sumrank = sumrank+score["Rank"]
    print(f"Average global rank: {round(sumrank/len(scores), 3)}")
    if countrankfetched:
        print(f"Average country rank: {round(sumcountrank/len(scores), 3)}")

    print("")
    input("\nPress \"Enter\" to continue...")


if __name__ == "__main__":
    main()
