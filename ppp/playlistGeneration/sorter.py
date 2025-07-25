import time
from ppp.utils.paths import *
from ppp.utils.miscUtils import *


def sort_scores(scores, sort_key: str):
    if not scores or not sort_key:
        return scores

    if "_" in sort_key:
        key, order = sort_key.rsplit("_", 1)
        reverse = order.lower() == "desc"
    else:
        key = sort_key
        reverse = False

    if scores:
        key_lower = key.lower()
        for k in scores[0].keys():
            if k.lower() == key_lower:
                key = k
                break

    def sort_func(score):
        if key.lower() == "recent":
            return score.get("timestamp", 0)
        return score.get(key, float('-inf') if reverse else float('inf'))

    return sorted(scores, key=sort_func, reverse=reverse)
