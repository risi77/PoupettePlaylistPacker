import json
import pytest
from ppp.playlistGeneration.specsHandler import *
from ppp.utils.paths import *
from pathlib import Path
import time
from copy import deepcopy


@pytest.mark.parametrize("input1, expected", [
    (
        {
            "Playlist_Name": "test1",
            "Preset": "Default",
            "Stars_min": 0,
            "Stars_max": 13,
            "PP_min": 0,
            "PP_max": 1000,
            "Accuracy_min": 0,
            "Accuracy_max": 100,
            "Miss_min": 0,
            "Miss_max": 10000,
            "Rank_min": 1,
            "Rank_max": 999999,
            "Country_Rank_min": 1,
            "Country_Rank_max": 999999
        },
        {
            "PP": (0, 1000),
            "Accuracy": (0, 100),
            "Miss": (0, 10000),
            "Rank": (1, 999999),
            "Country_Rank": (1, 999999),
            "Stars": (0, 13)
        }
    ),
    (
        {
            "Playlist_Name": "test2",
            "Preset": "Default",
            "Stars_min": -3,
            "Stars_max": 103,
            "PP_min": 10,
            "PP_max": 1003,
            "Accuracy_min": -30,
            "Accuracy_max": 100,
            "Miss_min": 0,
            "Miss_max": 0,
            "Rank_min": 0,
            "Rank_max": 15
        },
        {
            "PP": (10, 1003),
            "Accuracy": (0, 100),
            "Miss": (0, 0),
            "Rank": (1, 15),
            "Country_Rank": (1, float("inf")),
            "Stars": (0, 103)
        }
    ),
    (
        {
            "Playlist_Name": "test3",
            "Preset": "Default",
            "Stars_min": 7,
        },
        {
            "PP": (0, float("inf")),
            "Accuracy": (0, 100),
            "Miss": (0, float("inf")),
            "Rank": (1, float("inf")),
            "Country_Rank": (1, float("inf")),
            "Stars": (7, float("inf"))
        }
    ),
    (
        {
            "Playlist_Name": "test2",
            "Preset": "Default",
            "Stars_min": 6,
            "Stars_max": 3,
            "PP_min": 100,
            "PP_max": -3,
            "Accuracy_min": 5002184,
            "Accuracy_max": -30,
            "Rank_min": -10,
            "Country_Rank_max": -20
        },
        {
            "PP": (0, 100),
            "Accuracy": (0, 100),
            "Miss": (0, float("inf")),
            "Rank": (1, float("inf")),
            "Country_Rank": (1, 1),
            "Stars": (3, 6)
        }
    ),
])
def test_trimSpecsToRange(input1, expected):
    assert trimSpecsToRange(input1) == expected


# this test just WOULDNT work with parametrize and i'm so done with it so here it is with a list of cases
def test_Get_MultiPlaylistsSpec():
    testcases = [
        (
            [
                {
                    "Playlist_Name": "test1",
                    "Preset": "Default",
                    "Cover_Image": "imageName",
                    "Include_Perfect_Scores": True,
                    "Stars_min": 0,
                    "Stars_max": 13,
                    "PP_min": 0,
                    "PP_max": 1000,
                    "Accuracy_min": 0,
                    "Accuracy_max": 100,
                    "Miss_min": 0,
                    "Miss_max": 10000,
                    "Rank_min": 1,
                    "Rank_max": 999999,
                    "Country_Rank_min": 1,
                    "Country_Rank_max": 999999
                },
                {
                    "Playlist_Name": "test1.2",
                    "Stars_min": 1,
                    "Stars_max": 5,
                    "Accuracy_min": 0,
                    "Accuracy_max": 100,
                    "Rank_min": 1,
                    "Rank_max": 999999,
                    "Country_Rank_min": 1,
                    "Country_Rank_max": 4
                }
            ],
            {
                "test1":   {"Preset": "Default",
                            "Cover_Image": "imageName",
                            "Include_Perfect_Scores": True,
                            "Sort": "Recent_Desc",
                            "SpecsMinMax": [
                                {"PP": (0, 1000),
                                 "Accuracy": (0, 100),
                                 "Miss": (0, 10000),
                                 "Rank": (1, 999999),
                                 "Country_Rank": (1, 999999),
                                 "Stars": (0, 13)
                                 }
                            ]
                            },
                "test1.2":   {"Preset": "Default",
                              "Cover_Image": "Poupette.png",
                              "Include_Perfect_Scores": False,
                              "Sort": "Recent_Desc",
                              "SpecsMinMax": [
                                  {"PP": (0, float("inf")),
                                   "Accuracy": (0, 100),
                                   "Miss":  (0, float("inf")),
                                   "Rank": (1, 999999),
                                   "Country_Rank": (1, 4),
                                   "Stars": (1, 5)
                                   }
                              ]
                              }
            }
        ),
        (
            [
                {
                    "Playlist_Name": "test2",
                    "Preset": "Default",
                    "Cover_Image": "imageName",
                    "Include_Perfect_Scores": True,
                    "Stars_min": 0,
                    "Stars_max": 13,
                    "PP_min": 0,
                    "PP_max": 1000,
                    "Accuracy_min": 0,
                    "Accuracy_max": 100,
                    "Miss_min": 0,
                    "Miss_max": 10000,
                    "Rank_min": 1,
                    "Rank_max": 999999,
                    "Country_Rank_min": 1,
                    "Country_Rank_max": 999999
                },
                {
                    "Playlist_Name": "test2",
                    "Stars_min": 1,
                    "Stars_max": 5,
                    "Accuracy_min": 0,
                    "Accuracy_max": 100,
                    "Rank_min": 1,
                    "Rank_max": 999999,
                    "Country_Rank_min": 1,
                    "Country_Rank_max": 4
                }
            ],
            {
                "test2":   {"Preset": "Default",
                            "Cover_Image": "imageName",
                            "Include_Perfect_Scores": True,
                            "Sort": "Recent_Desc",
                            "SpecsMinMax": [
                                {"PP": (0, 1000),
                                 "Accuracy": (0, 100),
                                 "Miss": (0, 10000),
                                 "Rank": (1, 999999),
                                 "Country_Rank": (1, 999999),
                                 "Stars": (0, 13)
                                 },
                                {"PP": (0, float("inf")),
                                 "Accuracy": (0, 100),
                                 "Miss":  (0, float("inf")),
                                 "Rank": (1, 999999),
                                 "Country_Rank": (1, 4),
                                 "Stars": (1, 5)
                                 }
                            ]
                            }
            }
        ),
        (
            [
                {
                    "Playlist_Name": "test3",
                    "Preset": "Default",
                    "Include_Perfect_Scores": True,
                    "Stars_min": 0,
                    "Stars_max": 13,
                    "PP_min": 0,
                    "PP_max": 1000,
                    "Accuracy_min": 0,
                    "Accuracy_max": 100,
                    "Miss_min": 0,
                    "Miss_max": 10000,
                    "Rank_min": 1,
                    "Rank_max": 999999,
                    "Country_Rank_min": 1,
                    "Country_Rank_max": 999999
                },
                {
                    "Playlist_Name": "test3",
                    "Preset": "Default",
                    "Cover_Image": "imageName",
                    "Stars_min": 1,
                    "Stars_max": 5,
                    "Accuracy_min": 0,
                    "Accuracy_max": 100,
                    "Rank_min": 1,
                    "Rank_max": 999999,
                    "Country_Rank_min": 1,
                    "Country_Rank_max": 4
                }
            ],
            {
                "test3":   {"Preset": "Default",
                            "Cover_Image": "Poupette.png",
                            "Include_Perfect_Scores": True,
                            "Sort": "Recent_Desc",
                            "SpecsMinMax": [
                                {"PP": (0, 1000),
                                 "Accuracy": (0, 100),
                                 "Miss": (0, 10000),
                                 "Rank": (1, 999999),
                                 "Country_Rank": (1, 999999),
                                 "Stars": (0, 13)
                                 },
                                {"PP": (0, float("inf")),
                                 "Accuracy": (0, 100),
                                 "Miss":  (0, float("inf")),
                                 "Rank": (1, 999999),
                                 "Country_Rank": (1, 4),
                                 "Stars": (1, 5)
                                 }
                            ]
                            }
            }
        )
    ]
    if os.path.exists(PLAYLISTS_SPECS_FILE):
        original_content = load_JSONFile(PLAYLISTS_SPECS_FILE)
    else:
        original_content = []

    try:
        for idx, (input_data, expected) in enumerate(testcases):
            print(f"\n--- Running test case {idx + 1} ---")

            # ✅ On écrase le fichier avec le nouveau jeu de données
            dumpToJson(PLAYLISTS_SPECS_FILE, input_data)
            time.sleep(0.05)  # petite pause pour être sûr que le FS a fini

            # 🔍 Test réel
            result = Get_MultiPlaylistsSpec()
            print("Expected:", expected)
            print("Got     :", result)
            assert result == expected, f"FAILED at case {idx + 1}"

    finally:
        # 🔁 Restaurer le fichier original même en cas de fail
        dumpToJson(PLAYLISTS_SPECS_FILE, original_content)
