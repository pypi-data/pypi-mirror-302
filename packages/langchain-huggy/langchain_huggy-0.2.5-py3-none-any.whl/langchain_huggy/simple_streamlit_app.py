import streamlit as st
import requests
import json

API_URL = "http://0.0.0.0:11435/v1/generate"

def get_api_response(prompt, stream=True):
    data = {
        "prompt": prompt,
        "stream": stream
    }
    response = requests.post(API_URL, json=data, stream=stream)
    return response

def streamlit_app():
    st.title("Chat with Llama-3.1-Nemotron-70B")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is your message?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            # for chunk in get_api_response(prompt).iter_lines(decode_unicode=True):
            for chunk in get_api_response(prompt).iter_content(decode_unicode=True):
                if chunk:
                    chunk_data = chunk
                    full_response += chunk_data
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    streamlit_app()