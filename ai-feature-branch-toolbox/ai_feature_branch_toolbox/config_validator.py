import re
import logging
from typing import Dict, Any

class ConfigValidator:
    @staticmethod
    def validate_config(config: Dict[str, Any]) -> None:
        ConfigValidator._validate_repository(config.get('repository', {}))
        ConfigValidator._validate_branches(config.get('branches', {}))
        ConfigValidator._validate_commit(config.get('commit', {}))
        ConfigValidator._validate_merge(config.get('merge', {}))
        ConfigValidator._validate_logging(config.get('logging', {}))
        ConfigValidator._validate_ai_agent(config.get('ai_agent', {}))

    @staticmethod
    def _validate_repository(repo: Dict[str, str]) -> None:
        logging.info("Validating repository configuration")
        if 'path' not in repo:
            raise ValueError("Repository path is required in 'repository'")
        if 'remote' not in repo:
            raise ValueError("Repository remote is required in 'repository'")

    @staticmethod
    def _validate_branches(branches: Dict[str, str]) -> None:
        logging.info("Validating branches configuration")
        if 'main' not in branches:
            raise ValueError("Main branch name is required in 'branches'")
        if 'prefix' not in branches:
            raise ValueError("Branch prefix is required in 'branches'")

    @staticmethod
    def _validate_commit(commit: Dict[str, str]) -> None:
        logging.info("Validating commit configuration")
        required_fields = ['author_name', 'author_email', 'message_template']
        for field in required_fields:
            if field not in commit:
                raise ValueError(f"Commit {field} is required in 'commit'")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", commit['author_email']):
            raise ValueError("Invalid email format for commit author_email in 'commit'")

    @staticmethod
    def _validate_merge(merge: Dict[str, Any]) -> None:
        logging.info("Validating merge configuration")
        if 'strategy' not in merge:
            raise ValueError("Merge strategy is required in 'merge'")
        if merge['strategy'] not in ['merge', 'rebase']:
            raise ValueError("Invalid merge strategy in 'merge'. Must be 'merge' or 'rebase'")
        if 'squash' not in merge or not isinstance(merge['squash'], bool):
            raise ValueError("Merge squash must be a boolean value in 'merge'")

    @staticmethod
    def _validate_logging(logging_config: Dict[str, str]) -> None:
        logging.info("Validating logging configuration")
        if 'level' not in logging_config:
            raise ValueError("Logging level is required in 'logging'")
        if logging_config['level'] not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            raise ValueError("Invalid logging level in 'logging'")
        if 'file' not in logging_config:
            raise ValueError("Logging file is required in 'logging'")

    @staticmethod
    def _validate_ai_agent(ai_agent: Dict[str, Any]) -> None:
        logging.info("Validating AI agent configuration")
        if 'model' not in ai_agent:
            raise ValueError("AI agent model is required in 'ai_agent'")
        if 'temperature' not in ai_agent:
            raise ValueError("AI agent temperature is required in 'ai_agent'")
        if not isinstance(ai_agent['temperature'], (int, float)) or not 0 <= ai_agent['temperature'] <= 1:
            raise ValueError("AI agent temperature must be a float between 0 and 1 in 'ai_agent'")