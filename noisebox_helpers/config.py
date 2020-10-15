import configparser as cp
import os

def get_config(default_config_path='./default-config.ini', custom_config_path='./config.ini'):
    cfg = cp.ConfigParser(interpolation=cp.ExtendedInterpolation())
    cfg.read(default_config_path)

    if os.path.isfile(custom_config_path):
        cfg.read(custom_config_path)

    else:
        print("""
        config.ini file not found, reading default-config.ini instead,
        please create your own config.ini file.
        """)

    return cfg

def get_default_only(default_config_path='./default-config.ini'):
    cfg = cp.ConfigParser(interpolation=cp.ExtendedInterpolation())
    cfg.read(default_config_path)

    return cfg

def get_custom_only(custom_config_path='./config.ini'):
    cfg = cp.ConfigParser(interpolation=cp.ExtendedInterpolation())
    cfg.read(custom_config_path)

    return cfg
