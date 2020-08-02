# Code apadted from https://github.com/madwort/jacktrip_pypatcher

import jack
from itertools import product

jackClient = jack.Client('MadwortAutoPatcher')


def get_unique_port_names(jackClient, search_string):
    return list(set(map(lambda x: x.name.split(':')[0],
                    jackClient.get_ports(search_string))))

# Get list  of jack ports grouped into singlets (mono) or pairs (stereo)


def get_grouped_port_list(jackClient, identifier):
    """Get an array of client mono & stereo jack ports"""

    search_string = '.*{}.*'.format(identifier)
    target_ports = jackClient.get_ports(search_string)
    unique_ports = get_unique_port_names(search_string)

    grouped_ports = []

    for port in target_ports:
        grouped_ports.append([port for port_name in unique_ports if port.name.startswith(port_name)])

    return grouped_ports

# This would give us something like:
# [[..ffff.192.168.0.1:receive_1, ..ffff.192.168.0.1:receive_2],
# [..ffff.192.168.0.2:receive_1],
# [..ffff.192.168.0.3:receive_1, ..ffff.192.168.0.3:receive_2]
# etc...]


def disconnect_all(jackClient, receive_ports_list):
    """disconnect everything from a port"""
    # iterate over all individual ports and get connections
    for receive_ports in (*receive_ports_list):
        for receive_port in receive_ports:
            send_ports = jackClient.get_all_connections(receive_port)

            for send_port in send_ports:
                jackClient.disconnect(receive_port, send_port)


def is_already_connected(jackClient, receive_port, send_port):
    """check if ports are already connected"""

    connected_ports = jackClient.get_all_connections(receive_port)
    for connected_port in connected_ports:
        if send_port.name == connected_port.name:
            return True
    return False


def connect(jackClient, receive_port, send_port):
    """connect ports if not already connected"""
    if not is_already_connected(receive_port, send_port):
        jackClient.connect(receive_port, send_port)


def connect_all(jackClient, receive_ports_list, send_ports_list):
    """Connect all receive  port to list of send ports"""

    # create all possible connections between receive_ports and send_ports
    # this function could be expanded a lot to deal with ladspa panning
    # or adapted to compare against a list of existing connections and only
    # make new connections.
    for connection in product(*receive_ports_list, *send_ports_list):

        receive_ports = connection[0]
        send_ports = connection[1]
        # don't connect a port to itself
        if receive_ports[0].name.split(':')[0] == send_ports[0].name.split(':')[0]:
            continue

        # Make connections depending on stereo or mono clients
        receive_stereo = True if len(receive_ports) == 2 else False
        send_stereo = True if len(send_ports) == 2 else False
        if receive_stereo and send_stereo:
            connect(receive_ports[0], send_ports[0])
            connect(receive_ports[1], send_ports[1])
        if receive_stereo and not send_stereo:
            connect(receive_ports[0], send_ports[0])
            connect(receive_ports[1], send_ports[0])
        if not receive_stereo and not send_stereo:
            connect(receive_ports[0], send_ports[0])

# make lists of all connections we want to connect


jacktrip_client_receives = get_grouped_port_list(jackClient, 'receive')
jacktrip_client_sends = get_grouped_port_list(jackClient, 'send')
darkice_sends = get_grouped_port_list(jackClient, 'darkice')

# disconnect all existing connections
# not clear what happens to connections on a port when it unregisters
# if they just cleanly disappear that would be nice....

# disconnect_all(jackClient, jacktrip_client_receives)

# make new connections
connect_all(jackClient, jacktrip_client_receives, [jacktrip_client_sends, darkice_sends])
