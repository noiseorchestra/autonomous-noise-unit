import configparser as cp
import os

default_path = './default-config.ini'
custom_path = './config.ini'

def get_config(default_path=default_path, custom_path=custom_path):
    cfg = cp.ConfigParser(interpolation=cp.ExtendedInterpolation())
    cfg.read(default_path)

    if os.path.isfile(custom_path):
        cfg.read(custom_path)

    else:
        print("""
        config.ini file not found, reading default-config.ini instead,
        please create your own config.ini file.
        """)

    return cfg


def get_default_only(default_path=default_path):
    cfg = cp.ConfigParser(interpolation=cp.ExtendedInterpolation())
    cfg.read(default_path)

    return cfg


def get_custom_only(custom_path=custom_path):
    cfg = cp.ConfigParser(interpolation=cp.ExtendedInterpolation())
    cfg.read(custom_path)

    return cfg


def change_server_ip(ip):
    cfg = get_custom_only()
    cfg["server1"]["ip"] = ip
    return cfg


def change_input_channels(channels):
    cfg = get_custom_only()
    cfg["jacktrip-default"]["input-channels"] = channels
    return cfg


def change_output_channels(channels):
    cfg = get_custom_only()
    cfg["jacktrip-default"]["output-channels"] = channels
    return cfg


def change_buffer(buffer):
    cfg = get_custom_only()
    cfg["jacktrip-default"]["jacktrip-q"] = buffer
    return cfg


def save(cfg):
    with open('./config.ini', 'w') as configfile:
        configfile.write(configfile)
