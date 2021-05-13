import noisebox_helpers as nh
import pytest
from unittest.mock import Mock

jack_helper = nh.jack_helper.JackHelper()

local_receive_ports = ["system:capture_1", "system:capture_2"]

system_capture_01 = Mock()
system_capture_01.name = "system:capture_01"
system_capture_02 = Mock()
system_capture_02.name = "system:capture_02"
system_playback_01 = Mock()
system_playback_01.name = "system:playback_01"
system_playback_02 = Mock()
system_playback_02.name = "system:playback_02"
jacktrip_send_01 = Mock()
jacktrip_send_01.name = "jactrip:send_01"
jacktrip_send_02 = Mock()
jacktrip_send_02.name = "jactrip:send_02"

system_capture_mono = [Mock()]

dummy_cfg_with_fpp = {
    "jacktrip-default": {
        "ip": "123.123.123.123",
        "hub_mode": True,
        "server": False,
        "jacktrip-channels": "2",
        "input-channels": "2",
        "jacktrip-q": "6",
        "jack-fpp": "128"

    }
}

dummy_cfg_without_fpp = {
    "jacktrip-default": {
        "ip": "123.123.123.123",
        "hub_mode": True,
        "server": False,
        "jacktrip-channels": "2",
        "input-channels": "2",
        "jacktrip-q": "6"

    }
}

def test_check_current_fpp():
    jack_helper = nh.JackHelper()
    jack_helper.current_fpp = "256"
    assert jack_helper.check_current_fpp("128") == False
    assert jack_helper.check_current_fpp("256") == True

def test_generate_command():
    jack_helper = nh.JackHelper()
    result = ['jackd', '-R', '-dalsa', '-r48000', "-p256", '-n2', '-s', '-S']
    assert jack_helper.generate_command(dummy_cfg_without_fpp["jacktrip-default"]) == result
    result = ['jackd', '-R', '-dalsa', '-r48000', "-p128", '-n2', '-s', '-S']
    assert jack_helper.generate_command(dummy_cfg_with_fpp["jacktrip-default"]) == result


def test_check_input_ports():
    with pytest.raises(nh.NoiseBoxCustomError):
        assert jack_helper.check_input_ports([], stereo=True) == []
    assert jack_helper.check_input_ports(local_receive_ports, stereo=True) == local_receive_ports
    assert jack_helper.check_input_ports(local_receive_ports, stereo=False) == [local_receive_ports[0]]

def test_set_all_connections_monitoring_stereo_stereo():
    receive_ports_list = [
        [system_capture_01, system_capture_02]
    ]
    send_ports_list = [
        [system_playback_01, system_playback_02]
    ]
    jack_helper.connections = []
    jack_helper.set_all_connections(receive_ports_list, send_ports_list)
    assert jack_helper.connections == [(system_capture_01, system_playback_01),
                                       (system_capture_02, system_playback_02)]

def test_set_all_connections_monitoring_mono_stereo():
    receive_ports_list = [
        [system_capture_01]
    ]
    send_ports_list = [
        [system_playback_01, system_playback_02]
    ]
    jack_helper.connections = []
    jack_helper.set_all_connections(receive_ports_list, send_ports_list)
    assert jack_helper.connections == [(system_capture_01, system_playback_01),
                                       (system_capture_01, system_playback_02)]

def test_set_all_connections_monitoring_mono_mono():
    receive_ports_list = [
        [system_capture_01]
    ]
    send_ports_list = [
        [system_playback_01]
    ]
    jack_helper.connections = []
    jack_helper.set_all_connections(receive_ports_list, send_ports_list)
    assert jack_helper.connections == [(system_capture_01, system_playback_01)]

def test_set_all_connections_monitoring_stereo_mono():
    receive_ports_list = [
        [system_capture_01, system_capture_02]
    ]
    send_ports_list = [
        [system_playback_01]
    ]
    jack_helper.connections = []
    jack_helper.set_all_connections(receive_ports_list, send_ports_list)
    assert jack_helper.connections == [(system_capture_01, system_playback_01),
                                       (system_capture_02, system_playback_01)]

def test_set_all_connections_session_mono_mono():
    receive_ports_list = [
        [system_capture_01]
    ]
    send_ports_list = [
        [system_playback_01],
        [jacktrip_send_01],
    ]
    jack_helper.connections = []
    jack_helper.set_all_connections(receive_ports_list, send_ports_list)
    assert jack_helper.connections == [(system_capture_01, system_playback_01),
                                       (system_capture_01, jacktrip_send_01)]

def test_set_all_connections_session_mono_stereo():
    receive_ports_list = [
        [system_capture_01]
    ]
    send_ports_list = [
        [system_playback_01, system_playback_02],
        [jacktrip_send_01, jacktrip_send_02],
    ]
    jack_helper.connections = []
    jack_helper.set_all_connections(receive_ports_list, send_ports_list)
    assert jack_helper.connections == [(system_capture_01, system_playback_01),
                                       (system_capture_01, system_playback_02),
                                       (system_capture_01, jacktrip_send_01),
                                       (system_capture_01, jacktrip_send_02)]

def test_set_all_connections_session_stereo_stereo():
    receive_ports_list = [
        [system_capture_01, system_capture_02]
    ]
    send_ports_list = [
        [system_playback_01, system_playback_02],
        [jacktrip_send_01, jacktrip_send_02],
    ]
    jack_helper.connections = []
    jack_helper.set_all_connections(receive_ports_list, send_ports_list)
    assert jack_helper.connections == [(system_capture_01, system_playback_01),
                                       (system_capture_02, system_playback_02),
                                       (system_capture_01, jacktrip_send_01),
                                       (system_capture_02, jacktrip_send_02)]

def test_set_all_connections_session_stereo_mono():
    receive_ports_list = [
        [system_capture_01, system_capture_02]
    ]
    send_ports_list = [
        [system_playback_01],
        [jacktrip_send_01],
    ]
    jack_helper.connections = []
    jack_helper.set_all_connections(receive_ports_list, send_ports_list)
    assert jack_helper.connections == [(system_capture_01, system_playback_01),
                                       (system_capture_02, system_playback_01),
                                       (system_capture_01, jacktrip_send_01),
                                       (system_capture_02, jacktrip_send_01)]
