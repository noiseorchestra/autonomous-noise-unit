import configparser as cp
import os


class Config:

    def __init__(self, default_path='./default-config.ini', custom_path='./config.ini'):
        self.default_path = default_path
        self.custom_path = custom_path

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
        cfg["server1"]["ip"] = ip
        return cfg

    def change_input_channels(self, channels):
        cfg = self.get_custom_only()
        cfg["jacktrip-default"]["input-channels"] = channels
        return cfg

    def change_output_channels(self, channels):
        cfg = self.get_custom_only()
        cfg["jacktrip-default"]["output-channels"] = channels
        return cfg

    def change_queue(self, queue):
        cfg = self.get_custom_only()
        cfg["jacktrip-default"]["jacktrip-q"] = queue
        return cfg

    def save(self, cfg):
        with open('./config.ini', 'w') as configfile:
            cfg.write(configfile)
