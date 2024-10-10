import unittest
from ai_feature_branch_toolbox import ConfigManager
import tempfile
import os
import logging
import shutil

logging.basicConfig(level=logging.INFO)

class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, 'test_config.yaml')
        logging.info(f"Setting up test with config path: {self.config_path}")
        self.valid_config = '''
repository:
  path: "/path/to/repo"
  remote: "origin"
branches:
  main: "main"
  prefix: "feature/"
commit:
  author_name: "AI Agent"
  author_email: "ai@example.com"
  message_template: "feat: {message}"
merge:
  strategy: "merge"
  squash: false
logging:
  level: "INFO"
  file: "ai_feature_branch.log"
ai_agent:
  model: "default"
  temperature: 0.7
'''
        with open(self.config_path, 'w') as f:
            f.write(self.valid_config)
        logging.info(f"Test config file created at: {self.config_path}")

    def tearDown(self):
        logging.info(f"Cleaning up test environment for config path: {self.config_path}")
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_load_valid_config(self):
        logging.info("Running test_load_valid_config")
        config_manager = ConfigManager(self.config_path)
        config = config_manager.get_config()
        logging.info(f"Loaded config: {config}")
        self.assertIsInstance(config, dict)
        self.assertEqual(config['repository']['path'], "/path/to/repo")
        self.assertEqual(config['branches']['main'], "main")

    def test_invalid_repository(self):
        logging.info("Running test_invalid_repository")
        invalid_config = self.valid_config.replace('path: "/path/to/repo"', '')
        with open(self.config_path, 'w') as f:
            f.write(invalid_config)
        with self.assertRaises(ValueError) as context:
            ConfigManager(self.config_path)
        self.assertIn("Repository path is required", str(context.exception))

    def test_invalid_branches(self):
        logging.info("Running test_invalid_branches")
        invalid_config = self.valid_config.replace('main: "main"', '')
        with open(self.config_path, 'w') as f:
            f.write(invalid_config)
        with self.assertRaises(ValueError) as context:
            ConfigManager(self.config_path)
        self.assertIn("Main branch name is required", str(context.exception))

    def test_invalid_commit(self):
        logging.info("Running test_invalid_commit")
        invalid_config = self.valid_config.replace('author_email: "ai@example.com"', 'author_email: "invalid_email"')
        with open(self.config_path, 'w') as f:
            f.write(invalid_config)
        with self.assertRaises(ValueError) as context:
            ConfigManager(self.config_path)
        self.assertIn("Invalid email format for commit author_email", str(context.exception))

    def test_invalid_merge(self):
        logging.info("Running test_invalid_merge")
        invalid_config = self.valid_config.replace('strategy: "merge"', 'strategy: "invalid_strategy"')
        with open(self.config_path, 'w') as f:
            f.write(invalid_config)
        with self.assertRaises(ValueError) as context:
            ConfigManager(self.config_path)
        self.assertIn("Invalid merge strategy", str(context.exception))

    def test_invalid_logging(self):
        logging.info("Running test_invalid_logging")
        invalid_config = self.valid_config.replace('level: "INFO"', 'level: "INVALID_LEVEL"')
        with open(self.config_path, 'w') as f:
            f.write(invalid_config)
        with self.assertRaises(ValueError) as context:
            ConfigManager(self.config_path)
        self.assertIn("Invalid logging level", str(context.exception))

    def test_invalid_ai_agent(self):
        logging.info("Running test_invalid_ai_agent")
        invalid_config = self.valid_config.replace('temperature: 0.7', 'temperature: 1.5')
        with open(self.config_path, 'w') as f:
            f.write(invalid_config)
        with self.assertRaises(ValueError) as context:
            ConfigManager(self.config_path)
        self.assertIn("AI agent temperature must be a float between 0 and 1", str(context.exception))

    def test_get_value(self):
        logging.info("Running test_get_value")
        config_manager = ConfigManager(self.config_path)
        self.assertEqual(config_manager.get_value('repository.remote'), "origin")
        self.assertEqual(config_manager.get_value('branches.prefix'), "feature/")
        self.assertIsNone(config_manager.get_value('nonexistent.key'))
        self.assertEqual(config_manager.get_value('nonexistent.key', 'default'), 'default')

    def test_file_not_found(self):
        logging.info("Running test_file_not_found")
        with self.assertRaises(FileNotFoundError):
            ConfigManager('nonexistent.yaml')

    def test_invalid_yaml(self):
        logging.info("Running test_invalid_yaml")
        invalid_config_path = os.path.join(self.temp_dir, 'invalid_config.yaml')
        with open(invalid_config_path, 'w') as f:
            f.write('invalid: yaml: content')
        with self.assertRaises(ValueError):
            ConfigManager(invalid_config_path)

if __name__ == '__main__':
    unittest.main()