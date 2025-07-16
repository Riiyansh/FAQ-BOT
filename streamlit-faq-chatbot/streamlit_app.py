"""
Streamlit FAQ Chatbot (streamlit_app.py)
Run with:
    streamlit run streamlit_app.py -- -csv faq.csv
"""

import io
import sys
import pandas as pd
import streamlit as st
from sentence_transformers import SentenceTransformer
from pathlib import Path

from app import clean_text, get_response, build_faiss_index

st.set_page_config(page_title="FAQ Chatbot", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
        .stChatMessage {border-radius: 12px; padding:0.6rem 0.9rem;}
        footer, header {visibility: hidden;}
        .block-container {padding-top: 2rem;}
    </style>
""", unsafe_allow_html=True)

st.title("🤖 FAQ Chatbot")
st.write("Upload a CSV file and ask any question from your knowledge base.")

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
model_name = st.sidebar.selectbox("Choose embedding model", ["all-mpnet-base-v2", "all-MiniLM-L6-v2"])
thr_exact = st.sidebar.slider("Exact match threshold", 0.0, 1.0, 0.60, 0.05)
thr_suggest = st.sidebar.slider("Suggestion threshold", 0.0, 1.0, 0.35, 0.05)

@st.cache_resource
def load_model(name):
    return SentenceTransformer(name)

@st.cache_resource
def prepare_index(csv_bytes, model_name):
    df = pd.read_csv(io.BytesIO(csv_bytes)).dropna(subset=["question", "answer"])
    cleaned = [clean_text(q) for q in df["question"]]
    model = load_model(model_name)
    vectors = model.encode(cleaned, convert_to_numpy=True, normalize_embeddings=True)
    index = build_faiss_index(vectors)
    return df, vectors, index

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if uploaded_file:
    file_bytes = uploaded_file.getvalue()
    df, vectors, index = prepare_index(file_bytes, model_name)
    st.sidebar.success(f"Loaded {len(df)} FAQs ✓")

    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    query = st.chat_input("Ask your question…")
    if query:
        st.session_state.chat_history.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        model = load_model(model_name)
        answer, score = get_response(query, model=model, index=index, df=df, vectors=vectors,
                                     thr_exact=thr_exact, thr_suggest=thr_suggest)

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.chat_history.append({"role": "assistant", "content": answer})
else:
    st.info("Upload a valid FAQ CSV file with 'question' and 'answer' columns.")
