"""
Improved FAQ Chatbot (app.py)
=============================
A production-ready CLI chatbot using Sentence Transformers + FAISS.
"""

import argparse
import os
import pickle
import re
import sys

import pandas as pd
import numpy as np
import contractions
import nltk
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer
import faiss
from rapidfuzz import fuzz

# Download stopwords if needed
try:
    STOPWORDS = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords")
    STOPWORDS = set(stopwords.words("english"))

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = contractions.fix(text.lower())
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    tokens = [tok for tok in text.split() if tok not in STOPWORDS]
    return " ".join(tokens)

def build_or_load_embeddings(csv_path: str, model_name: str = "all-mpnet-base-v2"):
    cache_path = os.path.splitext(csv_path)[0] + "_embeddings.pkl"
    if os.path.exists(cache_path):
        with open(cache_path, "rb") as f:
            return pickle.load(f)

    df = pd.read_csv(csv_path).dropna(subset=["question", "answer"])
    cleaned_qs = [clean_text(q) for q in df["question"].tolist()]
    model = SentenceTransformer(model_name)
    vectors = model.encode(cleaned_qs, convert_to_numpy=True, normalize_embeddings=True)

    data = {"df": df, "vectors": vectors, "model_name": model_name}
    with open(cache_path, "wb") as f:
        pickle.dump(data, f)
    return data

def build_faiss_index(vectors: np.ndarray):
    dim = vectors.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(vectors)
    return index

def get_response(query: str, *, model, index, df, vectors, top_k=3, thr_exact=0.60, thr_suggest=0.35):
    cleaned = clean_text(query)
    q_vec = model.encode([cleaned], convert_to_numpy=True, normalize_embeddings=True)
    scores, ids = index.search(q_vec, top_k)
    scores, ids = scores[0], ids[0]
    best_id, best_score = int(ids[0]), float(scores[0])

    if best_score >= thr_exact:
        return df.loc[best_id, "answer"], best_score

    if best_score >= thr_suggest:
        suggestions = [
            f"- {df.loc[int(idx), 'question']}\n  Answer: {df.loc[int(idx), 'answer']}"
            for idx in ids
        ]
        return "I found related questions:\n\n" + "\n\n".join(suggestions), best_score

    fuzzy_scores = [fuzz.partial_ratio(cleaned, clean_text(q)) / 100 for q in df["question"]]
    fi = int(np.argmax(fuzzy_scores))
    if fuzzy_scores[fi] >= 0.4:
        return (f"Did you mean: {df.loc[fi, 'question']}?\n\nAnswer: {df.loc[fi, 'answer']}"), fuzzy_scores[fi]

    return "I'm not sure I understood. Could you please rephrase?", 0.0

def chat_loop(model, index, df, vectors):
    print("\nChatbot ready! Type 'exit' to quit.\n")
    session = []
    try:
        while True:
            user = input("You: ").strip()
            if user.lower() == "exit":
                break
            answer, score = get_response(user, model=model, index=index, df=df, vectors=vectors)
            print("Bot:", answer)
            session.append({"user": user, "bot": answer, "score": score})
            fb = input("Helpful? (yes/no): ").strip().lower()
            session[-1]["feedback"] = fb
    except (KeyboardInterrupt, EOFError):
        print("\nExiting…")
    finally:
        if session:
            pd.DataFrame(session).to_csv("chat_log.csv", index=False)
            print("Saved chat_log.csv")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="CSV file with 'question' and 'answer'")
    parser.add_argument("--model", default="all-mpnet-base-v2")
    args = parser.parse_args()

    data = build_or_load_embeddings(args.csv, args.model)
    df, vectors = data["df"], data["vectors"]
    model = SentenceTransformer(data["model_name"])
    index = build_faiss_index(vectors)

    chat_loop(model, index, df, vectors)

if __name__ == "__main__":
    main()
