import pypatcher_sketches
import jack
from itertools import product

# SETUP

client_1_stereo = jack.Client('client_1_stereo')
client_2_stereo = jack.Client('client_2_stereo')
client_3_mono = jack.Client('client_3_mono')
client_4_stereo = jack.Client('client_4_stereo')
client_5_mono = jack.Client('client_5_mono')
client_6_stereo = jack.Client('client_6_stereo')

client_1_stereo.activate()
client_2_stereo.activate()
client_3_mono.activate()
client_4_stereo.activate()
client_5_mono.activate()
client_6_stereo.activate()

client_1_stereo.outports.register("receive_1")
client_1_stereo.outports.register("receive_2")
client_2_stereo.outports.register("receive_1")
client_2_stereo.outports.register("receive_2")
client_3_mono.outports.register("receive_1")
client_4_stereo.outports.register("receive_1")
client_4_stereo.outports.register("receive_2")
client_5_mono.outports.register("receive_1")
client_6_stereo.outports.register("receive_1")
client_6_stereo.outports.register("receive_2")

client_1_stereo.inports.register("send_1")
client_1_stereo.inports.register("send_2")
client_2_stereo.inports.register("send_1")
client_2_stereo.inports.register("send_2")
client_3_mono.inports.register("send_1")
client_4_stereo.inports.register("send_1")
client_4_stereo.inports.register("send_2")
client_5_mono.inports.register("send_1")
client_6_stereo.inports.register("send_1")
client_6_stereo.inports.register("send_2")

jackClient = jack.Client('MadwortAutoPatcher')
jackClient.activate()

all_port_names = ["client_1_stereo:receive_1", "client_1_stereo:receive_2",
                  "client_2_stereo:receive_1", "client_2_stereo:receive_2",
                  "client_3_mono:receive_1", "client_4_stereo:receive_1",
                  "client_4_stereo:receive_2", "client_5_mono:receive_1",
                  "client_6_stereo:receive_1", "client_6_stereo:receive_2",
                  "client_1_stereo:send_1", "client_1_stereo:send_2",
                  "client_2_stereo:send_1", "client_2_stereo:send_2",
                  "client_3_mono:send_1", "client_4_stereo:send_1",
                  "client_4_stereo:send_2", "client_5_mono:send_1",
                  "client_6_stereo:send_1", "client_6_stereo:send_2"]

unique_port_names = ["client_1_stereo",
                     "client_2_stereo",
                     "client_3_mono",
                     "client_4_stereo",
                     "client_5_mono",
                     "client_6_stereo"]

grouped_receive_ports = [
    ["client_1_stereo:receive_1", "client_1_stereo:receive_2"],
    ["client_2_stereo:receive_1", "client_2_stereo:receive_2"],
    ["client_3_mono:receive_1"], ["client_4_stereo:receive_1",
    "client_4_stereo:receive_2"], ["client_5_mono:receive_1"],
    ["client_6_stereo:receive_1", "client_6_stereo:receive_2"]
]

grouped_send_ports = [["client_1_stereo:send_1", "client_1_stereo:send_2"],
                      ["client_2_stereo:send_1", "client_2_stereo:send_2"],
                      ["client_3_mono:send_1"], ["client_4_stereo:send_1",
                      "client_4_stereo:send_2"], ["client_5_mono:send_1"],
                      ["client_6_stereo:send_1", "client_6_stereo:send_2"]]


all_fake_connections = [
    (['client_1_stereo:receive_1', 'client_1_stereo:receive_2'],
        ['client_2_stereo:send_1', 'client_2_stereo:send_2']),
    (['client_1_stereo:receive_1', 'client_1_stereo:receive_2'],
        ['client_3_mono:send_1']),
    (['client_1_stereo:receive_1', 'client_1_stereo:receive_2'],
        ['client_4_stereo:send_1', 'client_4_stereo:send_2']),
    (['client_1_stereo:receive_1', 'client_1_stereo:receive_2'],
        ['client_5_mono:send_1']),
    (['client_1_stereo:receive_1', 'client_1_stereo:receive_2'],
        ['client_6_stereo:send_1', 'client_6_stereo:send_2']),
    (['client_2_stereo:receive_1', 'client_2_stereo:receive_2'],
        ['client_1_stereo:send_1', 'client_1_stereo:send_2']),
    (['client_2_stereo:receive_1', 'client_2_stereo:receive_2'],
        ['client_3_mono:send_1']),
    (['client_2_stereo:receive_1', 'client_2_stereo:receive_2'],
        ['client_4_stereo:send_1', 'client_4_stereo:send_2']),
    (['client_2_stereo:receive_1', 'client_2_stereo:receive_2'],
        ['client_5_mono:send_1']),
    (['client_2_stereo:receive_1', 'client_2_stereo:receive_2'],
        ['client_6_stereo:send_1', 'client_6_stereo:send_2']),
    (['client_3_mono:receive_1'],
        ['client_1_stereo:send_1', 'client_1_stereo:send_2']),
    (['client_3_mono:receive_1'],
        ['client_2_stereo:send_1', 'client_2_stereo:send_2']),
    (['client_3_mono:receive_1'],
        ['client_4_stereo:send_1', 'client_4_stereo:send_2']),
    (['client_3_mono:receive_1'],
        ['client_5_mono:send_1']),
    (['client_3_mono:receive_1'],
        ['client_6_stereo:send_1', 'client_6_stereo:send_2']),
    (['client_4_stereo:receive_1', 'client_4_stereo:receive_2'],
        ['client_1_stereo:send_1', 'client_1_stereo:send_2']),
    (['client_4_stereo:receive_1', 'client_4_stereo:receive_2'],
        ['client_2_stereo:send_1', 'client_2_stereo:send_2']),
    (['client_4_stereo:receive_1', 'client_4_stereo:receive_2'],
        ['client_3_mono:send_1']),
    (['client_4_stereo:receive_1', 'client_4_stereo:receive_2'],
        ['client_5_mono:send_1']),
    (['client_4_stereo:receive_1', 'client_4_stereo:receive_2'],
        ['client_6_stereo:send_1', 'client_6_stereo:send_2']),
    (['client_5_mono:receive_1'],
        ['client_1_stereo:send_1', 'client_1_stereo:send_2']),
    (['client_5_mono:receive_1'],
        ['client_2_stereo:send_1', 'client_2_stereo:send_2']),
    (['client_5_mono:receive_1'],
        ['client_3_mono:send_1']),
    (['client_5_mono:receive_1'],
        ['client_4_stereo:send_1', 'client_4_stereo:send_2']),
    (['client_5_mono:receive_1'],
        ['client_6_stereo:send_1', 'client_6_stereo:send_2']),
    (['client_6_stereo:receive_1', 'client_6_stereo:receive_2'],
        ['client_1_stereo:send_1', 'client_1_stereo:send_2']),
    (['client_6_stereo:receive_1', 'client_6_stereo:receive_2'],
        ['client_2_stereo:send_1', 'client_2_stereo:send_2']),
    (['client_6_stereo:receive_1', 'client_6_stereo:receive_2'],
        ['client_3_mono:send_1']),
    (['client_6_stereo:receive_1', 'client_6_stereo:receive_2'],
        ['client_4_stereo:send_1', 'client_4_stereo:send_2']),
    (['client_6_stereo:receive_1', 'client_6_stereo:receive_2'],
        ['client_5_mono:send_1'])
]

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

# TESTS


def test_get_all_fake_ports():
    assert get_all_fake_ports(jackClient) == all_port_names


def test_get_unique_client():
    all_clients = jackClient.get_ports(".*receive.*")
    assert pypatcher_sketches.get_unique_port_names(all_clients) == unique_port_names


def test_get_grouped_receive_ports():
    assert pypatcher_sketches.get_grouped_port_list(jackClient, 'receive') == grouped_receive_ports


def test_get_grouped_send_ports():
    assert pypatcher_sketches.get_grouped_port_list(jackClient, 'send') == grouped_send_ports


def test_connect_all():
    print(all_fake_connections)
    assert pypatcher_sketches.connect_all(jackClient, grouped_receive_ports, grouped_send_ports) == all_fake_connections
