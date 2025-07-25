from pathlib import Path
import sys


# Aliases to eaily use the paths are written above each of them
# The aliases are set above load_JSONFile(name), in ConfigHandler.py

# "root", "ppp"
if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent
    PPP_DIR = Path(sys._MEIPASS) / "ppp"
else:
    ROOT_DIR = Path(__file__).resolve().parents[2]
    PPP_DIR = ROOT_DIR / "ppp"

# "data"
DATA_DIR = ROOT_DIR / ".poupetteData"

# "defaultImages"
DEFAULTIMAGES_DIR = PPP_DIR / "defaultImages"

# "images"
IMAGES_DIR = ROOT_DIR / "Images"

# "results"
RESULTS_DIR = ROOT_DIR / "Results"

# "playlists"
PLAYLISTS_DIR = RESULTS_DIR/"Playlists"

# "csv"
CSV_DIR = RESULTS_DIR/"CSV"


# "config"
CONFIG_FILE = ROOT_DIR / "config.json"

# "spec"
PLAYLIST_SPECS_FILE = ROOT_DIR / "PlaylistSpecs.json"

# "specs"
PLAYLISTS_SPECS_FILE = ROOT_DIR / "PlaylistsSpecs.json"

# "playerData"
PLAYERDATA_FILE = DATA_DIR / "PlayerData.json"

# "SSRankedMaps"
SCORESABER_RANKEDMAPS_FILE = DATA_DIR / "ScoresaberRankedMaps.csv"


#


#


# these paths are for testing purposes

# testdir1
TESTJSONS_DIR = ROOT_DIR/"tests/testJSONs"

# testdir2
TESTJSONS_SUBDIR = TESTJSONS_DIR/"subfolder"

# testfile1
TESTJSONS_FILE = TESTJSONS_DIR/"zob.json"

# testfile2
TESTJSONS_SUBFILE = TESTJSONS_SUBDIR/"petitzob.json"

TESTJSONS_DUMP = TESTJSONS_DIR/"dump.json"
