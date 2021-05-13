from noisebox import Noisebox
from unittest.mock import Mock
import noisebox_helpers as nh
import pytest


def test_get_session_params():
    noisebox = Noisebox(dry_run=True)
    assert noisebox.get_session_params()["ip"] == "111.111.111.111"

def test_check_peers():
    noisebox = Noisebox(dry_run=True)
    noisebox.nh = Mock()
    noisebox.check_peers()
    noisebox.nh.get_online_peers.assert_called_with(['pi@raspberry.myvpn', 'pi@raspberry.myvpn', '111.111.111.111'])

def test_start_level_meters():
    noisebox = Noisebox(dry_run=True)
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
    noisebox.is_stereo_input = Mock()
    noisebox.oled = Mock()
    noisebox.jack_helper = Mock()
    noisebox.jack_helper.get_inputs.side_effect = get_inputs
    noisebox.is_stereo_input.side_effect = [False, True, True]
    noisebox.start_level_meters()
    assert noisebox.level_meters == [('system:capture_01', 'IN-1')]
    noisebox.start_level_meters()
    assert noisebox.level_meters == [('system:capture_01', 'IN-1'), ('system:capture_02', 'IN-2')]
    noisebox.nh.LevelMeter.side_effect = nh.NoiseBoxCustomError
    with pytest.raises(nh.NoiseBoxCustomError):
        noisebox.start_level_meters()

def test_start_local_monitoring():
    noisebox = Noisebox(dry_run=True)
    noisebox.start_level_meters = Mock()
    noisebox.jack_helper = Mock()
    noisebox.start_local_monitoring()
    noisebox.start_level_meters.assert_called_with()
    noisebox.jack_helper.make_monitoring_connections.assert_called_with(True)

def test_start_jacktrip_monitoring():
    noisebox = Noisebox(dry_run=True)
    noisebox.start_level_meters = Mock()
    noisebox.jack_helper = Mock()
    noisebox.start_jacktrip_monitoring()
    noisebox.start_level_meters.assert_called_with(jacktrip_session=True)
    noisebox.jack_helper.make_jacktrip_connections.assert_called_with(True)

def test_restart_jack_if_needed():
    noisebox = Noisebox(dry_run=True)
    noisebox.jack_helper = nh.JackHelper()
    noisebox.jack_helper.start = Mock()
    noisebox.oled = Mock()
    noisebox.jack_helper.current_fpp = "256"
    noisebox.restart_jack_if_needed()
    assert not noisebox.jack_helper.start.called

    noisebox.jack_helper.current_fpp = "64"
    noisebox.jack_helper.start = Mock()
    noisebox.restart_jack_if_needed()
    noisebox.jack_helper.start.assert_called()
