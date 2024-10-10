import os
import tempfile
import unittest
from ai_feature_branch_toolbox.git_operations import GitOperations

class TestSwitchBranch(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.git_ops = GitOperations()
        self.git_ops.initialize_repo(self.temp_dir)

    def tearDown(self):
        self.git_ops.close_repo()
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.temp_dir)

    def test_switch_branch(self):
        # Create a new feature branch
        self.git_ops.create_feature_branch("feature-1")

        # Switch back to main branch
        result = self.git_ops.switch_branch("master")
        self.assertTrue(result)
        self.assertEqual(self.git_ops.repo.active_branch.name, "master")

        # Switch to the feature branch
        result = self.git_ops.switch_branch("feature-1")
        self.assertTrue(result)
        self.assertEqual(self.git_ops.repo.active_branch.name, "feature-1")

        # Try to switch to a non-existent branch
        result = self.git_ops.switch_branch("non-existent-branch")
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()