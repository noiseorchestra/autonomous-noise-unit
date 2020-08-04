import pypatcher_sketches
import jacktrip_p2p_tests_setup as t
import jack
from itertools import product

jackClient = jack.Client('MadwortAutoPatcher')
jackClient.activate()

# SETUP

# for later randomised testing

# all_fake_clients = [client_1, client_2, client_3, client_4, client_5, client_6]

# for fake_client in all_fake_clients:
#     channels = random.randint(1, 2)
#     for i in channels:
#         fake_client.inports.register("receive_{i}")
#         fake_client.outports.register("receive_{i}")


def get_all_fake_ports(jackClient):

    all_ports = []

    client_ports = jackClient.get_ports(".*client.*")
    for port in client_ports:
        all_ports.append(port.name)
    print(all_ports)
    return all_ports


def test_get_all_fake_ports():
    assert get_all_fake_ports(jackClient) == t.all_port_names


def test_get_unique_client():
    all_clients = jackClient.get_ports(".*receive.*")
    assert pypatcher_sketches.get_unique_port_names(all_clients) == t.unique_port_names


def test_get_jacktrip_receive_ports():
    assert pypatcher_sketches.get_grouped_port_list(jackClient, 'receive') == t.jacktrip_receive_ports


def test_get_jacktrip_send_ports():
    assert pypatcher_sketches.get_grouped_port_list(jackClient, 'send') == t.jacktrip_send_ports


def test_connect_all():
    assert pypatcher_sketches.connect_all(jackClient, t.jacktrip_receive_ports, t.jacktrip_send_ports) == t.all_connections
