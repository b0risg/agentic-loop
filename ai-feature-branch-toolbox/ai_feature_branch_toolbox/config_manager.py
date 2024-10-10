import yaml
import logging
import os
from .config_validator import ConfigValidator

class ConfigManager:
    def __init__(self, config_path='config.yaml'):
        self.config_path = config_path
        logging.info(f"Initializing ConfigManager with config path: {self.config_path}")
        logging.info(f"Current working directory: {os.getcwd()}")
        self.config = self._load_config()

    def _load_config(self):
        try:
            logging.info(f"Attempting to load config from: {self.config_path}")
            with open(self.config_path, 'r') as config_file:
                config = yaml.safe_load(config_file)
            logging.info(f"Successfully loaded config: {config}")

            # Validate the loaded configuration
            logging.info("Validating configuration")
            ConfigValidator.validate_config(config)
            logging.info("Configuration validation completed successfully")

            return config
        except FileNotFoundError as e:
            logging.error(f"Configuration file not found at {self.config_path}. Error: {e}")
            raise FileNotFoundError(f"Configuration file not found at {self.config_path}")
        except yaml.YAMLError as e:
            logging.error(f"Error parsing YAML configuration: {e}")
            raise ValueError(f"Error parsing YAML configuration: {e}")
        except ValueError as e:
            logging.error(f"Invalid configuration: {e}")
            raise

    def get_config(self):
        return self.config

    def get_value(self, key, default=None):
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def set_value(self, key, value):
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self._save_config()

    def _save_config(self):
        try:
            with open(self.config_path, 'w') as config_file:
                yaml.dump(self.config, config_file, default_flow_style=False)
            logging.info(f"Configuration saved successfully to {self.config_path}")
        except Exception as e:
            logging.error(f"Error saving configuration: {e}")
            raise