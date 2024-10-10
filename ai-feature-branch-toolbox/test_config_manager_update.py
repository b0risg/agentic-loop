import os
import tempfile
import unittest
import yaml
import logging
from ai_feature_branch_toolbox.config_manager import ConfigManager

class TestConfigManagerUpdate(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, 'test_config.yaml')
        logging.info(f"Test config path: {self.config_path}")
        self.initial_config = {
            'repository': {'path': '/test/repo', 'remote': 'origin'},
            'branches': {'main': 'main', 'prefix': 'feature/'},
            'commit': {
                'author_name': 'Test AI',
                'author_email': 'test@example.com',
                'message_template': 'feat: {message}'
            },
            'merge': {'strategy': 'merge', 'squash': False},
            'logging': {'level': 'INFO', 'file': 'test.log'},
            'ai_agent': {'model': 'default', 'temperature': 0.7}
        }
        logging.info(f"Initial config: {self.initial_config}")
        with open(self.config_path, 'w') as f:
            yaml.dump(self.initial_config, f)
        logging.info(f"Config file contents:\n{open(self.config_path, 'r').read()}")
        self.config_manager = ConfigManager(self.config_path)

    def tearDown(self):
        os.remove(self.config_path)
        os.rmdir(self.temp_dir)

    def test_get_value(self):
        logging.info(f"Current config: {self.config_manager.get_config()}")
        self.assertEqual(self.config_manager.get_value('repository.path'), '/test/repo')
        self.assertEqual(self.config_manager.get_value('branches.main'), 'main')
        self.assertIsNone(self.config_manager.get_value('nonexistent.key'))

    def test_set_value(self):
        logging.info(f"Current config before set: {self.config_manager.get_config()}")
        self.config_manager.set_value('repository.path', '/new/repo')
        logging.info(f"Current config after set: {self.config_manager.get_config()}")
        self.assertEqual(self.config_manager.get_value('repository.path'), '/new/repo')

        self.config_manager.set_value('new.key', 'new_value')
        logging.info(f"Current config after adding new key: {self.config_manager.get_config()}")
        self.assertEqual(self.config_manager.get_value('new.key'), 'new_value')

    def test_set_value_persistence(self):
        logging.info(f"Current config before set: {self.config_manager.get_config()}")
        self.config_manager.set_value('commit.author_email', 'test@example.com')
        logging.info(f"Current config after set: {self.config_manager.get_config()}")

        # Create a new ConfigManager instance to verify persistence
        new_config_manager = ConfigManager(self.config_path)
        logging.info(f"New config manager config: {new_config_manager.get_config()}")
        self.assertEqual(new_config_manager.get_value('commit.author_email'), 'test@example.com')

if __name__ == '__main__':
    unittest.main()