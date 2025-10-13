# Streamlit AI Assistant Tutorial

This project demonstrates how to build user interfaces for AI assistants, chatbots, and other AI applications using Streamlit.

## Project Structure

- `app.py`: Main application entry point
- `pages/`: Directory containing different example pages
  - `1_simple_chat.py`: Basic chatbot interface
  - `2_advanced_chat.py`: Advanced chat with memory and context
  - `3_document_qa.py`: Document Q&A interface
  - `4_data_visualization.py`: Data visualization with AI insights
- `utils/`: Utility functions and helpers
  - `openai_helper.py`: OpenAI API integration functions
  - `ui_components.py`: Reusable UI components
- `data/`: Sample data for demos
- `styles/`: Custom CSS styles
- `.env.example`: Example environment variables file

## Getting Started

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and add your API keys
4. Run the application:
   ```
   streamlit run app.py
   ```

## Features

- Basic and advanced chat interfaces
- Document question answering
- Interactive data visualization 
- Custom UI components
- Session state management
- User authentication examples
- API integration patterns

## Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [Streamlit Components](https://streamlit.io/components) 