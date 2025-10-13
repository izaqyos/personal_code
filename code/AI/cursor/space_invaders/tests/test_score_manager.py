"""
Tests for the ScoreManager class.
"""
import os
import sys
import unittest
import json
import tempfile
from unittest.mock import patch

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.score_manager import ScoreManager
from src.utils.settings import DEFAULT_HIGH_SCORE


class TestScoreManager(unittest.TestCase):
    """Tests for the ScoreManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary file for scores
        self.temp_dir = tempfile.TemporaryDirectory()
        self.score_file = os.path.join(self.temp_dir.name, "test_scores.json")
        
        # Patch the SCORE_FILE setting
        self.patcher = patch('src.utils.score_manager.SCORE_FILE', self.score_file)
        self.patcher.start()
        
        # Create a score manager
        self.score_manager = ScoreManager()
        
    def tearDown(self):
        """Tear down test fixtures."""
        # Stop the patcher
        self.patcher.stop()
        
        # Clean up the temporary directory
        self.temp_dir.cleanup()
        
    def test_initial_score(self):
        """Test that initial score is zero."""
        self.assertEqual(self.score_manager.get_current_score(), 0)
        
    def test_update_score(self):
        """Test updating the score."""
        self.score_manager.update_current_score(10)
        self.assertEqual(self.score_manager.get_current_score(), 10)
        
        self.score_manager.update_current_score(20)
        self.assertEqual(self.score_manager.get_current_score(), 30)
        
    def test_reset_score(self):
        """Test resetting the score."""
        self.score_manager.update_current_score(50)
        self.score_manager.reset_current_score()
        self.assertEqual(self.score_manager.get_current_score(), 0)
        
    def test_add_score(self):
        """Test adding a score to the high scores."""
        # Add a score
        self.score_manager.add_score(100)
        
        # Check that it was added to the recent scores
        recent_scores = self.score_manager.get_recent_scores()
        self.assertEqual(len(recent_scores), 1)
        self.assertEqual(recent_scores[0]["score"], 100)
        
    def test_high_score(self):
        """Test setting a new high score."""
        # Initial high score should be the default
        self.assertEqual(self.score_manager.get_high_score(), DEFAULT_HIGH_SCORE)
        
        # Add a higher score
        is_high_score = self.score_manager.add_score(200)
        
        # Check that it's a new high score
        self.assertTrue(is_high_score)
        self.assertEqual(self.score_manager.get_high_score(), 200)
        
        # Add a lower score
        is_high_score = self.score_manager.add_score(150)
        
        # Check that it's not a new high score
        self.assertFalse(is_high_score)
        self.assertEqual(self.score_manager.get_high_score(), 200)
        
    def test_persistence(self):
        """Test that scores are persisted to disk."""
        # Add some scores
        self.score_manager.add_score(300)
        self.score_manager.add_score(200)
        
        # Create a new score manager (which should load from disk)
        new_score_manager = ScoreManager()
        
        # Check that it loaded the correct high score
        self.assertEqual(new_score_manager.get_high_score(), 300)
        
        # Check that it loaded the correct recent scores
        recent_scores = new_score_manager.get_recent_scores()
        self.assertEqual(len(recent_scores), 2)
        
        # Scores should be sorted by value (highest first)
        self.assertEqual(recent_scores[0]["score"], 300)
        self.assertEqual(recent_scores[1]["score"], 200)
        
        
if __name__ == "__main__":
    unittest.main() 