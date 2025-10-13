"""
Module for managing and persisting player scores.
"""
import os
import json
from typing import Dict, List, Tuple
from datetime import datetime

from src.utils.settings import SCORE_FILE, DEFAULT_HIGH_SCORE


class ScoreManager:
    """Class to manage player scores and persist them to disk."""
    
    def __init__(self):
        """Initialize the score manager."""
        self.scores = self.load_scores()
        self.current_score = 0
        
    def load_scores(self) -> Dict:
        """Load scores from the score file."""
        if not os.path.exists(SCORE_FILE):
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(SCORE_FILE), exist_ok=True)
            
            # Initialize with default values
            default_scores = {
                "high_score": DEFAULT_HIGH_SCORE,
                "recent_scores": []
            }
            
            # Save to file
            with open(SCORE_FILE, 'w') as f:
                json.dump(default_scores, f)
                
            return default_scores
        
        try:
            with open(SCORE_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # Handle corrupt or missing file
            return {
                "high_score": DEFAULT_HIGH_SCORE,
                "recent_scores": []
            }
    
    def save_scores(self) -> None:
        """Save scores to the score file."""
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(SCORE_FILE), exist_ok=True)
        
        with open(SCORE_FILE, 'w') as f:
            json.dump(self.scores, f)
    
    def add_score(self, score: int) -> bool:
        """
        Add a new score to the records.
        
        Args:
            score: The score to add
            
        Returns:
            bool: True if it's a new high score, False otherwise
        """
        is_high_score = False
        
        # Check if it's a new high score
        if score > self.scores.get("high_score", DEFAULT_HIGH_SCORE):
            self.scores["high_score"] = score
            is_high_score = True
        
        # Add to recent scores
        recent_score = {
            "score": score,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        recent_scores = self.scores.get("recent_scores", [])
        recent_scores.append(recent_score)
        
        # Keep only the 10 most recent scores
        self.scores["recent_scores"] = sorted(
            recent_scores, 
            key=lambda x: x["score"], 
            reverse=True
        )[:10]
        
        # Save to disk
        self.save_scores()
        
        return is_high_score
    
    def get_high_score(self) -> int:
        """Get the current high score."""
        return self.scores.get("high_score", DEFAULT_HIGH_SCORE)
    
    def get_recent_scores(self) -> List[Dict]:
        """Get the list of recent scores."""
        return self.scores.get("recent_scores", [])
    
    def update_current_score(self, points: int) -> None:
        """
        Update the current score.
        
        Args:
            points: Points to add to current score
        """
        self.current_score += points
    
    def reset_current_score(self) -> None:
        """Reset the current score to zero."""
        self.current_score = 0
    
    def get_current_score(self) -> int:
        """Get the current score."""
        return self.current_score 