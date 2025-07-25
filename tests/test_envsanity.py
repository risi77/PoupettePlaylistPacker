# chatgpt wrote this

def test_basic_import():
    try:
        import ppp.utils.miscUtils
        assert True
    except ImportError as e:
        print(f"ImportError: {e}")
        assert False, "L'import utils.configHandler a échoué"


def test_pythonpath_effect():
    import os
    pythonpath = os.environ.get("PYTHONPATH", "")
    assert "." in pythonpath or os.getcwd(
    ) in pythonpath, f"Le PYTHONPATH ne contient pas le dossier courant. PYTHONPATH : {pythonpath}"
