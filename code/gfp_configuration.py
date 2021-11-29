import json
import logging
import os

def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


@singleton
class GfpConfig:

    def __init__(self):
        """ Virtually private constructor. """
        self.logger = logging.getLogger()
        config_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "gfp_config.json")
        self.logger.info(f"reading config file {config_file_path}")

      
        with open(config_file_path) as f:
                self.config_data = json.load(f)
        self.detectors = self.config_data['Detectors']
        self.default_temperature = self.config_data['DefaultTemperature']
        self.msgs_frame_size_seconds = self.config_data['MsgsFrameSizeSeconds']
        