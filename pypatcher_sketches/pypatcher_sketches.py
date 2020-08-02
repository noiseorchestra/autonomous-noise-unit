# Code apadted from https://github.com/madwort/jacktrip_pypatcher

import jack
from itertools import product

jackClient = jack.Client('MadwortAutoPatcher')


def get_unique_port_names(jackClient, search_string):
    return list(set(map(lambda x: x.name.split(':')[0],
                    jackClient.get_ports(search_string))))


def get_grouped_port_list(jackClient, identifier):
    """Get an array of client mono & stereo jack ports"""
    # Get list  of jack ports grouped into singlets (mono) or pairs (stereo)
    # based on an identifier which would need to be unique to that class of port
    # could also make use of JACK-Client is_output=True search params

    search_string = '.*{}.*'.format(identifier)
    target_ports = jackClient.get_ports(search_string)
    unique_ports = get_unique_port_names(search_string)

    grouped_ports = []

    for port in target_ports:
        grouped_ports.append([port for port_name in unique_ports if port.name.startswith(port_name)])

    return grouped_ports

# This should give us things like (maybe the nested lists could be sets?):
#
# [[..ffff.192.168.0.1:receive_1, ..ffff.192.168.0.1:receive_2],
# [..ffff.192.168.0.2:receive_1],
# [..ffff.192.168.0.3:receive_1, ..ffff.192.168.0.3:receive_2]
# etc...]
#


"""SIMPLE MONO or STEREO SESSION / MAIN OUT"""

def disconnect_all(jackClient, receive_ports_list):
    # we may not need this if we go for only making new connections
    """disconnect everything from a port"""
    # iterate over all individual ports and get connections
    for receive_ports in (*receive_ports_list):
        for receive_port in receive_ports:
            send_ports = jackClient.get_all_connections(receive_port)

            for send_port in send_ports:
                jackClient.disconnect(receive_port, send_port)


def is_already_connected(jackClient, receive_port, send_port):
    """check if 2 ports are already connected"""

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

    # create all possible connections between receive_ports and send_ports.
    for connection in product(*receive_ports_list, *send_ports_list):

        # this should produce connection pairs like this:
        # [([stereo-receive-left, stereo-receive-right], [mono-send]),
        # [([mono-receive], [stereo-send-left, stereo-send-right]),
        # [([mono-receive], [mono-send])]

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


"""PANNED LADSPA SESSION"""

def is_already_connected_ladspa(jackClient, receive_port, ladspa_send_ports):
    """check if ports are already connected to ANY ladspa send"""
    connected = False
    connected_ports = jackClient.get_all_connections(receive_port)
    for connected_port in connected_ports:
        for ladspa_send_port in ladspa_send_ports:
            if ladspa_send_port.name == connected_port.name:
                connected = True
    return connected


def connect_ladspa(jackClient, receive_port, ladspa_send_port, ladspa_send_ports):
    """connect ports if not already connected"""
    for send_port in ladspa_send_ports:
        if not is_already_connected_ladspa(receive_port, ladspa_send_ports):
            jackClient.connect(receive_port, send_port)


def loop(ladspa_send_ports):
    """generator to loop through all ladspa send ports and return one at a time"""
    x = 0
    while True:
        yield ladspa_send_ports[x]
        x += 1 if x < len(ladspa_send_ports) else 0


def connect_all_to_ladspa(jackClient, receive_ports_list, ladspa_send_ports):
    """Connect all receive ports to list of ladspa send ports"""

    for receive_ports in receive_ports_list:
        ladspa_send_port = next(loop(ladspa_send_ports))
        for receive_port in (receive_ports):
            connect_ladspa(receive_port, ladspa_send_port, ladspa_send_ports)


# make lists of all ports we want to connect

jacktrip_client_receives = get_grouped_port_list(jackClient, 'receive')
jacktrip_client_sends = get_grouped_port_list(jackClient, 'send')
darkice_sends = jackClient.get_ports('.*darkice.*')
ladspa_sends = jackClient.get_ports('.*Input.*')
ladspa_receives = jackClient.get_ports('.*Output.*')

# make all mono / stereo connections
connect_all(jackClient, jacktrip_client_receives, [jacktrip_client_sends, darkice_sends])

# OR

# make all panned ladspa connections
connect_all_to_ladspa(jackClient, jacktrip_client_receives, ladspa_sends)

# then connect ladspa to all desired sends in stereo
# TO DO
# connect_from_ladspa(jackClient, ladspa_receives, [jacktrip_client_sends, darkice_sends])
