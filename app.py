import streamlit as st
from main import Main
from pypdf import PdfReader
from io import BytesIO


st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)


@st.cache_resource
def load_backend():
    return Main()

obj = load_backend()


if "messages" not in st.session_state:
    st.session_state.messages = []

if "source_type" not in st.session_state:
    st.session_state.source_type = "Website"

if "last_response" not in st.session_state:
    st.session_state.last_response = ""


st.sidebar.title(" Controls")

st.session_state.source_type = st.sidebar.radio(
    "Select Data Source",
    ["Website", "PDF", "Text"]
)

if st.session_state.source_type == "Website":
    link = st.sidebar.text_input("Website URL")

elif st.session_state.source_type == "PDF":
    uploaded_pdf = st.sidebar.file_uploader("Upload PDF", type=["pdf"])

elif st.session_state.source_type == "Text":
    text_input = st.sidebar.text_area("Enter Text", height=200)


if st.sidebar.button(" New Chat"):
    st.session_state.messages = []
    st.session_state.last_response = ""
    obj.reset_fuction()
    st.rerun()


st.title(" RAG Chatbot")
st.caption("Website / PDF / Text → Embeddings → Answer")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


prompt = st.chat_input("Ask your question...")

if prompt:
    # User message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                if st.session_state.source_type == "Website":
                    st.session_state.last_response = obj.main_for_web(
                        link=link,
                        question=prompt
                    )

                elif st.session_state.source_type == "PDF":
                    if uploaded_pdf is None:
                        st.session_state.last_response = "Please upload a PDF first."
                    else:
                        reader = PdfReader(BytesIO(uploaded_pdf.read()))
                        pdf_text = ""

                        for page in reader.pages:
                            t = page.extract_text()
                            if t:
                                pdf_text += t + "\n"

                        st.session_state.last_response = obj.mian_for_pdf(
                            text=pdf_text,
                            question=prompt
                        )

                elif st.session_state.source_type == "Text":
                    st.session_state.last_response = obj.mian_for_text(
                        text_path=text_input,
                        question=prompt
                    )

                st.markdown(st.session_state.last_response)

            except Exception as e:
                st.session_state.last_response = f"❌ Error: {e}"
                st.error(st.session_state.last_response)


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": st.session_state.last_response
        }
    )
