from noisebox import Noisebox
from unittest.mock import Mock
import noisebox_helpers as nh
import pytest

noisebox = Noisebox(dry_run=True)

def test_get_session_params():
    assert noisebox.get_session_params()["ip"] == "111.111.111.111"

def test_check_peers():
    noisebox.nh = Mock()
    noisebox.check_peers()
    noisebox.nh.get_online_peers.assert_called_with(['pi@raspberry.myvpn', 'pi@raspberry.myvpn'])

def test_start_level_meters():
    system_capture_01 = Mock()
    system_capture_01.name = "system:capture_01"
    system_capture_02 = Mock()
    system_capture_02.name = "system:capture_02"

    jacktrip_receive_01 = Mock()
    jacktrip_receive_01.name = "jactrip:receive_01"
    jacktrip_receive_02 = Mock()
    jacktrip_receive_02.name = "jactrip:receive_02"

    def level_meters(port_name, channel):
        return port_name, channel

    def get_inputs(stereo):
        if stereo is True:
            return [system_capture_01, system_capture_02]
        return [system_capture_01]

    noisebox.nh = Mock()
    noisebox.nh.NoiseBoxCustomError = nh.NoiseBoxCustomError
    noisebox.nh.LevelMeter = Mock()
    noisebox.nh.LevelMeter.side_effect = level_meters
    noisebox.oled = Mock()
    noisebox.jack_helper = Mock()
    noisebox.jack_helper.get_inputs.side_effect = get_inputs
    noisebox.start_level_meters()
    assert noisebox.level_meters == [('system:capture_01', 'IN-1')]
    noisebox.start_level_meters(stereo_input=(True))
    assert noisebox.level_meters == [('system:capture_01', 'IN-1'), ('system:capture_02', 'IN-2')]
    noisebox.nh.LevelMeter.side_effect = nh.NoiseBoxCustomError
    with pytest.raises(nh.NoiseBoxCustomError):
        noisebox.start_level_meters()
