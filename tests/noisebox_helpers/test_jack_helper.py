import noisebox_helpers as nh
import pytest

jack_helper = nh.jack_helper.JackHelper()

local_receive_ports = ["system:capture_1", "system:capture_2"]

def test_process_meter_value():
    with pytest.raises(nh.NoiseBoxCustomError):
        assert jack_helper.check_input_ports([], stereo=True) == []
    assert jack_helper.check_input_ports(local_receive_ports, stereo=True) == local_receive_ports
    assert jack_helper.check_input_ports(local_receive_ports, stereo=False) == [local_receive_ports[0]]
