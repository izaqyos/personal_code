import streamlit as st
import pandas as pd
import numpy as np
import time
import altair as alt

st.title("Advanced Streamlit Widgets Demo")

st.header("1. Progress Bar")
progress_bar = st.progress(0)
for i in range(100):
    progress_bar.progress(i + 1)
    time.sleep(0.01)  # Speed up for demo
st.success("Progress completed!")

st.header("2. Celebration Animations")
col1, col2 = st.columns(2)
with col1:
    if st.button("Show Balloons"):
        st.balloons()
with col2:
    if st.button("Show Snow"):
        st.snow()

st.header("3. Status Elements")
st.error("This is an error message")
st.warning("This is a warning message")
st.info("This is an informational message")
st.success("This is a success message")

st.header("4. Metric Display")
col1, col2, col3 = st.columns(3)
col1.metric(label="Temperature", value="70 °F", delta="1.2 °F")
col2.metric(label="Humidity", value="86%", delta="-4%")
col3.metric(label="AQI", value="23", delta="-8")

st.header("5. Data Display")
# Create sample dataframe
df = pd.DataFrame(
    np.random.randn(10, 5),
    columns=("Col %d" % i for i in range(5))
)

st.subheader("Interactive DataFrame")
st.dataframe(df, use_container_width=True)

st.subheader("Static Table")
st.table(df.head(3))

st.subheader("JSON Display")
st.json({
    "name": "John Doe",
    "age": 30,
    "city": "New York",
    "skills": ["Python", "Streamlit", "Data Science"],
    "experience": {
        "company": "Tech Co",
        "years": 5
    }
})

st.header("6. Media Elements")
st.subheader("Image Display")
st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=200)

st.subheader("Video Display")
st.video("https://www.youtube.com/watch?v=B2iAodr0fOo")

st.header("7. Forms")
with st.form("user_form"):
    st.subheader("User Information Form")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, step=1)
    satisfaction = st.slider("Satisfaction", 0, 10, 5)
    
    # Form submit button
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.write(f"Hello {name}, you're {age} years old with satisfaction level {satisfaction}/10")

st.header("8. Caching for Performance")
@st.cache_data
def expensive_computation(param):
    time.sleep(1)  # Simulate an expensive computation
    return param * 2

slider_value = st.slider("Set value for cached computation", 1, 10, 5)
result = expensive_computation(slider_value)
st.write(f"Result of computation: {result}")
st.info("The function is cached, so it only runs when the parameter changes")

st.header("9. Layout Control with Containers")
container = st.container()
container.write("This is written inside the container first")

st.write("This is written outside and appears above the container")

container.write("This is added to the container later but still appears in the container")

st.header("10. State Callbacks")
if "count" not in st.session_state:
    st.session_state.count = 0

def increment_counter():
    st.session_state.count += 1

def decrement_counter():
    st.session_state.count -= 1

col1, col2 = st.columns(2)
with col1:
    st.button("Increment", on_click=increment_counter)
with col2:
    st.button("Decrement", on_click=decrement_counter)

st.write(f"Count: {st.session_state.count}")

st.header("11. Chat Elements")
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
prompt = st.chat_input("Say something")
if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.write(prompt)
    
    # Add AI response to chat history
    response = f"Echo: {prompt}"
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Display AI response in chat message container
    with st.chat_message("assistant"):
        st.write(response)

st.header("12. Interactive Charts")
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
chart = alt.Chart(chart_data).mark_circle().encode(
    x="a", y="b", size="c", color="c", tooltip=["a", "b", "c"]
)
st.altair_chart(chart, use_container_width=True)

st.header("13. Toggle and Switch")
toggle = st.toggle("Enable feature")
st.write(f"Feature enabled: {toggle}")

st.header("14. File Download")
text_content = "This is a text file generated for download."
st.download_button(
    label="Download Text File",
    data=text_content,
    file_name="streamlit_download.txt",
    mime="text/plain"
)

# Generate sample CSV
csv_data = pd.DataFrame({
    'Name': ['John', 'Mary', 'Bob'],
    'Age': [30, 25, 40]
}).to_csv(index=False)

st.download_button(
    label="Download CSV File",
    data=csv_data,
    file_name="sample_data.csv",
    mime="text/csv"
)

st.header("15. Sidebar")
with st.sidebar:
    st.title("Sidebar Controls")
    selected_page = st.radio("Go to", ["Home", "About", "Settings"])
    st.write(f"You selected: {selected_page}")
    
    st.divider()
    
    st.slider("Sidebar Slider", 0, 100, 50)
