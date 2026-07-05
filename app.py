import streamlit as st
import requests
import uuid  # Used to generate random, hidden IDs for the backend

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Medical Q&A Assistant",
    page_icon="💊",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# CALM DESIGN — soft, muted palette + gentle spacing (visual only, no logic)
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

        /* ---- Base canvas: soft peaceful gradient behind the glass ---- */
        html, body,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stBottom"],
        footer {
            background: transparent !important;
        }

        .stApp {
            background: linear-gradient(135deg, #dff3ee 0%, #e3ecfa 45%, #f3e8f7 100%) !important;
            background-attachment: fixed !important;
            font-family: 'Inter', sans-serif;
        }

        /* Soft floating color blobs for depth (purely decorative, behind content) */
        .stApp::before {
            content: "";
            position: fixed;
            top: -120px;
            left: -100px;
            width: 420px;
            height: 420px;
            background: radial-gradient(circle, rgba(126,207,190,0.45) 0%, rgba(126,207,190,0) 70%);
            z-index: 0;
            pointer-events: none;
        }
        .stApp::after {
            content: "";
            position: fixed;
            bottom: -140px;
            right: -120px;
            width: 480px;
            height: 480px;
            background: radial-gradient(circle, rgba(160,150,235,0.35) 0%, rgba(160,150,235,0) 70%);
            z-index: 0;
            pointer-events: none;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }
        [data-testid="stToolbar"], [data-testid="stDecoration"] {
            background: transparent !important;
        }

        /* ---- Main content shell: frosted glass card ---- */
        .block-container {
            max-width: 780px;
            margin-top: 1.5rem;
            padding: 2.2rem 2.4rem 2.6rem 2.4rem;
            background: rgba(255, 255, 255, 0.45) !important;
            backdrop-filter: blur(22px) saturate(160%);
            -webkit-backdrop-filter: blur(22px) saturate(160%);
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.6);
            box-shadow: 0 8px 32px rgba(69, 89, 120, 0.12);
            position: relative;
            z-index: 1;
        }

        /* ---- Title ---- */
        h1 {
            font-family: 'Poppins', sans-serif !important;
            color: #3a4a63 !important;
            font-weight: 600 !important;
            font-size: 2rem !important;
            letter-spacing: -0.02em;
            margin-bottom: 0.2rem !important;
        }
        [data-testid="stCaptionContainer"], .stCaption {
            color: #6b7a94 !important;
        }

        /* ---- Sidebar: glass panel ---- */
        section[data-testid="stSidebar"] {
            background: rgba(255, 255, 255, 0.35) !important;
            backdrop-filter: blur(20px) saturate(160%);
            -webkit-backdrop-filter: blur(20px) saturate(160%);
            border-right: 1px solid rgba(255, 255, 255, 0.5);
        }
        section[data-testid="stSidebar"] h2 {
            font-family: 'Poppins', sans-serif;
            color: #3a4a63;
            font-size: 1.1rem;
            font-weight: 600;
        }
        section[data-testid="stSidebar"] p {
            color: #5c6b85;
            font-size: 0.9rem;
        }

        /* Sidebar upload widget — glass card */
        section[data-testid="stSidebar"] .stFileUploader {
            background: rgba(255, 255, 255, 0.5);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 0.6rem;
            border: 1px solid rgba(255, 255, 255, 0.6);
        }

        /* ---- Buttons: glassy gradient pill ---- */
        .stButton > button {
            background: linear-gradient(135deg, rgba(126,207,190,0.9), rgba(139,163,235,0.9));
            color: #ffffff;
            border: 1px solid rgba(255,255,255,0.5);
            border-radius: 14px;
            padding: 0.55rem 1.1rem;
            font-weight: 500;
            backdrop-filter: blur(6px);
            box-shadow: 0 4px 14px rgba(110, 140, 200, 0.25);
            transition: all 0.25s ease;
        }
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 18px rgba(110, 140, 200, 0.35);
            color: #ffffff;
        }

        /* ---- Chat message bubbles: frosted glass ---- */
        div[data-testid="stChatMessage"] {
            background: rgba(255, 255, 255, 0.55) !important;
            backdrop-filter: blur(14px) saturate(160%);
            -webkit-backdrop-filter: blur(14px) saturate(160%);
            border-radius: 18px;
            padding: 0.9rem 1.1rem;
            margin-bottom: 0.7rem;
            box-shadow: 0 4px 18px rgba(69, 89, 120, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.55);
        }

        /* ---- Chat input: glass bar ---- */
        .stChatInputContainer, div[data-testid="stChatInput"] {
            border-radius: 16px !important;
            background: rgba(255, 255, 255, 0.55) !important;
            backdrop-filter: blur(16px) saturate(160%);
            -webkit-backdrop-filter: blur(16px) saturate(160%);
            border: 1px solid rgba(255, 255, 255, 0.6) !important;
        }
        div[data-testid="stChatInput"] textarea {
            background: transparent !important;
            color: #3a4a63 !important;
        }
        [data-testid="stBottomBlockContainer"] {
            background: transparent !important;
        }

        [data-testid="collapsedControl"] {
            background: transparent !important;
        }

        /* ---- Alerts: soft glass tones ---- */
        div[data-testid="stAlertContentSuccess"] {
            background: rgba(210, 240, 227, 0.6) !important;
            backdrop-filter: blur(8px);
            border-radius: 12px;
            color: #2f5d4f;
        }
        div[data-testid="stAlertContentError"] {
            background: rgba(250, 220, 217, 0.6) !important;
            backdrop-filter: blur(8px);
            border-radius: 12px;
            color: #7a3b36;
        }
        div[data-testid="stAlertContentWarning"] {
            background: rgba(250, 235, 205, 0.6) !important;
            backdrop-filter: blur(8px);
            border-radius: 12px;
            color: #7a5a2b;
        }

        hr {
            border-top: 1px solid rgba(255,255,255,0.5);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# 1. GENERATE HIDDEN IDs IN THE BACKGROUND
# If this is the user's first time opening the page, we create silent IDs for them.
if "user_id" not in st.session_state:
    st.session_state.user_id = f"user_{uuid.uuid4().hex[:8]}"
if "session_id" not in st.session_state:
    st.session_state.session_id = f"session_{uuid.uuid4().hex[:8]}"
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Medical Q&A Assistant 💊")
st.caption("A calm, focused space to ask questions about your medical documents.")

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