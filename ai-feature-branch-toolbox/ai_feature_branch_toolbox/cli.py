import argparse
import sys
from .git_operations import GitOperations
from .config_manager import ConfigManager

def init_command(args):
    git_ops = GitOperations()
    config_manager = ConfigManager(args.config_path)

    try:
        if git_ops.initialize_repo(args.repo_path):
            print(f"Successfully initialized repository at {args.repo_path}")
            config_manager.set_value('repository.path', args.repo_path)
            if args.remote_url:
                if git_ops.add_remote('origin', args.remote_url):
                    print(f"Added remote 'origin' with URL: {args.remote_url}")
                    config_manager.set_value('repository.remote_url', args.remote_url)
                else:
                    print(f"Failed to add remote repository")
            config_manager._save_config()
            print(f"Updated configuration file at {args.config_path}")
        else:
            print(f"Failed to initialize repository at {args.repo_path}")
            sys.exit(1)
    except Exception as e:
        print(f"An error occurred during initialization: {e}")
        sys.exit(1)
    finally:
        git_ops.close_repo()

def create_branch_command(args, git_ops):
    if git_ops.create_feature_branch(args.branch_name):
        print(f"Successfully created and switched to new branch: {args.branch_name}")
    else:
        print(f"Failed to create branch: {args.branch_name}")
        sys.exit(1)

def switch_branch_command(args, git_ops):
    if git_ops.switch_branch(args.branch_name):
        print(f"Successfully switched to branch: {args.branch_name}")
    else:
        print(f"Failed to switch to branch: {args.branch_name}")
        sys.exit(1)

def commit_command(args, git_ops):
    if git_ops.commit_changes(args.message):
        print(f"Successfully committed changes with message: {args.message}")
    else:
        print("Failed to commit changes")
        sys.exit(1)

def push_command(args, git_ops):
    config_manager = ConfigManager('config.yaml')
    remote_url = config_manager.get_value('repository.remote_url')
    if not remote_url:
        print("Remote URL not set. Please provide a remote URL:")
        remote_url = input("https://github.com/b0risg/workspace.git")  # INPUT_REQUIRED {Provide the remote repository URL}
        if git_ops.add_remote('origin', remote_url):
            print(f"Added remote 'origin' with URL: {remote_url}")
            config_manager.set_value('repository.remote_url', remote_url)
            config_manager._save_config()
        else:
            print("Failed to add remote repository")
            sys.exit(1)

    if git_ops.push_changes(remote=args.remote, branch=args.branch):
        print(f"Successfully pushed changes to remote repository")
    else:
        print("Failed to push changes")
        sys.exit(1)

def merge_branch_command(args, git_ops):
    result = git_ops.merge_feature_branch(args.feature_branch, args.main_branch)
    if result == True:
        print(f"Successfully merged '{args.feature_branch}' into '{args.main_branch}'")
    elif result == 'CONFLICT':
        print("Merge conflict detected. Please resolve conflicts manually and then commit the changes.")
        print("After resolving conflicts, run the 'resolve-conflicts' command.")
    else:
        print(f"Failed to merge '{args.feature_branch}' into '{args.main_branch}'")
        sys.exit(1)

def resolve_conflicts_command(args, git_ops):
    result = git_ops.resolve_conflicts()
    if result == True:
        print("No conflicts detected.")
    elif result == 'CONFLICT':
        print("Conflicts detected. Please resolve them manually, stage the changes, and then commit.")
        print("Use the following commands:")
        print("1. Edit the conflicting files to resolve conflicts")
        print("2. Stage the resolved files: git add <filename>")
        print("3. Commit the changes: git commit -m 'Resolve merge conflicts'")
    else:
        print("Failed to check for conflicts")
        sys.exit(1)

def help_command(args):
    print("AI Feature Branch Toolbox CLI Help")
    print("Available commands:")
    print("  init             Initialize the repository")
    print("  create-branch    Create a new feature branch")
    print("  switch-branch    Switch to an existing branch")
    print("  commit           Commit changes to the current branch")
    print("  push             Push changes to the remote repository")
    print("  merge            Merge a feature branch into the main branch")
    print("  resolve-conflicts Check and resolve merge conflicts")
    print("Use 'ai-feature-branch-toolbox <command> --help' for more information on a command.")

def main():
    parser = argparse.ArgumentParser(
        description="AI Feature Branch Toolbox CLI",
        epilog="For more information on each command, use: ai-feature-branch-toolbox <command> --help"
    )
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize the repository')
    init_parser.add_argument('--repo-path', required=True, help='Path to the Git repository')
    init_parser.add_argument('--config-path', default='config.yaml', help='Path to the configuration file')
    init_parser.add_argument('--remote-url', help='URL of the remote repository')

    # Create branch command
    create_branch_parser = subparsers.add_parser('create-branch', help='Create a new feature branch')
    create_branch_parser.add_argument('branch_name', help='Name of the new branch')

    # Switch branch command
    switch_branch_parser = subparsers.add_parser('switch-branch', help='Switch to an existing branch')
    switch_branch_parser.add_argument('branch_name', help='Name of the branch to switch to')

    # Commit changes command
    commit_parser = subparsers.add_parser('commit', help='Commit changes to the current branch')
    commit_parser.add_argument('message', help='Commit message')

    # Push changes command
    push_parser = subparsers.add_parser('push', help='Push changes to the remote repository')
    push_parser.add_argument('--remote', default='origin', help='Name of the remote repository')
    push_parser.add_argument('--branch', help='Name of the branch to push')

    # Add merge command
    merge_parser = subparsers.add_parser('merge', help='Merge a feature branch into the main branch')
    merge_parser.add_argument('feature_branch', help='Name of the feature branch to merge')
    merge_parser.add_argument('--main-branch', default='main', help='Name of the main branch (default: main)')

    # Add resolve-conflicts command
    resolve_conflicts_parser = subparsers.add_parser('resolve-conflicts', help='Check and resolve merge conflicts')

    # Add help command
    help_parser = subparsers.add_parser('help', help='Show help message')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        git_ops = GitOperations()
        config_manager = ConfigManager('config.yaml')

        if args.command == 'init':
            init_command(args)
        elif args.command == 'help':
            help_command(args)
        else:
            repo_path = config_manager.get_value('repository.path')

            if not repo_path:
                raise ValueError("Repository path not set. Please run 'init' command first.")

            if not git_ops.initialize_repo(repo_path):
                raise RuntimeError(f"Failed to initialize repository at {repo_path}")

            try:
                if args.command == 'create-branch':
                    create_branch_command(args, git_ops)
                elif args.command == 'switch-branch':
                    switch_branch_command(args, git_ops)
                elif args.command == 'commit':
                    commit_command(args, git_ops)
                elif args.command == 'push':
                    push_command(args, git_ops)  # This line is added as per instructions
                elif args.command == 'merge':
                    merge_branch_command(args, git_ops)
                elif args.command == 'resolve-conflicts':
                    resolve_conflicts_command(args, git_ops)
            finally:
                git_ops.close_repo()

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()