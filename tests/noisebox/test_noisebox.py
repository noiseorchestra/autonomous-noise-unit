from noisebox import Noisebox

noisebox = Noisebox(dry_run=True)

def test_get_session_params():
    assert noisebox.get_session_params()["ip"] == "111.111.111.111"
