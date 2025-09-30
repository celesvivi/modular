import yaml, os, sys
from mLog import Logger, TypeOfLog
from functools import reduce
from pathlib import Path

def get_app_directory():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))
# VERION 1.1
class Config:
    """
        Config class for yaml config file

        Handles loading, saving, and accessing configuration values from YAML files.
        Automatically creates default config if file doesn't exist.

        Args:
        config_path (path, default = app_dir): dir of config file
        default_config (dict, opt): custom default config for creation
        log (Logger, opt): logger instance for logging, empty if you don't want to log yaml
    """
    def __init__(self, config_path = None, default_config = None, log = None):
        version = 1.1
        self.logger = Logger()
        self.default_config = default_config

        if config_path is None:
            self.config_path = get_app_directory()
        else: 
            self.config_path = config_path
        self.config = self._load_config(os.path.join(config_path, 'config.yaml'))

    def _log(self, message, log_type = "info"):
        if self.logger is not None:
            self.logger.log(message, log_type)
            

    def _create_default_config_file(self):
        if self.default_config is not None:
            return self.default_config        
        config = {
            'path': {
              'log': 'default'
            },
            'author': 'celestine'
        }
        self._log("Default config created", TypeOfLog.INFO)
        return config

    def _save_config(self, config, config_path):
        with open(config_path, 'w', encoding='utf-8') as file:
            yaml.dump(config, file, default_flow_style = False, indent = 2)
    
    def _setup_config(self, config_path):
        if not os.path.exists(config_path):
            config = self._create_default_config_file()
            self._save_config(config, config_path)
            self._log("Config file setup successfully", TypeOfLog.INFO)

    def _load_config(self, config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as file: 
                config = yaml.safe_load(file)
            self._log("Load config successfully", TypeOfLog.INFO)
            return config
        except FileNotFoundError: #Create config file and load it again (dunno if this will lead to OuRoBoRos or not)
            self._log("Config file doesn't exist", TypeOfLog.ERROR)
            self._log("Making new config file", TypeOfLog.ACTION)
            self._setup_config(config_path)
            self._load_config(config_path)
    
    def _get_variable(self, key, default = None):
        """
        Get a value from the config file
        Args:
            key (str): the value you want to get (e.g. port)
            default (any, opt): default value if value of key doesn't exist
        Returns:
            value of key or default value if not found
        """
        #Only have vague idea of how this works
        keys = key.slipt('.')
        result = reduce(
            lambda d, k: d.get(k) if isinstance(d, dict) else None,
            keys,
            self.config
        )
        return default if result is None else result