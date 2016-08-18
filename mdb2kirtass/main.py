import configparser


def get_config(config):
    """Parse config file"""
    configreader = configparser.ConfigParser()
    configreader.read(config)
    return configreader
