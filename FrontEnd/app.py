import streamlit as st
import requests
import re

st.title("YouTube Video Chatbot")

# Initialize session state variables
if "api_key" not in st.session_state:
    st.session_state["api_key"] = ""

if "api_key_submitted" not in st.session_state:
    st.session_state["api_key_submitted"] = False

if "video_url" not in st.session_state:
    st.session_state["video_url"] = ""

if "video_submitted" not in st.session_state:
    st.session_state["video_submitted"] = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "start_seconds" not in st.session_state:
    st.session_state.start_seconds = 0

# Backend URL
backend_url = "http://127.0.0.1:8000"

# Input field for API key
if not st.session_state["api_key_submitted"]:
    st.session_state["api_key"] = st.text_input("Enter your OpenAI API key", type="password")
    if st.session_state["api_key"]:
        response = requests.post(f"{backend_url}/set_openai_api_key/", json={"api_key": st.session_state["api_key"]})
        if response.status_code == 200:
            st.session_state["api_key_submitted"] = True
            st.rerun()  # Rerun the script to hide the API key form

# Input field for YouTube video URL
if st.session_state["api_key_submitted"] and not st.session_state["video_submitted"]:
    st.session_state["video_url"] = st.text_input("Enter YouTube Video URL")
    if st.session_state["video_url"]:
        response = requests.post(f"{backend_url}/load_youtube_transcript/", json={"url": st.session_state["video_url"]})
        if response.status_code == 200:
            st.session_state["video_submitted"] = True
            st.rerun()  # Rerun the script to hide the video URL form

if st.session_state["api_key_submitted"] and st.session_state["video_submitted"]:
    # Display the video
    video_placeholder = st.empty()
    video_placeholder.video(st.session_state["video_url"])

    @st.dialog("Watch in Video")
    def watch_in_video_dialog(start_seconds):
        st.write("Playing the video...")
        start=str(start_seconds)+'s'
        st.video(st.session_state["video_url"], start_time=start)

    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant":
                if st.button(f"Watch in Video", key=f"watch_{i}"):
                    watch_in_video_dialog(st.session_state.start_seconds)

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = requests.post(f"{backend_url}/process_input_message/", json={"message": prompt})
        if response.status_code == 200:
            response_data = response.json()
            response_text = response_data.get("message", "No response received.")
            st.session_state.messages.append({"role": "assistant", "content": response_text})

            # Extract start_seconds from the response text
            match = re.search(r"\(start_seconds: (\d+)\)", response_text)
            if match:
                st.session_state.start_seconds = int(match.group(1))

            st.rerun()  # Rerun the script to update the UI with the new response