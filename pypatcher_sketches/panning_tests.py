import panning_tests_setup as t
import pypatcher_sketches
import jack
from itertools import product

jackClient = jack.Client('MadwortAutoPatcher')
jackClient.activate()


def test_get_ladspa_send_ports():
    assert pypatcher_sketches.get_grouped_port_list(jackClient, 'Input') == t.ladspa_sends


def test_get_ladspa_receive_ports():
    assert pypatcher_sketches.get_grouped_port_list(jackClient, 'Output') == t.ladspa_receives


def test_connect_all_to_ladspa():
    assert pypatcher_sketches.connect_all(jackClient, t.jacktrip_receive_ports, t.ladspa_sends, withPanning=True) == t.ladspa_receive_connections


def test_connect_ladspa_to_all():
    assert pypatcher_sketches.connect_all(jackClient, t.ladspa_receives, t.jacktrip_send_ports) == t.ladspa_send_connections
