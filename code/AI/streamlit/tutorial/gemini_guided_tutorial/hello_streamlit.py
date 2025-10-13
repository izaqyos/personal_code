import streamlit as st
import os
from datetime import datetime
import socket

st.title("My First Streamlit App")

st.write("Hello, Streamlit World!")

st.write(f"This is running inside a Conda environment. {os.environ['CONDA_PREFIX']}")
st.write(f"Streamlit version: {st.__version__}")

#print user name, hostname, and pretty print date and time
st.write(f"User: {os.getlogin()}")
st.write(f"Hostname: {socket.gethostname()}")
st.write(f"Date and Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

#add a button to the app that displays click count, capture more than just first click
if 'click_count' not in st.session_state:
    st.session_state.click_count = 0

if st.button("Click me!"):
    st.session_state.click_count += 1

st.write(f"Click count: {st.session_state.click_count}")
