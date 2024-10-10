import yaml
import logging
import os
from .config_validator import ConfigValidator
from .config_template import DEFAULT_CONFIG
from .persistent_config import PersistentConfig

class ConfigManager:
    def __init__(self, config_path='config.yaml'):
        self.config_path = config_path
        logging.info(f"Initializing ConfigManager with config path: {self.config_path}")
        logging.info(f"Current working directory: {os.getcwd()}")
        self.persistent_config = PersistentConfig()
        self.config = self._load_or_create_config()

    def _load_or_create_config(self):
        try:
            return self._load_config()
        except FileNotFoundError:
            return self._create_default_config()

    def _load_config(self):
        try:
            logging.info(f"Attempting to load config from: {self.config_path}")
            with open(self.config_path, 'r') as config_file:
                config = yaml.safe_load(config_file)
            logging.info(f"Successfully loaded config: {config}")

            # Merge with persistent config
            persistent_config = self.persistent_config.load()
            config.update(persistent_config)

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

    def _create_default_config(self):
        logging.info(f"Creating default configuration at {self.config_path}")
        config = DEFAULT_CONFIG.copy()
        self._save_config(config)
        return config

    def _save_config(self, config=None):
        if config is None:
            config = self.config
        try:
            with open(self.config_path, 'w') as config_file:
                yaml.dump(config, config_file, default_flow_style=False)
            logging.info(f"Configuration saved successfully to {self.config_path}")

            # Save to persistent config
            self.persistent_config.save(config)
        except Exception as e:
            logging.error(f"Error saving configuration: {e}")
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
        self.config[key] = value
        self.persistent_config.update(key, value)
        self._save_config()