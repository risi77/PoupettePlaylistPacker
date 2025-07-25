import json
import os
import re
import pandas as pd
from datetime import datetime
from ppp.utils.paths import *


def getOrElse(X, Y):
    """
    returns X if it exists, Y otherwise

    :param X: maybe something
    :param Y: default
    :return: returns X if it exists, Y otherwise
    """
    return X if X is not None else Y


def ifExistsInDictOrElse(dict, StrKey, default):
    """
    returns the value of a key that maybe exists in a Dictionnary, else a default. Also adds the default in the ict if nothing is found

    :param dict: The Dictionnary you want to search into
    :param StrKey: the key that maybe exists in the Dict
    :param default: the default return value
    :return: returns the value of a key that maybe exists in a Dictionnary, else a default
    """
    if StrKey in dict:
        return dict[StrKey]
    else:
        dict[StrKey] = default
        return default


def floatingPointToFixedPoint(number):
    if isinstance(number, float):
        return number
    return


# FILES PATH Aliases
NAMED_FILES = {
    "config": CONFIG_FILE,
    "spec": PLAYLIST_SPECS_FILE,
    "specs": PLAYLISTS_SPECS_FILE,
    "playerData": PLAYERDATA_FILE,
    "SSRankedMaps": SCORESABER_RANKEDMAPS_FILE,
    "testfile1": TESTJSONS_FILE,
    "testfile2": TESTJSONS_SUBFILE,
}

# DIRS PATH Aliases
NAMED_DIRS = {
    "root": ROOT_DIR,
    "ppp": PPP_DIR,
    "images": IMAGES_DIR,
    "DefaultImages": DEFAULTIMAGES_DIR,
    "results": RESULTS_DIR,
    "data": DATA_DIR,
    "csv": CSV_DIR,
    "playlists": PLAYLISTS_DIR,
    "testdir1": TESTJSONS_DIR,
    "testdir2": TESTJSONS_SUBDIR,
}


def load_JSONFile(name_or_path):
    """
    Reads a Json file based on alias or path.

    Accepts either:
    - A Path directly
    - A string using aliases. Aliases are found above this function

    if name is a path, then it reads the json found at this path.
    If name is a string:
    3 cases :
    - Name is a known file alias : load file
    - Name has a format like "DIR_alias/fileName" : load filename in ALIAS
    - Name is an unknown path : interpreted as raw file path from root

    :param name: either a PATH, or a string with an alias to a file or folder (without .json at the end)
    :return: name's JSON content
    """
    filepath = pathAsSTRhandler(name_or_path)

    if not filepath.exists():
        if not filepath.is_file():
            raise FileNotFoundError(f"No JSON file found at: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def dumpToJson(location, content):
    """
    Dumps a JSON formatted collection into a JSON

    :param location: where you want the JSON to be, and what you want it's name to be
    :param name:
    """
    path = pathAsSTRhandler(location)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=4)
        f.flush()
        os.fsync(f.fileno())


def pathAsSTRhandler(name_or_path):
    """
    returns the path you've given it or a path that corresponds to the STR with or without aliases representing a path you have given it.

    :param name_or_path: the STR or path
    :return: The full resolved Path
    """

    if isinstance(name_or_path, str):
        return stringAliasToPath(name_or_path)
    elif isinstance(name_or_path, Path):
        return name_or_path
    else:
        raise TypeError("The parameter isn't a string or a PATH")


def stringAliasToPath(name: str):
    """
    gives a PATH from a string with or without aliases

    :param name: A string representing either:
                 - a file alias (e.g. "config")
                 - an aliased directory + filename (e.g. "data/stats")
                 - or a raw path from ROOT
    :return: The full resolved Path
    """
    path_parts = Path(name.replace("\\", "/")).parts

    if name in NAMED_FILES:
        filepath = NAMED_FILES[name]

    elif path_parts[0] in NAMED_DIRS:
        filepath = NAMED_DIRS[path_parts[0]].joinpath(
            *path_parts[1:])

    else:
        filepath = ROOT_DIR / Path(name)

    return filepath


def get_SSinfo(Player_ID):
    """
    Imports scoresaberRequests locally and gets full scoresaber player info

    :param Player_ID: The player ID you want info on
    :return: Full player info formatted in JSON
    """
    from ppp.CSVGeneration.scoresaberRequests import get_playerStats
    return get_playerStats(Player_ID)


def get_config():
    """
    Gives full info about the player, and dumps it in Data/PlayerData.json

    PLAYER_ID, MAX_MAPS, COUNTRYRANKSORT, SORT, TARGET, PLAYER, TOTALPLAYCOUNT, RANKEDPLAYCOUNT, COUNTRY, RATELIMITER, CHECK_SS, CHECK_NEWMAPS
    """
    config = load_JSONFile("config")
    fresh_player_stats = get_SSinfo(config["PLAYER_ID"])
    PlayerData = {
        "PLAYER_ID": config["PLAYER_ID"],
        "PLAYER": fresh_player_stats.json().get("name", []),
        "TOTALPLAYCOUNT": fresh_player_stats.json().get("scoreStats", []).get("totalPlayCount", []),
        "RANKEDPLAYCOUNT": fresh_player_stats.json().get("scoreStats", []).get("rankedPlayCount", []),
        "COUNTRY": fresh_player_stats.json().get("country", []),
        "RATELIMITER": config["I_PROMISE_IM_NOT_DDOSING"]
    }

    dumpToJson(PLAYERDATA_FILE, PlayerData)


def load_LastCSV(leaderboard="SS"):
    df = pd.read_csv(CSV_DIR / get_LastCSVname(leaderboard))
    return df


def get_LastCSVname(leaderboard="SS"):
    """
    returns the name of the last CSV with the active PlayerID data

    :param: leaderboard: what leaderboard's CSV are going to be checked, defaulted to SS
    :return: the exact name of the latest file.
    """
    PlayerID = load_JSONFile(PLAYERDATA_FILE)["PLAYER_ID"]
    if leaderboard == "BL":
        fullLDname = "beatleader"
    elif leaderboard == "SS":
        fullLDname = "scoresaber"
    else:
        raise Exception("unknown leaderboard given")
    pattern = re.compile(
        rf"^{fullLDname}_ranked_{PlayerID}_(\d{{4}}-\d{{2}}-\d{{2}}_\d{{2}}-\d{{2}}-\d{{2}})\.csv$")
    file_matches = []
    for file in CSV_DIR.iterdir():
        if file.is_file():
            match = pattern.match(file.name)
            if match:
                date_str = match.group(1)
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d_%H-%M-%S")
                    file_matches.append((date, file.name))
                except ValueError:
                    continue
    if not file_matches:
        return None
    file_matches.sort(reverse=True)
    return file_matches[0][1]


def get_LastCSVdate(leaderboard="SS"):
    """
    returns the 'YYYY-MM-DD_HH-MM-SS' part of the specified Player's last CSV
    """
    filename = get_LastCSVname(leaderboard)
    if not filename:
        return None

    match = re.search(r"(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})", filename)
    if match:
        return match.group(1)
    return None


def load_LastCSV(leaderboard="SS"):
    if get_LastCSVname(leaderboard) != None:
        return pd.read_csv(CSV_DIR / get_LastCSVname(leaderboard))


def timestamp_to_str(timestamp):
    """
    Converts a timestamp (int or float) to STR 'YYYY-MM-DD_HH-MM-SS'.
    """
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d_%H-%M-%S")


def str_to_timestamp(date_str):
    """
    Converts STR 'YYYY-MM-DD_HH-MM-SS' to Timestamp (int).
    """
    dt = datetime.strptime(date_str, "%Y-%m-%d_%H-%M-%S")
    return int(dt.timestamp())
