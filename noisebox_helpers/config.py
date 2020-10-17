import configparser as cp
import os


class Config:

    def __init__(self, dry_run=False):
        self.default_path = None
        self.custom_path = None

        self.set_paths(dry_run)

    def set_paths(self, dry_run):
        if dry_run is True:
            self.default_path = './tests/test_default_config.ini'
            self.custom_path = './tests/test_custom_config.ini'
            return

        self.default_path = './default-config.ini'
        self.custom_path = './config.ini'

    def get_config(self):
        cfg = cp.ConfigParser(interpolation=cp.ExtendedInterpolation())
        cfg.read(self.default_path)

        if os.path.isfile(self.custom_path):
            cfg.read(self.custom_path)

        else:
            print("""
            config.ini file not found, reading default-config.ini instead,
            please create your own config.ini file.
            """)

        return cfg

    def get_default_only(self):
        cfg = cp.ConfigParser(interpolation=cp.ExtendedInterpolation())
        cfg.read(self.default_path)

        return cfg

    def get_custom_only(self):
        cfg = cp.ConfigParser(interpolation=cp.ExtendedInterpolation())
        cfg.read(self.custom_path)

        return cfg

    def change_server_ip(self, ip):
        cfg = self.get_custom_only()
        cfg["jacktrip-default"]["ip"] = ip
        return cfg

    def change_input_channels(self, channels):
        cfg = self.get_custom_only()
        cfg["jacktrip-default"]["input-channels"] = channels
        return cfg

    def change_output_channels(self, channels):
        cfg = self.get_custom_only()
        cfg["jacktrip-default"]["jacktrip-channels"] = channels
        return cfg

    def change_queue(self, queue):
        cfg = self.get_custom_only()
        cfg["jacktrip-default"]["jacktrip-q"] = queue
        return cfg

    def save(self, cfg):
        with open('./config.ini', 'w') as configfile:
            cfg.write(configfile)
