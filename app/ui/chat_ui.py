import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000/ai"

st.title("AI Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize user_input in session_state if it doesn't exist
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Use a form to better handle input submission
with st.form("chat_form"):
    prompt = st.text_input("Ask something...", value=st.session_state.user_input, key="input_field")
    submitted = st.form_submit_button("Send", type="primary")

    if submitted:
        if prompt.strip():
            st.session_state.chat_history.append(("user", prompt))

            with st.spinner("Thinking..."):
                try:
                    response = requests.post(API_URL, json={"prompt": prompt})
                    if response.status_code == 200:
                        result = response.json().get("response", "No response")
                        st.session_state.chat_history.append(("bot", result))
                    else:
                        st.session_state.chat_history.append(("bot", f"Error: {response.text}"))
                except requests.exceptions.RequestException as e:
                    st.session_state.chat_history.append(("bot", f"Connection error: {e}"))

            # Clear the input after submission
            st.session_state.user_input = ""
            st.rerun()
        else:
            st.warning("Please enter a question")

# Display chat history
for sender, message in reversed(st.session_state.chat_history):
    if sender == "user":
        st.markdown(
            f"<div style='text-align: right; color: lightgreen; margin-bottom: 10px;'>🧑‍💻 {message}</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div style='text-align: left; color: lightblue; margin-bottom: 10px;'>🤖 {message}</div>",
            unsafe_allow_html=True,
        )