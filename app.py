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

if "data_applied" not in st.session_state:
    st.session_state.data_applied = False

if "website_link" not in st.session_state:
    st.session_state.website_link = ""

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

if "text_data" not in st.session_state:
    st.session_state.text_data = ""


st.sidebar.title("Controls")

st.session_state.source_type = st.sidebar.radio(
    "Select Data Source",
    ["Website", "PDF", "Text"]
)


with st.sidebar.form("data_form"):
    if st.session_state.source_type == "Website":
        link = st.text_input(
            "Website URL",
            placeholder="https://www.example.com"
        )

    elif st.session_state.source_type == "PDF":
        uploaded_pdf = st.file_uploader(
            "Upload PDF",
            type=["pdf"]
        )

    elif st.session_state.source_type == "Text":
        text_input = st.text_area(
            "Enter Text",
            height=200
        )

    apply_clicked = st.form_submit_button("Apply")


if apply_clicked:
    try:
        if st.session_state.source_type == "Website":
            if not link.strip():
                st.sidebar.error("Please enter a website URL")
            else:
                st.session_state.website_link = link
                st.session_state.data_applied = True
                st.sidebar.success("Website applied successfully")

        elif st.session_state.source_type == "PDF":
            if uploaded_pdf is None:
                st.sidebar.error("Please upload a PDF")
            else:
                reader = PdfReader(BytesIO(uploaded_pdf.read()))
                pdf_text = ""
                for page in reader.pages:
                    t = page.extract_text()
                    if t:
                        pdf_text += t + "\n"

                st.session_state.pdf_text = pdf_text
                st.session_state.data_applied = True
                st.sidebar.success("PDF applied successfully")

        elif st.session_state.source_type == "Text":
            if not text_input.strip():
                st.sidebar.error("Please enter some text")
            else:
                st.session_state.text_data = text_input
                st.session_state.data_applied = True
                st.sidebar.success("Text applied successfully")

    except Exception as e:
        st.sidebar.error(f"Apply failed: {e}")


if st.sidebar.button("New Chat"):
    st.session_state.messages = []
    st.session_state.data_applied = False
    st.session_state.website_link = ""
    st.session_state.pdf_text = ""
    st.session_state.text_data = ""
    obj.reset_fuction()
    st.rerun()


st.title("RAG Chatbot")
st.caption("Website / PDF / Text → Embeddings → Answer")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


prompt = st.chat_input(
    "Ask your question...",
    disabled=not st.session_state.data_applied
)

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                if st.session_state.source_type == "Website":
                    response = obj.main_for_web(
                        link=st.session_state.website_link,
                        question=prompt
                    )

                elif st.session_state.source_type == "PDF":
                    response = obj.mian_for_pdf(
                        text=st.session_state.pdf_text,
                        question=prompt
                    )

                elif st.session_state.source_type == "Text":
                    response = obj.mian_for_text(
                        text_path=st.session_state.text_data,
                        question=prompt
                    )

                st.markdown(response)

            except Exception as e:
                response = f"Error: {e}"
                st.error(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
