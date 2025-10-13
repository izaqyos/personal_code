import ollama
import streamlit as st

st.title("Yosi's Chatbot. All local LLMs!!")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "models" not in st.session_state:
    st.session_state["models"] = ""
models = [model['name'] for model in ollama.list()['models']]    
st.session_state["models"] = st.selectbox("Select model", models)

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
def model_resp_gen():
    stream = ollama.chat(
        model=st.session_state["models"],
        messages=st.session_state["messages"],
        stream=True,
    )
    for chunk in stream:
        yield chunk["message"]["content"]
    
# use wallrus operator to assign in expression
if prompt := st.chat_input("Ask away :) "):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    #streamlit already has useful chat input and chat message functions for "user" and "assistant" roles
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Not stream handling:
        #response = ollama.chat(
        #    model=st.session_state["models"],
        #    messages=st.session_state["messages"],
        #    stream=False,
        #)
        #message = response["message"]["content"]
        #st.markdown(message)

        #stream handling
        message = st.write_stream(model_resp_gen())
        st.session_state["messages"].append({"role": "assistant", "content": message})
        