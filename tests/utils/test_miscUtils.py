import json
import pytest
from ppp.utils.miscUtils import *
from ppp.utils.paths import *
from pathlib import Path

# yes I put a lot of similar cases in my tests, but i like to be SURE that these basic functions FUNCTION, so i put in pretty much any case


@pytest.mark.parametrize("input1, input2, expected", [
    ("a", "b", "a"),
    (1, 2, 1),
    (None, "b", "b"),
    (None, 2, 2),
    (True, False, True),
    (False, True, False),
    (None, False, False),
])
def test_getOrElse(input1, input2, expected):
    assert getOrElse(input1, input2) == expected
    assert getOrElse("images", "2") != getOrElse("2", "images")


@pytest.mark.parametrize("input1, input2, input3, expected", [
    ({"a": 1, "b": 2, "c": 3}, "a", 3, 1),
    ({"a": 1, "b": 2}, "c", 3, 3),
    ({}, "c", 3, 3),

])
def test_ifExistsInDictOrElse(input1, input2, input3, expected):
    assert ifExistsInDictOrElse(input1, input2, input3) == expected
    # checks if default has been added
    assert ifExistsInDictOrElse(input1, "c", 5) == 3

    assert ifExistsInDictOrElse(input1, "c", 5) != 5


@pytest.mark.parametrize("input, expected", [
    (TESTJSONS_FILE, [{"aaa": "oui"}, {"bbb": "mdr non gros NOOB va",
                                       "ccc": False, "FF": 4, "zzz": 5.3855092264}]),
    ("testfile1", [{"aaa": "oui"}, {"bbb": "mdr non gros NOOB va",
                                    "ccc": False, "FF": 4, "zzz": 5.3855092264}]),
    ("testdir1/subfolder/petitzob.json", {"microzizi": "oui :("}),
    (TESTJSONS_DIR/"subfolder/petitzob.json", {"microzizi": "oui :("}),
    (TESTJSONS_SUBDIR/"petitzob.json", {"microzizi": "oui :("}),
])
def test_load_JSONFile(input, expected):
    assert load_JSONFile(input) == expected
    assert load_JSONFile(TESTJSONS_FILE) != load_JSONFile(TESTJSONS_SUBFILE)


@pytest.mark.parametrize("input1, input2, expected", [
    (TESTJSONS_DUMP, [{"aaa": "oui"}, {"bbb": "mdr non gros NOOB va",
                                       "ccc": False, "FF": 4, "zzz": 5.3855092264}], load_JSONFile(TESTJSONS_FILE)),
    (TESTJSONS_DIR/"dump.json", "a", "a"),
])
def test_dumpToJson(input1, input2, expected):
    dumpToJson(input1, input2)
    assert load_JSONFile(input1) == expected
    assert load_JSONFile(TESTJSONS_DUMP) != load_JSONFile(TESTJSONS_SUBFILE)


@pytest.mark.parametrize("input, expected", [
    (ROOT_DIR, ROOT_DIR),
    (ROOT_DIR/"config.json", CONFIG_FILE),
    (TESTJSONS_DIR/"subfolder", TESTJSONS_SUBDIR),
    (TESTJSONS_FILE, TESTJSONS_DIR/"zob.json"),
])
def test_pathAsSTRhandler(input, expected):
    assert pathAsSTRhandler(input) == expected
    assert pathAsSTRhandler("images") != pathAsSTRhandler("tests")


@pytest.mark.parametrize("input, expected", [
    ("root", ROOT_DIR),
    ("images", ROOT_DIR/"Images"),
    ("images", ROOT_DIR/"Images"),
    ("testdir1/subfolder", TESTJSONS_SUBDIR),
    ("testfile1", TESTJSONS_DIR/"zob.json"),
    ("testdir1/subfolder/petitzob.json", TESTJSONS_SUBFILE),
    ("tests/testJSONs/subfolder/petitzob.json", TESTJSONS_SUBFILE),
    ("tests/testJSONs/subfolder/petitzob.json", stringAliasToPath("testfile2")),
])
def test_stringAliasToPath(input, expected):
    assert stringAliasToPath(input) == expected
    assert stringAliasToPath("images") != stringAliasToPath("tests")


@pytest.mark.parametrize("input1, expected", [
    (
        {
            "Playlist_Name": "test1",
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


def test_update_last_refresh():
    playerdata = load_JSONFile(PLAYERDATA_FILE)
    dumpToJson(TESTJSONS_DUMP, playerdata)
    update_last_refresh()
    expecdate = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    expecstamp = int(datetime.now().timestamp())
    test = load_JSONFile(PLAYERDATA_FILE)
    dumpToJson(PLAYERDATA_FILE, load_JSONFile(TESTJSONS_DUMP))
    assert test["LASTUPDATE"] == expecdate
    assert test["LASTUPDATETIMESTAMP"] == expecstamp
