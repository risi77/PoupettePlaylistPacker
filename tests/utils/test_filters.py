import json
import pytest
from pathlib import Path
from ppp.utils.filters import *
from ppp.utils.paths import *


@pytest.mark.parametrize("input, expected", [
    ([{"leaderboard": {"ranked": True, "zob": False, "num": 1}},
      {"leaderboard": {"ranked": False, "zob": False,  "num": 47}},
        {"leaderboard": {"ranked": True, "zob": False, "num": 2}},
        {"leaderboard": {"ranked": False, "zob": True, "num": 42}},
        {"leaderboard": {"ranked": True, "zob": True,  "num": 3}}], [1, 2, 3]),
])
def test_filter_ranked(input, expected):
    list = []
    res = filter_ranked(input)
    for score in res:
        list.append(score["leaderboard"]["num"])
    assert list == expected
    assert list != [1, 3]
