import streamlit as st

st.title("Basic Widgets Demo")

# text input
text_input = st.text_input("Enter your name")
st.write(f"Hello, {text_input}!")

# number input
number_input = st.number_input("Enter a number", value=0, step=1, format="%d", label_visibility="visible")
st.write(f"You entered: {number_input}")

# slider
slider = st.slider("Select a value", min_value=0, max_value=100, value=50, step=1)
st.write(f"You selected: {slider}")

# checkbox
checkbox = st.checkbox("I agree")
st.write(f"You selected: {checkbox}")

# radio button
radio = st.radio("Select an option", ["Option 1", "Option 2", "Option 3"])
st.write(f"You selected: {radio}")

# select box
select_box = st.selectbox("Select an option", ["Option 1", "Option 2", "Option 3"])
st.write(f"You selected: {select_box}")

# multiselect
multiselect = st.multiselect("Select multiple options", ["Option 1", "Option 2", "Option 3"])
st.write(f"You selected: {multiselect}")

# date input
date_input = st.date_input("Select a date")
st.write(f"You selected: {date_input}")

# time input
time_input = st.time_input("Select a time")
st.write(f"You selected: {time_input}")

#file uploader
file_uploader = st.file_uploader("Upload a file")
st.write(f"You uploaded: {file_uploader}")

#color picker
color_picker = st.color_picker("Select a color")
st.write(f"You selected: {color_picker}")

#expander
expander = st.expander("Click to expand")
expander.write("This is an expander")

#spinner
spinner = st.spinner("Loading...")

#tabs
tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])
tab1.write("This is tab 1")
tab2.write("This is tab 2")
tab3.write("This is tab 3")

#columns for layout
col1, col2, col3 = st.columns(3)
col1.write("This is column 1")
col2.write("This is column 2")
col3.write("This is column 3")







