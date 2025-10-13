import streamlit as st
import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import json

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.claude_helper import get_claude_response, format_messages

# Page configuration
st.set_page_config(
    page_title="Data Visualization | AI Assistant Tutorial",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 AI-Enhanced Data Visualization")

# Description
st.markdown("""
This example demonstrates how to integrate AI with data visualization.
Upload data, get AI-generated insights, and create interactive visualizations.

Key features:
- Data upload and inspection
- AI-generated data analysis
- Interactive visualization suggestions
- Custom plotting capabilities
""")

# Add a divider
st.divider()

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = None
if "analysis" not in st.session_state:
    st.session_state.analysis = None
if "viz_code" not in st.session_state:
    st.session_state.viz_code = None

# Create sample data
def create_sample_data():
    # Create sample sales data
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
    
    # Product categories
    categories = ['Electronics', 'Clothing', 'Home Goods', 'Sports', 'Books']
    
    # Create dataframe
    data = []
    for date in dates:
        for category in categories:
            # Base sales with some seasonality
            base_sales = 100 + 50 * np.sin(date.dayofyear / 365 * 2 * np.pi)
            
            # Add category effect
            if category == 'Electronics':
                category_factor = 2.0
            elif category == 'Clothing':
                category_factor = 1.5
            elif category == 'Home Goods':
                category_factor = 1.2
            elif category == 'Sports':
                category_factor = 0.8
            else:  # Books
                category_factor = 0.6
            
            # Add weekend effect
            weekend_factor = 1.3 if date.dayofweek >= 5 else 1.0
            
            # Add holiday effect (simple proxy for major holidays)
            holiday_factor = 1.5 if date.month in [1, 7, 11, 12] and date.day in [1, 4, 15, 25] else 1.0
            
            # Calculate final sales with some randomness
            sales = base_sales * category_factor * weekend_factor * holiday_factor
            sales = max(10, sales * np.random.normal(1, 0.1))
            
            # Calculate profit (as a function of sales with some category variation)
            profit_margin = 0.2 if category == 'Electronics' else 0.3 if category == 'Books' else 0.25
            profit = sales * profit_margin * np.random.normal(1, 0.05)
            
            # Add to data
            data.append({
                'date': date,
                'category': category,
                'sales': round(sales, 2),
                'profit': round(profit, 2),
                'is_weekend': date.dayofweek >= 5,
                'month': date.month_name(),
                'day_of_week': date.day_name()
            })
    
    return pd.DataFrame(data)

# Sidebar configuration
with st.sidebar:
    st.subheader("Data Source")
    data_source = st.radio(
        "Select Data Source",
        ["Upload CSV", "Sample Data"],
        index=1
    )
    
    if data_source == "Upload CSV":
        uploaded_file = st.file_uploader("Upload CSV", type="csv")
        if uploaded_file is not None:
            try:
                st.session_state.data = pd.read_csv(uploaded_file)
                st.success("Data loaded successfully!")
            except Exception as e:
                st.error(f"Error loading data: {str(e)}")
    else:
        if st.button("Generate Sample Data"):
            st.session_state.data = create_sample_data()
            st.success("Sample data generated!")
    
    st.subheader("AI Analysis")
    model = st.selectbox(
        "Select Model",
        ["gpt-4-turbo", "gpt-3.5-turbo"],
        index=1
    )

# Main content
if st.session_state.data is not None:
    # Data preview
    st.subheader("Data Preview")
    st.dataframe(st.session_state.data.head())
    
    # Data info
    with st.expander("Data Information"):
        # Display column info
        cols = list(st.session_state.data.columns)
        st.write(f"Columns: {', '.join(cols)}")
        
        # Display basic stats
        st.write(f"Shape: {st.session_state.data.shape[0]} rows, {st.session_state.data.shape[1]} columns")
        
        # Display dtypes
        st.write("Data Types:")
        st.write(st.session_state.data.dtypes)
    
    # Data analysis with AI
    st.subheader("AI Data Analysis")
    
    if st.button("Generate AI Analysis"):
        with st.spinner("Analyzing data..."):
            # Create a data description for the AI
            data_info = {
                "columns": list(st.session_state.data.columns),
                "shape": st.session_state.data.shape,
                "dtypes": str(st.session_state.data.dtypes),
                "summary": st.session_state.data.describe().to_dict(),
                "sample": st.session_state.data.head(5).to_dict()
            }
            
            # Create prompt for data analysis
            prompt = f"""
            You are a data analyst. Analyze this dataset and provide insights:
            
            Dataset Information:
            {json.dumps(data_info, indent=2)}
            
            Please provide:
            1. A summary of the dataset 
            2. Key insights and patterns you observe
            3. 3-5 specific visualization suggestions with explanations of what they would reveal
            
            Format the visualization suggestions as a numbered list. For each suggestion, explain what type of chart to use,
            which columns to include, and what insights we might gain from it.
            """
            
            # Get analysis from Claude
            messages = [{"role": "system", "content": prompt}]
            analysis = get_claude_response(
                messages=messages,
                model=model,
                temperature=0.3
            )
            
            st.session_state.analysis = analysis
    
    # Display analysis
    if st.session_state.analysis:
        st.markdown(st.session_state.analysis)
    
    # Visualization section
    st.subheader("Visualizations")
    
    # Visualization options
    viz_options = st.radio(
        "Select Visualization Method",
        ["Quick Charts", "AI-Generated Chart", "Custom Chart"],
        horizontal=True
    )
    
    if viz_options == "Quick Charts":
        # Simple built-in visualizations
        if 'category' in st.session_state.data.columns and 'sales' in st.session_state.data.columns:
            # Group by category
            category_sales = st.session_state.data.groupby('category')['sales'].sum().reset_index()
            
            # Create bar chart
            st.subheader("Sales by Category")
            fig = px.bar(
                category_sales, 
                x='category', 
                y='sales',
                color='category',
                title='Total Sales by Category'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Create line chart if time data is available
            if 'date' in st.session_state.data.columns:
                st.subheader("Sales Over Time")
                time_sales = st.session_state.data.groupby('date')['sales'].sum().reset_index()
                fig = px.line(
                    time_sales, 
                    x='date', 
                    y='sales',
                    title='Total Sales Over Time'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Create heatmap if we have day_of_week
                if 'day_of_week' in st.session_state.data.columns and 'month' in st.session_state.data.columns:
                    st.subheader("Sales Heatmap by Day and Month")
                    heatmap_data = st.session_state.data.groupby(['day_of_week', 'month'])['sales'].mean().reset_index()
                    heatmap_data_pivot = heatmap_data.pivot(index='day_of_week', columns='month', values='sales')
                    
                    # Sort days of week in proper order
                    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    heatmap_data_pivot = heatmap_data_pivot.reindex(day_order)
                    
                    fig = px.imshow(
                        heatmap_data_pivot,
                        title='Average Sales by Day of Week and Month',
                        color_continuous_scale='viridis'
                    )
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Data must contain 'category' and 'sales' columns for quick charts.")
            
    elif viz_options == "AI-Generated Chart":
        # Let AI generate a chart with code
        st.markdown("Let the AI generate a custom visualization based on your data:")
        viz_prompt = st.text_area(
            "Describe what visualization you want",
            "Show me a chart comparing total sales and profit by category with proper labels and colors"
        )
        
        if st.button("Generate Visualization"):
            with st.spinner("Generating visualization..."):
                # Create data description for the AI
                data_sample = st.session_state.data.head(5).to_dict()
                columns = list(st.session_state.data.columns)
                
                # Create prompt for chart generation
                prompt = f"""
                You are a data visualization expert. Generate a Python code snippet using Plotly Express to create
                the visualization described below. The code should be complete and ready to run.
                
                User's visualization request: "{viz_prompt}"
                
                Available data columns: {columns}
                Sample data: {json.dumps(data_sample, indent=2)}
                
                Instructions:
                1. Use only Plotly Express (import plotly.express as px)
                2. Assume the DataFrame is already loaded and named 'data'
                3. Include appropriate titles, labels, and styling
                4. Return ONLY the Python code, nothing else
                5. Your code must be complete and executable as-is
                6. Do not include import statements or DataFrame loading
                7. Generate a figure named 'fig' that can be displayed with st.plotly_chart(fig)
                """
                
                # Get code from Claude
                messages = [{"role": "system", "content": prompt}]
                viz_code = get_claude_response(
                    messages=messages,
                    model=model,
                    temperature=0.2
                )
                
                # Store the code
                st.session_state.viz_code = viz_code
                
                # Display the code
                with st.expander("Generated Code"):
                    st.code(viz_code, language="python")
                
                # Try to execute the code
                try:
                    # Define data for the context
                    data = st.session_state.data
                    
                    # Execute code
                    local_vars = {"data": data, "px": px, "go": go, "plt": plt, "np": np, "pd": pd}
                    exec(viz_code, globals(), local_vars)
                    
                    # Display the chart
                    if 'fig' in local_vars:
                        st.plotly_chart(local_vars['fig'], use_container_width=True)
                    else:
                        st.error("Code did not generate a 'fig' variable.")
                except Exception as e:
                    st.error(f"Error executing visualization code: {str(e)}")
        
        # Display previously generated chart
        elif st.session_state.viz_code:
            with st.expander("Generated Code"):
                st.code(st.session_state.viz_code, language="python")
            
            try:
                # Define data for the context
                data = st.session_state.data
                
                # Execute code
                local_vars = {"data": data, "px": px, "go": go, "plt": plt, "np": np, "pd": pd}
                exec(st.session_state.viz_code, globals(), local_vars)
                
                # Display the chart
                if 'fig' in local_vars:
                    st.plotly_chart(local_vars['fig'], use_container_width=True)
            except Exception as e:
                st.error(f"Error executing visualization code: {str(e)}")
                
    else:  # Custom Chart
        # Allow users to build their own chart
        st.markdown("Build your own custom chart:")
        
        # Get available columns
        columns = list(st.session_state.data.columns)
        numeric_columns = st.session_state.data.select_dtypes(include=np.number).columns.tolist()
        
        # Chart type selection
        chart_type = st.selectbox(
            "Select Chart Type",
            ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Box Plot", "Histogram"],
        )
        
        # Common parameters
        col1, col2 = st.columns(2)
        with col1:
            x_column = st.selectbox("X-axis", columns)
        
        with col2:
            if chart_type != "Histogram":
                y_column = st.selectbox("Y-axis", numeric_columns if numeric_columns else columns)
        
        # Optional parameters
        color_column = st.selectbox("Color By (optional)", ["None"] + columns)
        color_column = None if color_column == "None" else color_column
        
        title = st.text_input("Chart Title", f"{chart_type} of {y_column if chart_type != 'Histogram' else x_column} by {x_column if chart_type != 'Histogram' else ''}")
        
        # Create chart
        if st.button("Create Chart"):
            fig = None
            
            if chart_type == "Bar Chart":
                fig = px.bar(
                    st.session_state.data, 
                    x=x_column, 
                    y=y_column,
                    color=color_column,
                    title=title
                )
            elif chart_type == "Line Chart":
                fig = px.line(
                    st.session_state.data, 
                    x=x_column, 
                    y=y_column,
                    color=color_column,
                    title=title
                )
            elif chart_type == "Scatter Plot":
                fig = px.scatter(
                    st.session_state.data, 
                    x=x_column, 
                    y=y_column,
                    color=color_column,
                    title=title
                )
            elif chart_type == "Pie Chart":
                fig = px.pie(
                    st.session_state.data, 
                    names=x_column, 
                    values=y_column,
                    title=title
                )
            elif chart_type == "Box Plot":
                fig = px.box(
                    st.session_state.data, 
                    x=x_column, 
                    y=y_column,
                    color=color_column,
                    title=title
                )
            elif chart_type == "Histogram":
                fig = px.histogram(
                    st.session_state.data, 
                    x=x_column,
                    color=color_column,
                    title=title
                )
            
            if fig:
                st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Please upload or generate data using the sidebar controls.")

# Code explanation
with st.expander("See Code Explanation"):
    st.markdown("""
    ### Key Features of AI-Enhanced Data Visualization
    
    1. **Data Handling**:
       - CSV upload or sample data generation
       - Data inspection and summary statistics
       - Flexible data structure support
       
    2. **AI Integration**:
       - Automated data analysis with Claude
       - AI-powered visualization suggestions
       - Code generation for custom visualizations
       
    3. **Visualization Types**:
       - Quick auto-generated charts
       - AI-generated custom visualizations
       - User-configurable chart options
       
    4. **Implementation Notes**:
       - Uses Plotly for interactive visualizations
       - Executes AI-generated code safely
       - Handles errors gracefully
       - Provides multiple ways to visualize data
    """)

# Additional tips
st.warning("""
**Production Implementation Tips**:

1. Add data preprocessing and cleaning options
2. Implement more sophisticated chart customization
3. Add the ability to save and export visualizations
4. Implement caching for expensive operations
5. Add more robust error handling for AI-generated code
""") 