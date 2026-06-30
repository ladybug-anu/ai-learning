import streamlit as st
import tempfile, os
from rag import load_pdf, chunk_text, build_index, answer, rewrite_query, summarise_history

st.set_page_config(page_title="Document Q&A", page_icon="📄")
st.title("📄 Ask Your Document")

uploaded = st.file_uploader("Upload a PDF", type="pdf")

if uploaded:
    if st.session_state.get("doc_name") != uploaded.name:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded.read())
            tmp_path = tmp.name

        with st.spinner("Indexing..."):
            text, pages = load_pdf(tmp_path)
            chunks, chunk_pages = chunk_text(text, pages)
            collection = build_index(chunks, chunk_pages)
            st.session_state.collection = collection
            st.session_state.doc_name = uploaded.name
            st.session_state.history = []
            st.session_state.chat = []

        os.unlink(tmp_path)
        st.success(f"Indexed {len(chunks)} chunks")

    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if q := st.chat_input("Ask a question..."):
        st.session_state.chat.append({"role": "user", "content": q})
        with st.chat_message("user"):
            st.write(q)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = answer(q, st.session_state.collection, st.session_state.history)
            st.write(reply)

        st.session_state.chat.append({"role": "assistant", "content": reply})
        st.session_state.history = summarise_history(st.session_state.history)
else:
    st.info("Upload a PDF to get started")