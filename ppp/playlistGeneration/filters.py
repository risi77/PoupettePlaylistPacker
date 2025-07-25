import pandas as pd
from ppp.utils.paths import *
from ppp.utils.miscUtils import *

SpecTypes = {
    "PP": float,
    "Accuracy": float,
    "Miss": int,
    "Rank": int,
    "Country_Rank": int,
    "Stars": float
}


def filter_CSV(specsMinMax, Include_Perfect_Scores):
    """
    Filters out any score that doesn't comply with the limits in specsMinMax.

    :param specsMinMax: dict with {column_name: (min, max)}
    :param Include_Perfect_Scores: boolean that dictates if un-PB-able scores get in the playlist.
    :return: list of ranked scores (as dicts) that are within the specs
    """

    df = load_LastCSV()
    scores = df.to_dict(orient="records")

    filtered_scores = []
    for score in scores:

        valid = True
        for key, (min_val, max_val) in specsMinMax.items():
            val = score[key]
            if not (isinstance(val, SpecTypes[key])):
                if (key == "Country_Rank" and val == "NotFetched"):
                    continue
                print(score)
                valid = False
                break
            if not (min_val - 0.0001 <= val <= max_val + 0.0001):  # wiggle room
                valid = False
                break

        if valid and (score["Accuracy"] != 100.0 or (score["Accuracy"] == 100.0 and Include_Perfect_Scores)):
            filtered_scores.append(score)

    return filtered_scores


def multi_filter_CSV(multiSpecsMinMax, Include_Perfect_Scores):
    """
    Uses filter_CSV(specsMinMax) and merges the filtered scores if multiSpecsMinMax contains more than one Specs Dict

    :param multiSpecsMinMax: list of Specs dictionnaries with {column_name: (min, max)}.
    :param Include_Perfect_Scores: boolean that dictates if un-PB-able scores get in the playlist.
    :return: list of ranked scores that are within the specs of at least one of the Specs Dict
    """
    seen = set()
    scores = []
    for SpecsMinMax in multiSpecsMinMax:
        filtered = filter_CSV(SpecsMinMax, Include_Perfect_Scores)
        for score_dict in filtered:
            key = tuple(sorted(score_dict.items()))
            if key not in seen:
                seen.add(key)
                scores.append(score_dict)
    return scores
