import os
import tempfile
import unittest
import logging
from ai_feature_branch_toolbox.git_operations import GitOperations

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestMergeFeatureBranch(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.git_ops = GitOperations()
        self.git_ops.initialize_repo(self.temp_dir)

    def tearDown(self):
        self.git_ops.close_repo()
        import time
        time.sleep(0.1)

        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for name in files:
                try:
                    os.chmod(os.path.join(root, name), 0o666)
                    os.remove(os.path.join(root, name))
                except PermissionError:
                    logger.warning(f"Unable to remove file: {os.path.join(root, name)}")
            for name in dirs:
                try:
                    os.rmdir(os.path.join(root, name))
                except PermissionError:
                    logger.warning(f"Unable to remove directory: {os.path.join(root, name)}")

        try:
            os.rmdir(self.temp_dir)
        except PermissionError:
            logger.warning(f"Unable to remove temporary directory: {self.temp_dir}")

    def test_merge_feature_branch(self):
        logger.info("Starting test_merge_feature_branch")

        # Create a feature branch and make changes
        logger.info("Creating feature branch")
        self.git_ops.create_feature_branch('feature-branch')

        logger.info("Creating feature file")
        with open(os.path.join(self.temp_dir, 'feature_file.txt'), 'w') as f:
            f.write('Feature content')

        logger.info("Committing changes")
        self.git_ops.commit_changes('Add feature file')

        # Switch back to main branch
        logger.info("Switching back to main branch")
        self.git_ops.switch_branch('main')

        # Merge feature branch into main
        logger.info("Merging feature branch into main")
        result = self.git_ops.merge_feature_branch('feature-branch')
        logger.info(f"Merge result: {result}")
        self.assertTrue(result)

        # Verify that the changes are reflected in the main branch
        logger.info("Verifying changes in main branch")
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'feature_file.txt')))
        with open(os.path.join(self.temp_dir, 'feature_file.txt'), 'r') as f:
            content = f.read()
        logger.info(f"Content of feature_file.txt: {content}")
        self.assertEqual(content, 'Feature content')

        logger.info("test_merge_feature_branch completed successfully")

if __name__ == '__main__':
    unittest.main()