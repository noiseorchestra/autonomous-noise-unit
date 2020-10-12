import noisebox_helpers as nh
import pytest

jack_helper = nh.jack_helper.JackHelper()

local_receive_ports = ["system:capture_1", "system:capture_2"]

def test_check_input_ports():
    with pytest.raises(nh.NoiseBoxCustomError):
        assert jack_helper.check_input_ports([], stereo=True) == []
    assert jack_helper.check_input_ports(local_receive_ports, stereo=True) == local_receive_ports
    assert jack_helper.check_input_ports(local_receive_ports, stereo=False) == [local_receive_ports[0]]

def test_set_all_connections_monitoring_stereo_stereo():
    receive_ports_list = [
        ["system:capture_01", "system:capture_02"]
    ]
    send_ports_list = [
        ["system:playback_01", "system:playback_02"]
    ]
    jack_helper.set_all_connections(receive_ports_list, send_ports_list)
    assert jack_helper.connections == [('system:capture_01', 'system:playback_01'),
                                       ('system:capture_02', 'system:playback_02')]

def test_set_all_connections_monitoring_mono_stereo():
    receive_ports_list = [
        ["system:capture_01"]
    ]
    send_ports_list = [
        ["system:playback_01", "system:playback_02"]
    ]
    jack_helper.set_all_connections(receive_ports_list, send_ports_list)
    assert jack_helper.connections == [('system:capture_01', 'system:playback_01'),
                                       ('system:capture_01', 'system:playback_02')]

def test_set_all_connections_monitoring_mono_mono():
    receive_ports_list = [
        ["system:capture_01"]
    ]
    send_ports_list = [
        ["system:playback_01"]
    ]
    jack_helper.set_all_connections(receive_ports_list, send_ports_list)
    assert jack_helper.connections == [('system:capture_01', 'system:playback_01')]
