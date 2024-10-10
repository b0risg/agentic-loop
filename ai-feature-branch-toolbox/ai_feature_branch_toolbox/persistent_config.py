import os
import json
import logging

logger = logging.getLogger(__name__)

class PersistentConfig:
    def __init__(self, config_dir='.ai_feature_branch_toolbox'):
        self.config_dir = config_dir
        self.config_file = os.path.join(self.config_dir, 'persistent_config.json')
        self._ensure_config_dir()

    def _ensure_config_dir(self):
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
            logger.info(f"Created persistent config directory: {self.config_dir}")

    def load(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}

    def save(self, config):
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        logger.info(f"Saved persistent config to {self.config_file}")

    def update(self, key, value):
        config = self.load()
        config[key] = value
        self.save(config)

    def get(self, key, default=None):
        config = self.load()
        return config.get(key, default)