# ai_feature_branch_toolbox/config_template.py

DEFAULT_CONFIG = {
    'repository': {
        'path': './',  # INPUT_REQUIRED {Provide the local path to your repository}
        'remote': 'origin',
        'remote_url': 'https://github.com/b0risg/workspace.git'  # INPUT_REQUIRED {Provide the remote repository URL}
    },
    'branches': {
        'main': 'main',
        'prefix': 'feature/'
    },
    'commit': {
        'author_name': 'AI Agent',
        'author_email': 'borisjg@gmail.com',  # INPUT_REQUIRED {Provide the author's email}
        'message_template': 'feat: {message}'
    },
    'merge': {
        'strategy': 'merge',
        'squash': False
    },
    'logging': {
        'level': 'INFO',
        'file': 'ai_feature_branch.log'
    },
    'ai_agent': {
        'model': 'default',
        'temperature': 0.7
    }
}