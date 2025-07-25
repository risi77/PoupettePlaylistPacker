import copy
from ppp.utils.paths import *
from ppp.utils.miscUtils import *
from ppp.playlistGeneration.filters import *
from ppp.playlistGeneration.sorter import *


def complete_spec_handler():
    """
    Forms the final dictionnaries of dictionnaries, including everything needed to generate playlists.

    :return: A dictionnary of dictionnaries like:
        {   "playlist1Title":   {   "Preset":"[preset]",
                                    "Cover_Image":"imageName",
                                    "Scores":[
                                        *a list of scores formatted as dictionnaries like the CSV*
                                    ]
                            },
            "playlist2Title":   {   "Preset":"[preset]",
                                    "Cover_Image":"imageName",
                                    "Scores":[
                                        *a list of scores formatted as dictionnaries like the CSV*
                                    ]
                            }
        }
    """
    multiPlaylistSpec = Get_MultiPlaylistsSpec()
    finaldict = copy.deepcopy(multiPlaylistSpec)
    print("Filtering CSV scores")
    for (title, specsDict) in multiPlaylistSpec.items():
        finaldict[title].pop("Include_Perfect_Scores")
        finaldict[title].pop("SpecsMinMax")
        finaldict[title].pop("Sort")
        Include_Perfect_Scores = specsDict["Include_Perfect_Scores"]
        Sort = specsDict["Sort"]
        scores = multi_filter_CSV(
            specsDict["SpecsMinMax"], Include_Perfect_Scores)
        sortedScores = sort_scores(scores, Sort)
        finaldict[title]["Scores"] = sortedScores
    return finaldict


def Get_MultiPlaylistsSpec():
    """
    Loads the PlaylistsSpecs file and returns the appropriate filters, with defaults if nothing is specified
    Needs to be called after CSV is created

    :return: A dictionnary of dictionnaries like:
        {   "playlist1Title":   {   "Preset":"[preset]",
                                    "Cover_Image":"imageName",
                                    "Include_Perfect_Scores": bool,
                                    "SpecsMinMax":[
                                        {   "PP": (0, float("inf")),
                                            "Accuracy": (0.0, 100.0),
                                            "Miss": (0, float("inf")),
                                            "Rank": (1, float("inf")),
                                            "Country_Rank": (1, float("inf")),
                                            "Stars": (0, float("inf"))
                                        },
                                        {   "PP": (0, float("inf")),
                                            "Accuracy": (0.0, 100.0),
                                            "Miss": (0, float("inf")),
                                            "Rank": (1, float("inf")),
                                            "Country_Rank": (1, float("inf")),
                                            "Stars": (0, float("inf"))
                                        }
                                    ]
                            },
            "playlist2Title":   {   "Preset":"[preset]",
                                    "Cover_Image":"imageName",
                                    "Include_Perfect_Scores": bool,
                                    "SpecsMinMax":[
                                        {   "PP": (0, float("inf")),
                                            "Accuracy": (0.0, 100.0),
                                            "Miss": (0, float("inf")),
                                            "Rank": (1, float("inf")),
                                            "Country_Rank": (1, float("inf")),
                                            "Stars": (0, float("inf"))
                                        },
                                        {   "PP": (0, float("inf")),
                                            "Accuracy": (0.0, 100.0),
                                            "Miss": (0, float("inf")),
                                            "Rank": (1, float("inf")),
                                            "Country_Rank": (1, float("inf")),
                                            "Stars": (0, float("inf"))
                                        }
                                    ]
                            }
        }
    """
    playlistsSpecs = load_JSONFile(PLAYLISTS_SPECS_FILE)
    fullDict = {}
    preset_memory = {}  # keeps track of presets per playlist title

    for playlist in playlistsSpecs:
        title = playlist["Playlist_Name"]

        preset = ifExistsInDictOrElse(playlist, "Preset", "Default")

        # check for incoherent presets
        if title in preset_memory:
            if preset != preset_memory[title]:
                raise ValueError(
                    f"Preset mismatch in playlist '{title}': '{preset_memory[title]}' vs '{preset}'"
                )
        else:
            preset_memory[title] = preset

        Cover_Image = ifExistsInDictOrElse(
            playlist, "Cover_Image", "Poupette.png")
        Include_Perfect_Scores = ifExistsInDictOrElse(
            playlist, "Include_Perfect_Scores", False)
        Sort = ifExistsInDictOrElse(
            playlist, "Sort", "Recent_Desc")

        specsMinMax = trimSpecsToRange(playlist)

        if title in fullDict:
            print(f"merged two playlists titled \"{title}\"")
            fullDict[title]["SpecsMinMax"].append(specsMinMax)
        else:
            fullDict[title] = {
                "Preset": preset,
                "Cover_Image": Cover_Image,
                "Include_Perfect_Scores": Include_Perfect_Scores,
                "Sort": Sort,
                "SpecsMinMax": [specsMinMax]
            }

    return fullDict


def trimSpecsToRange(spec):
    """
    trims the users spec to maximum range, fixes user errors and fills in incomplete metrics

    :param specs: a dictionnary of the user's desired range for multiple metrics, not necessarely complete
    :return: A dictionnary with the min and max of each category
    """
    preset = spec["Preset"]

    if preset == "Default":
        DEFAULT_LIMITS = {
            "PP": (0, float("inf")),
            "Accuracy": (0.0, 100.0),
            "Miss": (0, float("inf")),
            "Rank": (1, float("inf")),
            "Country_Rank": (1, float("inf")),
            "Stars": (0, float("inf"))
        }
    elif preset == "PP_Playlist":
        DEFAULT_LIMITS = {
            "PlayersToScanAroundYou": 500,
            # aussi le maxScore, et un moyen d'avoir un booleen, peut etre rajouter dans specs?
            "MinimumWeighting": 500
        }
    else:
        raise Exception(
            f"Unknown Preset '{preset}' in spec: {spec.get('Playlist_Name')}")

    filter = {}
    for key, (default_min, default_max) in DEFAULT_LIMITS.items():
        userMin = getOrElse(spec.get(f'{key}_Min'), default_min)
        userMax = getOrElse(spec.get(f'{key}_Max'), default_max)

        if userMin > userMax:
            userMin, userMax = userMax, userMin
            print(f'{key}: min > max, swapped them')

        if userMin < default_min:
            print(
                f'{key} min ({userMin}) below allowed min ({default_min}), clamped.')
            userMin = default_min
        if userMax > default_max:
            print(
                f'{key} max ({userMax}) above allowed max ({default_max}), clamped.')
            userMax = default_max

        filter[key] = (userMin, userMax)

    return filter


def PrePassChecks() -> bool:
    """
    Will do a pre pass of the specs and determine if the script has to get the country ranks.

    :return: a Boolean telling if a country rank fetch is needed.
    """
    specs = load_JSONFile(PLAYLISTS_SPECS_FILE)
    for spec in specs:
        if "Sort" in spec:
            if (spec["Sort"].lower() == "sort_country_rank_asc") or (spec["Sort"].lower() == "sort_country_rank_desc"):
                return True
        if not (("Country_Rank_Min" in spec) or ("Country_Rank_Max" in spec)):
            continue
        elif ("Country_Rank_Max" in spec) and (spec["Country_Rank_Max"] > 1):
            return True
        elif ("Country_Rank_Min" in spec) and (spec["Country_Rank_Min"] > 1):
            return True

    return False
