import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

class MagicDemo:
    """
    A class to demonstrate various Streamlit magic commands.
    Each method showcases different types of magic command usage.
    """
    
    def __init__(self):
        self.sample_data = pd.DataFrame({
            'A': np.random.randn(10),
            'B': np.random.randn(10),
            'C': np.random.randn(10)
        })
    
    def text_magic_demo(self):
        """Demonstrates magic commands with text and strings."""
        "# Text Magic Demo"
        
        "## Basic String Magic"
        "This is a simple magic string!"
        
        # Variable magic
        greeting = "Hello from a magic variable!"
        greeting
        
        # F-string magic
        name = "Streamlit"
        f"Welcome to {name} magic commands!"
        
        # Multiline string magic
        """
        ## Markdown Magic
        This is a **multiline string** that gets rendered as *Markdown*.
        
        - Magic bullet point 1
        - Magic bullet point 2
        - Magic bullet point 3
        
        You can even include `code snippets` and [links](https://streamlit.io)!
        """
    
    def number_magic_demo(self):
        """Demonstrates magic commands with numbers and calculations."""
        "# Number Magic Demo"
        
        "## Simple Numbers"
        42
        3.14159
        
        "## Calculations"
        2 + 2
        10 * 5
        2 ** 8
        
        # Variable calculations
        result = 15 * 3
        result
        
        # Complex expressions
        import math
        math.sqrt(16)
        math.pi * 2
        
        # List comprehension magic
        [x**2 for x in range(5)]
    
    def data_structure_magic_demo(self):
        """Demonstrates magic commands with data structures."""
        "# Data Structure Magic Demo"
        
        "## Lists and Tuples"
        [1, 2, 3, 4, 5]
        (10, 20, 30)
        
        "## Dictionaries"
        {"name": "Alice", "age": 30, "city": "New York"}
        
        "## Sets"
        {1, 2, 3, 4, 5}
        
        "## Nested Structures"
        {
            "users": [
                {"name": "John", "score": 95},
                {"name": "Jane", "score": 87},
                {"name": "Bob", "score": 92}
            ],
            "total_users": 3
        }
    
    def dataframe_magic_demo(self):
        """Demonstrates magic commands with pandas DataFrames."""
        "# DataFrame Magic Demo"
        
        "## Sample DataFrame"
        self.sample_data
        
        "## DataFrame Operations"
        self.sample_data.head()
        self.sample_data.describe()
        self.sample_data.corr()
        
        "## Creating DataFrames with Magic"
        pd.DataFrame({
            'Product': ['Apple', 'Banana', 'Orange'],
            'Price': [1.20, 0.50, 0.80],
            'Stock': [100, 150, 75]
        })
        
        "## NumPy Arrays"
        np.array([1, 2, 3, 4, 5])
        np.random.randn(3, 3)
    
    def chart_magic_demo(self):
        """Demonstrates magic commands with charts and plots."""
        "# Chart Magic Demo"
        
        "## Simple Line Chart Data"
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['Line A', 'Line B', 'Line C']
        )
        chart_data
        
        "## Matplotlib Figure Magic"
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(range(10), [x**2 for x in range(10)], 'b-', label='x²')
        ax.plot(range(10), [x**1.5 for x in range(10)], 'r--', label='x^1.5')
        ax.set_title('Magic Matplotlib Plot')
        ax.set_xlabel('X values')
        ax.set_ylabel('Y values')
        ax.legend()
        ax.grid(True)
        fig
        
        plt.close(fig)  # Clean up to avoid memory issues
    
    def conditional_magic_demo(self):
        """Demonstrates magic commands with conditional logic."""
        "# Conditional Magic Demo"
        
        show_details = st.checkbox("Show detailed information")
        
        if show_details:
            "## Detailed Information"
            "You chose to see the details!"
            
            details = {
                "timestamp": datetime.datetime.now(),
                "user_choice": "show_details",
                "random_number": np.random.randint(1, 100)
            }
            details
        else:
            "Check the box above to see detailed information."
        
        # Magic with user input
        user_name = st.text_input("Enter your name:", "")
        if user_name:
            f"Hello, {user_name}! Nice to meet you."
            f"Your name has {len(user_name)} characters."
    
    def mixed_magic_demo(self):
        """Demonstrates mixing magic commands with explicit Streamlit commands."""
        st.title("Mixed Magic and Explicit Commands Demo")
        
        "## This section uses magic for quick display"
        
        # Magic for quick data display
        sample_metrics = {
            "Total Users": 1250,
            "Active Sessions": 89,
            "Revenue": "$12,450"
        }
        sample_metrics
        
        # Explicit command for specific formatting
        st.subheader("Detailed Metrics (using explicit commands)")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Users", "1,250", "12%")
        with col2:
            st.metric("Active Sessions", "89", "-2%")
        with col3:
            st.metric("Revenue", "$12,450", "8%")
        
        "## Back to magic for simple displays"
        "Magic commands are great for rapid prototyping and data exploration!"
        
        # Magic with calculations
        current_time = datetime.datetime.now()
        f"Current time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def run_all_demos(self):
        """Runs all magic command demonstrations."""
        st.title("🎩 Streamlit Magic Commands Demonstration")
        
        st.write("This demo showcases various ways to use Streamlit's magic commands.")
        
        demo_choice = st.selectbox(
            "Choose a demo to run:",
            [
                "All Demos",
                "Text Magic",
                "Number Magic", 
                "Data Structure Magic",
                "DataFrame Magic",
                "Chart Magic",
                "Conditional Magic",
                "Mixed Magic & Explicit"
            ]
        )
        
        if demo_choice == "All Demos":
            self.text_magic_demo()
            st.divider()
            self.number_magic_demo()
            st.divider()
            self.data_structure_magic_demo()
            st.divider()
            self.dataframe_magic_demo()
            st.divider()
            self.chart_magic_demo()
            st.divider()
            self.conditional_magic_demo()
            st.divider()
            self.mixed_magic_demo()
        elif demo_choice == "Text Magic":
            self.text_magic_demo()
        elif demo_choice == "Number Magic":
            self.number_magic_demo()
        elif demo_choice == "Data Structure Magic":
            self.data_structure_magic_demo()
        elif demo_choice == "DataFrame Magic":
            self.dataframe_magic_demo()
        elif demo_choice == "Chart Magic":
            self.chart_magic_demo()
        elif demo_choice == "Conditional Magic":
            self.conditional_magic_demo()
        elif demo_choice == "Mixed Magic & Explicit":
            self.mixed_magic_demo()

def main():
    """Main function to run the magic demo."""
    demo = MagicDemo()
    demo.run_all_demos()

if __name__ == "__main__":
    main() 