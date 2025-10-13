import sys
import os

# Add the parent directory to the sys.path to allow imports from app.py
# This assumes 'tests' is a subdirectory of your project root where app.py is located.
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from app import main  # Assuming your main function is in app.py
import streamlit as st
from unittest.mock import patch

# Basic test to see if the main function runs without error
# More specific tests for Streamlit elements are complex and often require
# tools like streamlit-testing-library or playwright for full interaction testing.
# For now, we'll keep it simple.

@patch('streamlit.title')
@patch('streamlit.write')
def test_main_runs(mock_write, mock_title):
    """Test that the main function calls st.title and st.write."""
    main()
    mock_title.assert_called_once_with("Hello, Streamlit!")
    mock_write.assert_called_once_with("Welcome to your first Streamlit app.")

def test_placeholder():
    """A simple placeholder test that always passes."""
    assert True 