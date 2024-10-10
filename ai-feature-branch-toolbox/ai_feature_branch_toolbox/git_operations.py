import os
import logging
from git import Repo, InvalidGitRepositoryError, GitCommandError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GitOperations:
    def __init__(self):
        self.repo = None

    def initialize_repo(self, path):
        """
        Initialize and connect to a Git repository.

        Args:
            path (str): The path to the Git repository.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            logger.info(f"Attempting to initialize repo at path: {path}")
            if os.path.exists(path):
                try:
                    self.repo = Repo(path)
                    logger.info(f"Connected to existing repository at {path}.")
                except InvalidGitRepositoryError:
                    self.repo = Repo.init(path)
                    logger.info(f"Initialized a new repository in existing directory at {path}.")
                    self._create_initial_commit()
            else:
                logger.error(f"Path {path} does not exist. Failing initialization.")
                return False

            return True
        except Exception as e:
            logger.exception(f"An error occurred while initializing the repository: {str(e)}")
            return False

    def _create_initial_commit(self):
        # Create a README file
        readme_path = os.path.join(self.repo.working_tree_dir, "README.md")
        with open(readme_path, "w") as f:
            f.write("# Initial commit\n")

        # Stage the README file
        self.repo.index.add(["README.md"])

        # Create the initial commit
        self.repo.index.commit("Initial commit")
        logger.info("Created initial commit")

    def is_connected(self):
        """
        Check if connected to a Git repository.

        Returns:
            bool: True if connected, False otherwise.
        """
        connected = self.repo is not None
        logger.info(f"Repository connected: {connected}")
        return connected

    def list_branches(self):
        """
        List all branches in the repository.

        Returns:
            list: A list of branch names, or None if not connected to a repository.
        """
        if not self.is_connected():
            logger.error("Not connected to a repository.")
            return None

        try:
            branches = [branch.name for branch in self.repo.branches]
            logger.info(f"Branches in the repository: {', '.join(branches)}")
            return branches
        except Exception as e:
            logger.exception(f"An error occurred while listing branches: {str(e)}")
            return None

    def create_feature_branch(self, branch_name):
        """
        Create a new feature branch.

        Args:
            branch_name (str): The name of the new feature branch.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self.is_connected():
            logger.error("Not connected to a repository.")
            return False

        try:
            new_branch = self.repo.create_head(branch_name)
            new_branch.checkout()
            logger.info(f"Created and switched to new branch: {branch_name}")
            return True
        except Exception as e:
            logger.exception(f"An error occurred while creating the feature branch: {str(e)}")
            return False

    def switch_branch(self, branch_name):
        """
        Switch to the specified branch.

        Args:
            branch_name (str): The name of the branch to switch to.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self.is_connected():
            logger.error("Not connected to a repository.")
            return False

        try:
            if branch_name not in [branch.name for branch in self.repo.branches]:
                logger.error(f"Branch '{branch_name}' does not exist.")
                return False

            self.repo.git.checkout(branch_name)
            logger.info(f"Switched to branch: {branch_name}")
            return True
        except Exception as e:
            logger.exception(f"An error occurred while switching branches: {str(e)}")
            return False

    def close_repo(self):
        """
        Close the repository and release resources.
        """
        if self.repo:
            self.repo.close()
            self.repo = None
        logger.info("Repository closed and resources released.")

    def commit_changes(self, message):
        """
        Commit changes to the current branch.

        Args:
            message (str): The commit message.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self.is_connected():
            logger.error("Not connected to a repository.")
            return False

        try:
            logger.info(f"Attempting to commit changes with message: {message}")
            logger.info(f"Repository dirty status: {self.repo.is_dirty()}")
            logger.info(f"Untracked files: {self.repo.untracked_files}")

            # Check if there are any changes to commit
            if not self.repo.is_dirty() and len(self.repo.untracked_files) == 0:
                logger.warning("No changes to commit.")
                return False

            # Stage all changes
            logger.info("Staging all changes")
            self.repo.git.add(A=True)

            # Commit the changes
            logger.info("Committing changes")
            commit = self.repo.index.commit(message)
            logger.info(f"Changes committed successfully. Commit hash: {commit.hexsha}")
            return True
        except Exception as e:
            logger.exception(f"An error occurred while committing changes: {str(e)}")
            return False

    def merge_feature_branch(self, feature_branch, main_branch='main'):
        if not self.is_connected():
            logger.error("Not connected to a repository.")
            return False

        try:
            logger.info(f"Attempting to merge '{feature_branch}' into '{main_branch}'")
            self.switch_branch(main_branch)

            try:
                self.repo.git.merge(feature_branch)
                logger.info(f"Successfully merged '{feature_branch}' into '{main_branch}'.")
                return True
            except GitCommandError as e:
                if 'conflict' in str(e).lower():
                    logger.warning("Merge conflict detected. Please resolve conflicts manually.")
                    return 'CONFLICT'
                else:
                    raise
        except Exception as e:
            logger.exception(f"An error occurred while merging branches: {str(e)}")
            return False

    def resolve_conflicts(self):
        if not self.is_connected():
            logger.error("Not connected to a repository.")
            return False

        try:
            status = self.repo.git.status()
            if 'You have unmerged paths.' in status:
                logger.info("Conflicts detected. Please resolve them manually and then commit the changes.")
                return 'CONFLICT'
            else:
                logger.info("No conflicts detected.")
                return True
        except Exception as e:
            logger.exception(f"An error occurred while checking for conflicts: {str(e)}")
            return False

    def add_remote(self, name, url):
        """
        Add or update a remote repository.

        Args:
            name (str): The name of the remote (e.g., 'origin').
            url (str): The URL of the remote repository.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self.is_connected():
            logger.error("Not connected to a repository.")
            return False

        try:
            if name in self.repo.remotes:
                remote = self.repo.remote(name)
                old_url = remote.url
                if old_url != url:
                    remote.set_url(url)
                    logger.info(f"Updated remote '{name}' URL from {old_url} to {url}")
                else:
                    logger.info(f"Remote '{name}' already exists with the correct URL")
            else:
                self.repo.create_remote(name, url)
                logger.info(f"Added new remote '{name}' with URL: {url}")

            # Verify the remote
            self.repo.git.remote('update', name)
            logger.info(f"Successfully verified remote '{name}'")
            return True
        except Exception as e:
            logger.exception(f"An error occurred while managing remote: {str(e)}")
            return False