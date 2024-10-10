import os
import shutil
import tempfile
import time
import unittest
from ai_feature_branch_toolbox.git_operations import GitOperations

print("Successfully imported GitOperations")

def cleanup_directory(directory):
    # Wait a short time to allow file handles to be released
    time.sleep(0.1)

    # Use shutil.rmtree with ignore_errors=True
    shutil.rmtree(directory, ignore_errors=True)

    # If the directory still exists, wait a bit longer and try again
    if os.path.exists(directory):
        time.sleep(0.5)
        shutil.rmtree(directory, ignore_errors=True)

class TestCommitChanges(unittest.TestCase):
    def setUp(self):
        print("Starting script")
        print(f"Current working directory: {os.getcwd()}")
        self.temp_dir = tempfile.mkdtemp()
        self.git_ops = GitOperations()
        print(f"GitOperations instance created: {self.git_ops}")
        init_result = self.git_ops.initialize_repo(self.temp_dir)
        print(f"Repository initialization result: {init_result}")

    def tearDown(self):
        self.git_ops.close_repo()
        cleanup_directory(self.temp_dir)

    def test_commit_changes(self):
        # Create a new file
        test_file_path = os.path.join(self.temp_dir, "test_file.txt")
        with open(test_file_path, "w") as f:
            f.write("Test content")
        print(f"Created test file at: {test_file_path}")

        # Commit the changes
        commit_message = "Test commit"
        print(f"Attempting to commit changes with message: {commit_message}")
        result = self.git_ops.commit_changes(commit_message)
        print(f"Commit result: {result}")

        # Verify the commit
        latest_commit = self.git_ops.repo.head.commit
        print(f"Latest commit message: {latest_commit.message}")
        print(f"Latest commit tree blobs: {len(latest_commit.tree.blobs)}")
        self.assertEqual(latest_commit.message, commit_message)
        self.assertEqual(len(latest_commit.tree.blobs), 2)  # README.md and test_file.txt

    def test_commit_no_changes(self):
        # Try to commit when there are no changes
        result = self.git_ops.commit_changes("No changes")
        self.assertFalse(result)

    def test_commit_multiple_changes(self):
        # Create multiple files
        for i in range(3):
            file_path = os.path.join(self.temp_dir, f"file_{i}.txt")
            with open(file_path, "w") as f:
                f.write(f"Content of file {i}")

        # Commit the changes
        commit_message = "Multiple file commit"
        result = self.git_ops.commit_changes(commit_message)
        self.assertTrue(result)

        # Verify the commit
        latest_commit = self.git_ops.repo.head.commit
        self.assertEqual(latest_commit.message, commit_message)
        self.assertEqual(len(latest_commit.tree.blobs), 4)  # README.md and 3 new files

if __name__ == '__main__':
    unittest.main()