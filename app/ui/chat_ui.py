import streamlit as st
import requests

# Flask endpoint
API_URL = "http://127.0.0.1:5000/ai"  # Update if your Flask runs on a different port

st.title("Chat with AI")

# Input prompt
prompt = st.text_area("Enter your question", height=150)

if st.button("Ask"):
    if prompt.strip():
        with st.spinner("Fetching response..."):
            response = requests.post(API_URL, json={"prompt": prompt})
            if response.status_code == 200:
                result = response.json().get("response", "No response")
                st.success(result)
            else:
                st.error("Error from server: " + response.text)
