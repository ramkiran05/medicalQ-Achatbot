import streamlit as st
import requests
import uuid  # Used to generate random, hidden IDs for the backend

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Medical Q&A Assistant", page_icon="💊")

# 1. GENERATE HIDDEN IDs IN THE BACKGROUND
# If this is the user's first time opening the page, we create silent IDs for them.
if "user_id" not in st.session_state:
    st.session_state.user_id = f"user_{uuid.uuid4().hex[:8]}"
if "session_id" not in st.session_state:
    st.session_state.session_id = f"session_{uuid.uuid4().hex[:8]}"
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Medical Q&A Assistant 💊")

# --- SIDEBAR: Clean and Simple ---
with st.sidebar:
    st.header("Upload Medical Document")
    st.write("Upload a PDF to ask specific questions about it.")
    
    uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])
    
    if st.button("Process Document"):
        if uploaded_file is not None:
            with st.spinner("Uploading and analyzing document..."):
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                # We pull the invisible user_id from the session state
                data = {"user_id": st.session_state.user_id}
                
                try:
                    response = requests.post(f"{API_URL}/upload", files=files, data=data)
                    if response.status_code == 200:
                        st.success("Document analyzed successfully! You can now ask questions.")
                    else:
                        st.error(f"Backend Error: {response.text}")
                except Exception as e:
                    st.error(f"Connection failed: {e}")
        else:
            st.warning("Please upload a PDF first.")

# --- MAIN CHAT INTERFACE ---
# Redraw previous chat messages on every screen refresh
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input box
if prompt := st.chat_input("Ask a medical question..."):
    
    # Display user's question
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Fetch streamed answer from FastAPI
    with st.chat_message("assistant"):
        # We silently package the hidden IDs into the payload
        payload = {
            "user_id": st.session_state.user_id,
            "session_id": st.session_state.session_id,
            "question": prompt
        }
        
        try:
            res = requests.post(f"{API_URL}/chat", json=payload, stream=True)
            
            if res.status_code == 200:
                def stream_parser():
                    for chunk in res.iter_content(chunk_size=None, decode_unicode=True):
                        if chunk:
                            yield chunk
                            
                # Stream the response word-by-word
                reply = st.write_stream(stream_parser())
                st.session_state.messages.append({"role": "assistant", "content": reply})
            else:
                st.error(f"Backend Error: {res.text}")
                
        except Exception as e:
            st.error(f"Backend connection failed. Is FastAPI running? Error: {e}")