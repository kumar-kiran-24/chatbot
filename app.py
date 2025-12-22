import streamlit as st
from main import Main

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------------------------
# Load backend ONCE
# --------------------------------------------------
@st.cache_resource
def load_backend():
    return Main()

obj = load_backend()

# --------------------------------------------------
# Initialize Streamlit session state
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "source_type" not in st.session_state:
    st.session_state.source_type = "Website"

# --------------------------------------------------
# Sidebar UI
# --------------------------------------------------
st.sidebar.title("⚙️ Controls")

st.session_state.source_type = st.sidebar.radio(
    "Select Data Source",
    ["Website", "PDF", "Text"]
)

# Inputs based on source
if st.session_state.source_type == "Website":
    link = st.sidebar.text_input(
        "Website URL",
        placeholder="https://example.com"
    )

elif st.session_state.source_type == "PDF":
    uploaded_pdf = st.sidebar.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

elif st.session_state.source_type == "Text":
    text_input = st.sidebar.text_area(
        "Enter Text",
        height=200
    )

# --------------------------------------------------
# NEW CHAT BUTTON (IMPORTANT)
# --------------------------------------------------
if st.sidebar.button("➕ New Chat"):
    # Clear UI history
    st.session_state.messages = []

    # Reset backend memory (new session_id)
    obj.reset_fuction()

    # Rerun app
    st.rerun()

# --------------------------------------------------
# Main UI
# --------------------------------------------------
st.title("🤖 RAG Chatbot")
st.caption("Context-aware conversational RAG with memory")

# --------------------------------------------------
# Display chat history
# --------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --------------------------------------------------
# Chat input
# --------------------------------------------------
prompt = st.chat_input("Ask your question...")

if prompt:
    # Store and show user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                if st.session_state.source_type == "Website":
                    response = obj.main_for_web(
                        link=link,
                        question=prompt
                    )

                elif st.session_state.source_type == "PDF":
                    if uploaded_pdf is None:
                        st.error("Please upload a PDF.")
                        st.stop()

                    with open("temp.pdf", "wb") as f:
                        f.write(uploaded_pdf.read())

                    response = obj.mian_for_pdf(
                        pdf="temp.pdf",
                        question=prompt
                    )

                elif st.session_state.source_type == "Text":
                    response = obj.mian_for_text(
                        text_path=text_input,
                        question=prompt
                    )

                st.markdown(response)

            except Exception as e:
                response = f" Error: {e}"
                st.error(response)

    # Store assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
