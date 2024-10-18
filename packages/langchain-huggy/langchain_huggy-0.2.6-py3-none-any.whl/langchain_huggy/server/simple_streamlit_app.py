from typing import Generator

import streamlit as st
import requests


def get_api_response(prompt, stream=True,url = "http://0.0.0.0:11435/v1/generate") -> Generator:
    data = {
        "prompt": prompt,
        "stream": stream
    }
    response = requests.post(url, json=data, stream=stream)
    for chunk in response.iter_content(decode_unicode=True):
        if chunk:
            yield chunk

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
            full_response+=message_placeholder.write_stream(get_api_response(prompt))
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    streamlit_app()