# AI Feature Branch Toolbox

The AI Feature Branch Toolbox is a Python library designed to facilitate feature branch-based development for AI agents interacting with Git repositories. The toolbox provides functionalities such as initializing repositories, managing branches, committing changes, and merging feature branches, all while adhering to specified branch naming conventions and maintaining persistent configuration states.

## Overview

The AI Feature Branch Toolbox is written in Python and deployed as a Python installation package. The configuration is managed through a `config.yaml` file, with mechanisms to generate a template `config.yaml` and maintain a persistent configuration state across branch operations. The toolbox enforces branch naming conventions and provides comprehensive usage instructions.

## Features

- **Initialization**: Initialize Git repositories and create a default configuration file.
- **Branch Management**: Create and switch branches while enforcing naming conventions.
- **Committing**: Commit changes to the repository with specified commit messages.
- **Merging**: Merge feature branches into the main branch, with conflict detection and resolution support.
- **Configuration Management**: Generate and manage configuration settings using `config.yaml` and persistent storage.
- **CLI Interface**: Comprehensive command-line interface for interacting with the toolbox.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-feature-branch-toolbox.git
   cd ai-feature-branch-toolbox
   ```

2. Install the package:
   ```
   pip install -e .
   ```

## Usage

### Initializing a Repository

To initialize a repository and create a default configuration file:

```
ai-feature-branch-toolbox init --repo-path /path/to/your/repo --config-path config.yaml --remote-url https://github.com/yourusername/yourrepo.git
```

- `--repo-path`: Path to the Git repository (required)
- `--config-path`: Path to the configuration file (default: config.yaml)
- `--remote-url`: URL of the remote repository (optional)

### Creating a Feature Branch

To create a new feature branch:

```
ai-feature-branch-toolbox create-branch feature/new-feature-name
```

- The branch name should follow the prefix specified in your `config.yaml` file.

### Switching Branches

To switch to an existing branch:

```
ai-feature-branch-toolbox switch-branch branch-name
```

### Committing Changes

To commit changes to the current branch:

```
ai-feature-branch-toolbox commit "Your commit message here"
```

### Pushing Changes

To push changes to the remote repository:

```
ai-feature-branch-toolbox push --remote origin --branch feature/your-branch-name
```

- `--remote`: Name of the remote repository (default: origin)
- `--branch`: Name of the branch to push

### Merging Branches

To merge a feature branch into the main branch:

```
ai-feature-branch-toolbox merge feature/your-feature-branch --main-branch main
```

- `--main-branch`: Name of the main branch (default: main)

### Resolving Conflicts

If conflicts occur during a merge, you can use the following command to check and resolve them:

```
ai-feature-branch-toolbox resolve-conflicts
```

This command will guide you through the process of resolving conflicts manually.

### Getting Help

To see the list of available commands and their descriptions:

```
ai-feature-branch-toolbox help
```

For more information on a specific command:

```
ai-feature-branch-toolbox <command> --help
```

## Configuration

The `config.yaml` file is used to store settings for the AI Feature Branch Toolbox. Here's an example of what it might contain:

```yaml
repository:
  path: /path/to/your/repo
  remote_url: https://github.com/yourusername/yourrepo.git
branch:
  prefix: feature/
  main: main
commit:
  author_name: AI Agent
  author_email: ai@example.com
merge:
  strategy: recursive
logging:
  level: INFO
  file: ai_feature_branch.log
```

You can modify this file to customize the behavior of the toolbox according to your needs.

## Troubleshooting

If you encounter any issues while using the AI Feature Branch Toolbox, please check the following:

1. Ensure that Git is installed and properly configured on your system.
2. Verify that you have the necessary permissions to access and modify the repository.
3. Check the `config.yaml` file for any misconfiguration.
4. Review the log file (specified in `config.yaml`) for any error messages or warnings.

If problems persist, please open an issue on the GitHub repository with a detailed description of the problem and steps to reproduce it.

## License

This project is proprietary. All rights reserved.

© 2024. All rights reserved.