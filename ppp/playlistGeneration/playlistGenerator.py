import re
import pandas as pd
import base64
import os
import math
import mimetypes
from tqdm import tqdm
from ppp.utils.paths import *
from ppp.utils.miscUtils import *


def image_to_base64(image_path=IMAGES_DIR/"poupette.png"):
    """
    returns the right image in base64 if the argument file name exists, it returns this image, otherwise, it returns the default image.

    :param image_path: the name of the image specified by the user.
    :return: this image in base64 if valid, default image if not.
    """
    if os.path.isfile(IMAGES_DIR/image_path):
        image_path = IMAGES_DIR/image_path
    if not os.path.isfile(image_path):
        image_path = DEFAULTIMAGES_DIR / "poupette.png"
    mime_type, _ = mimetypes.guess_type(image_path)
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode("utf-8")
        return f"data:{mime_type};base64,{encoded}"


def gen_playlist(titleAndSpecsTuple):
    """
    Generates the playlist as described by it's given argument, and puts it in Resulsts/Playlists.

    :param titleAndSpecsTuple: a tuple in the form of (title:str,{"Cover_Image":str, "Scores":[ *a list of scores formatted as dictionnaries like the CSV* ] } ).
    """
    title, specs = titleAndSpecsTuple[0], titleAndSpecsTuple[1]
    scores = specs["Scores"]
    image = specs["Cover_Image"]
    rankedplays = load_JSONFile(PLAYERDATA_FILE)["RANKEDPLAYCOUNT"]
    percent = round(((len(scores)/rankedplays)*100), 2)

    title = title+" ("+str(len(scores))+"/"+str(rankedplays) + \
        " = "+str(percent)+"% | "+str(round(100.0-percent, 2))+"%)"

    playlist = {
        "playlistTitle": title,
        "playlistAuthor": "la Poupette",
        "songs": [],
        "image": "base64," + image_to_base64(image)
    }

    for row in scores:
        match = re.match(
            r"_(.+)_Solo((?:[A-Z][a-z]*)+)", row["Difficulty"])
        if not match:
            print("Difficulty format error at: " +
                  row["Artist"]+" - "+row["Song"]+"("+row["Difficulty"]+")")
        diff, charac = match.groups()
        playlist["songs"].append({
            "songName": row["Song"],
            "levelAuthorName": row["Song"],
            "hash": row["Hash"],
            "levelid": f"custom_level_{row['Hash']}",
            "difficulties": [{
                "characteristic": charac,
                "name": diff
            }]
        })

    return json.dumps(playlist, indent=4)


def gen_multi_playlist(SpecsAndScoresDict):
    """
    Generates all thes playlists described by it's given argument, and puts them in Resulsts/Playlists.

    :param SpecsAndScoresDict: a dictionnary in the form of {title:str : {"Cover_Image":str, "Scores":[ *a list of scores formatted as dictionnaries like the CSV* ] } ).
    """
    lastUpdate = get_LastCSVdate()
    playerID = load_JSONFile(PLAYERDATA_FILE)["PLAYER_ID"]
    os.makedirs((PLAYLISTS_DIR / f'{playerID}_{lastUpdate}'), exist_ok=True)
    for (title, specs) in SpecsAndScoresDict.items():
        with open(PLAYLISTS_DIR / f"{playerID}_{lastUpdate}/{title}.bplist", "w") as f:
            f.write(gen_playlist((title, specs)))
        print(
            f"Playlist {title}.bplist\" generated.")
    print(
        f"All playlists generated! Find them in Results/Playlists/{playerID}_{lastUpdate}")
