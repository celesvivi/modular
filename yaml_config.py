import yaml, os, log
from functools import reduce
from pathlib import Path

class config:
    def __init__(self, config_path, log = None):
        self.log = log
        self.version = 1.0
        self.config = self.load_config(os.path.join(config_path, 'config.yaml'))

    def _log(self, message: str, log_type: str = "info"):
        if self.log:
            self.log.log(message, log_type)
            

    def create_default_config_file(self) -> dict[str, any]:
        config = {
            'path': {
              'log': 'default'  
            },
            'version': {
                'log': log.version, 
                'yaml_congif': self.version
            },
            'author': 'celestine'
        }
        self._log("Default config created", log.TypeOfError.info)
        return config

    def save_config(self, config, config_path):
        with open(config_path, 'w') as file:
            yaml.dump(config, file, default_flow_style = False, indent = 2)
    
    def setup_config(self, config_path):
        if not os.path.exists(config_path):
            config = self.create_default_config_file();
            self.save_config(config, config_path)
            self._log("Config file setup successfully", log.TypeOfError.info)

    def load_config(self, config_path):
        try:
            with open(config_path, 'r') as file: 
                config = yaml.safe_load(file)
            self._log("Load config successfully", log.TypeOfError.info)
            return config
        except FileNotFoundError: #Create config file and load it again (dunno if this will lead to OuRoBoRos or not)
            self._log("Config file doesn't exist", log.TypeOfError.error)
            self._log("Making new config file", log.TypeOfError.action)
            self.setup_config(config_path)
            self.load_config(config_path)
    
    def get_variable(self, key, default = None): #AI gives me this, will check on it later on
        keys = key.split('.')
        return reduce(lambda d, k: d.get(k) if isinstance(d, dict) else None, keys, self.config) or default
        




