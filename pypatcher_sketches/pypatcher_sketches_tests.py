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
    ["client_3_mono:receive_1"],
    ["client_4_stereo:receive_1", "client_4_stereo:receive_2"],
    ["client_5_mono:receive_1"],
    ["client_6_stereo:receive_1", "client_6_stereo:receive_2"]]

grouped_send_ports = [
    ["client_1_stereo:send_1", "client_1_stereo:send_2"],
    ["client_2_stereo:send_1", "client_2_stereo:send_2"],
    ["client_3_mono:send_1"],
    ["client_4_stereo:send_1", "client_4_stereo:send_2"],
    ["client_5_mono:send_1"],
    ["client_6_stereo:send_1", "client_6_stereo:send_2"]]


all_connections = [
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
        ['client_5_mono:send_1'])]


ladspa_client_1 = jack.Client('left-65')
ladspa_client_2 = jack.Client('left-30')
ladspa_client_3 = jack.Client('right-30')
ladspa_client_4 = jack.Client('right-65')

ladspa_client_1.activate()
ladspa_client_2.activate()
ladspa_client_3.activate()
ladspa_client_4.activate()

ladspa_client_1.outports.register('Output (Left)')
ladspa_client_2.outports.register('Output (Left)')
ladspa_client_3.outports.register('Output (Right)')
ladspa_client_4.outports.register('Output (Right)')

ladspa_client_1.inports.register('Input (Left)')
ladspa_client_2.inports.register('Input (Left)')
ladspa_client_3.inports.register('Input (Right)')
ladspa_client_4.inports.register('Input (Right)')

ladspa_sends = [
    'left-65:Input (Left)',
    'left-30:Input (Left)',
    'right-30:Input (Right)',
    'right-65:Input (Right)']

ladspa_receives = [
    'left-65:Output (Left)',
    'left-30:Output (Left)',
    'right-30:Output (Right)',
    'right-65:Output (Right)']

ladspa_receive_connections = [
    (['client_1_stereo:receive_1', 'client_1_stereo:receive_2'],
        ['left-65:Input (Left)']),
    (['client_2_stereo:receive_1', 'client_2_stereo:receive_2'],
        ['left-30:Input (Left)']),
    (['client_3_mono:receive_1'],
        ['right-30:Input (Right)']),
    (['client_4_stereo:receive_1', 'client_4_stereo:receive_2'],
        ['right-65:Input (Right)']),
    (['client_5_mono:receive_1'],
        ['left-65:Input (Left)']),
    (['client_6_stereo:receive_1', 'client_6_stereo:receive_2'],
        ['left-30:Input (Left)'])]

ladspa_send_connections = [
    (['left-30:Output (Left)', 'right-30:Output (Right)'],
        ['client_1_stereo:send_1', 'client_1_stereo:send_2']),
    (['left-30:Output (Left)', 'right-30:Output (Right)'],
        ['client_2_stereo:send_1', 'client_2_stereo:send_2']),
    (['left-30:Output (Left)', 'right-30:Output (Right)'],
        ['client_3_mono:send_1']),
    (['left-30:Output (Left)', 'right-30:Output (Right)'],
        ['client_4_stereo:send_1', 'client_4_stereo:send_2']),
    (['left-30:Output (Left)', 'right-30:Output (Right)'],
        ['client_5_mono:send_1']),
    (['left-30:Output (Left)', 'right-30:Output (Right)'],
        ['client_6_stereo:send_1', 'client_6_stereo:send_2']),
    (['left-65:Output (Left)', 'right-65:Output (Right)'],
        ['client_1_stereo:send_1', 'client_1_stereo:send_2']),
    (['left-65:Output (Left)', 'right-65:Output (Right)'],
        ['client_2_stereo:send_1', 'client_2_stereo:send_2']),
    (['left-65:Output (Left)', 'right-65:Output (Right)'],
        ['client_3_mono:send_1']),
    (['left-65:Output (Left)', 'right-65:Output (Right)'],
        ['client_4_stereo:send_1', 'client_4_stereo:send_2']),
    (['left-65:Output (Left)', 'right-65:Output (Right)'],
        ['client_5_mono:send_1']),
    (['left-65:Output (Left)', 'right-65:Output (Right)'],
        ['client_6_stereo:send_1', 'client_6_stereo:send_2'])]



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
    assert pypatcher_sketches.connect_all(jackClient, grouped_receive_ports, grouped_send_ports) == all_connections


def test_get_ladspa_ports():
    assert pypatcher_sketches.get_ladspa_ports(jackClient, 'Input') == ladspa_sends
    assert pypatcher_sketches.get_ladspa_ports(jackClient, 'Output') == ladspa_receives


def test_connect_all_to_ladspa():
    assert pypatcher_sketches.connect_all_to_ladspa(jackClient, grouped_receive_ports, ladspa_sends) == ladspa_receive_connections


def test_connect_from_ladspa():
    grouped_ladspa_ports = pypatcher_sketches.get_grouped_ladspa_ports(jackClient, 'Output')
    all_client_sends = pypatcher_sketches.get_grouped_port_list(jackClient, 'send')
    assert pypatcher_sketches.connect_all(jackClient, grouped_ladspa_ports, all_client_sends) == ladspa_send_connections
