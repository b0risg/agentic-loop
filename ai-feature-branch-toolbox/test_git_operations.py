from ai_feature_branch_toolbox import GitOperations
import os
import shutil

def test_git_operations():
    print("Starting test_git_operations")
    print(f"Current working directory: {os.getcwd()}")

    # Create a temporary directory for testing
    test_repo_path = "test_repo"
    print(f"Attempting to create directory: {test_repo_path}")
    os.makedirs(test_repo_path, exist_ok=True)
    print(f"Directory created: {os.path.exists(test_repo_path)}")

    # Initialize GitOperations
    git_ops = GitOperations()
    print("GitOperations instance created")

    # Test initializing a new repository
    success = git_ops.initialize_repo(test_repo_path)
    print(f"Initializing new repository: {'Success' if success else 'Failed'}")
    print(f"Connected to repository: {git_ops.is_connected()}")

    # Test listing branches
    branches = git_ops.list_branches()
    print(f"Branches in the repository: {branches}")

    # Test creating a new feature branch
    new_branch_name = "feature-test"
    success = git_ops.create_feature_branch(new_branch_name)
    print(f"Creating new feature branch '{new_branch_name}': {'Success' if success else 'Failed'}")

    # Verify the new branch appears in the list of branches
    updated_branches = git_ops.list_branches()
    print(f"Updated branches in the repository: {updated_branches}")
    print(f"New branch '{new_branch_name}' created: {new_branch_name in updated_branches}")

    # Close the repository before attempting to remove it
    print("Closing repository")
    git_ops.close_repo()

    # Clean up: remove the test repository
    print(f"Attempting to remove directory: {test_repo_path}")
    try:
        shutil.rmtree(test_repo_path)
        print(f"Directory removed: {not os.path.exists(test_repo_path)}")
    except PermissionError:
        print(f"Failed to remove directory. It may still be in use.")
        print("Please close any applications using the directory and try again.")

    # Test connecting to a non-existent repository (should fail)
    print(f"Attempting to initialize non-existent repository at: non_existent_repo")
    success = git_ops.initialize_repo("non_existent_repo")
    print(f"Connecting to non-existent repository: {'Success' if success else 'Failed'}")
    print(f"Connected to repository: {git_ops.is_connected()}")
    print(f"Repository object: {git_ops.repo}")

    # Test listing branches on a non-existent repository
    branches = git_ops.list_branches()
    print(f"Branches in non-existent repository: {branches}")

    print("Test completed. The test repository has been created, used for testing, and then removed as part of the cleanup process.")
    print("test_git_operations completed")

if __name__ == "__main__":
    test_git_operations()