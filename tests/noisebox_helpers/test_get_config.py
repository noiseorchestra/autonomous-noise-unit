import noisebox_helpers as nh

combined_config = {
    'jacktrip-default': {
        'hub_mode': 'True',
        'input-channels': '2',
        'ip': '111.111.111.111',
        'jacktrip-channels': '2',
        'queue': '6',
        'server': 'False'
    },
    'peers': {'ip_addresses': 'pi@raspberry.myvpn,pi@raspberry.myvpn'},
    'server1': {
        'ip': '111.111.111.111',
        'jacktrip-n': '2',
        'jacktrip-p': '256',
        'jacktrip-q': '6',
        'jacktrip-r': '48000'},
    'server2': {
        'ip': '222.222.222.222',
        'jacktrip-n': '2',
        'jacktrip-p': '256',
        'jacktrip-q': '6',
        'jacktrip-r': '48000'},
    'version': {'version': '0.1.4'}
}

default_config = {
    'jacktrip-default': {
        'hub_mode': 'True',
        'input-channels': '2',
        'ip': '123.123.123.123',
        'jacktrip-channels': '2',
        'queue': '6',
        'server': 'False'
    },
    'peers': {'ip_addresses': '111.111.111.111,222.222.222.222,333.333.333.333'},
    'server1': {
        'ip': '123.123.123.123',
        'jacktrip-n': '2',
        'jacktrip-p': '256',
        'jacktrip-q': '6',
        'jacktrip-r': '48000'},
    'server2': {
        'ip': '234.234.234.234',
        'jacktrip-n': '2',
        'jacktrip-p': '256',
        'jacktrip-q': '6',
        'jacktrip-r': '48000'},
    'version': {'version': '0.1.4'}
}

custom_config = {
    'jacktrip-default': {
        'input-channels': '2',
        'ip': '111.111.111.111',
        'jacktrip-channels': '2',
    },
    'peers': {'ip_addresses': 'pi@raspberry.myvpn,pi@raspberry.myvpn'},
    'server1': {
        'ip': '111.111.111.111'},
    'server2': {
        'ip': '222.222.222.222'},
}

default_path = './tests/test_default_config.ini'
custom_path = './tests/test_custom_config.ini'

def test_get_config():
    config = nh.config.get_config(default_path=default_path, custom_path=custom_path)
    my_config_parser_dict = {s:dict(config.items(s)) for s in config.sections()}

    assert my_config_parser_dict == combined_config

def test_get_default_config():
    config = nh.config.get_default_only(default_path=default_path)
    my_config_parser_dict = {s:dict(config.items(s)) for s in config.sections()}

    assert my_config_parser_dict == default_config

def test_get_custom_config():
    config = nh.config.get_custom_only(custom_path=custom_path)
    my_config_parser_dict = {s:dict(config.items(s)) for s in config.sections()}

    assert my_config_parser_dict == custom_config
