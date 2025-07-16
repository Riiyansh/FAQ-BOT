# FAQ-BOT
<img width="1512" height="900" alt="Screenshot 2025-07-16 at 6 56 03 AM" src="https://github.com/user-attachments/assets/8fe2c082-d69e-4595-a1c2-f58e97725577" />




# 🤖 FAQ-BOT – AI-Powered FAQ Chatbot

A smart, lightweight, and embeddable FAQ chatbot built using **Streamlit**, **Sentence Transformers**, and **FAISS**. Upload your own CSV with questions and answers, and this bot will semantically match and respond to user queries.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://riiyansh-faq-bot.streamlit.app)

---

## 📌 Features

- 🧠 Semantic search using [SentenceTransformers](https://www.sbert.net/)
- ⚡ Fast vector search using [FAISS](https://github.com/facebookresearch/faiss)
- 💬 Simple Streamlit-based UI
- 📄 CSV-based knowledge base (just upload `question`, `answer`)
- 🔁 CLI and web interface available
- 🌐 Embeddable in any website via iframe or floating button

---

## 🚀 Live Demo

🔗 [https://riiyansh-faq-bot.streamlit.app](faq-bot-dgfavkzva8skbkfrcyfirq.streamlit.app/)  
Try the chatbot online. Upload your own `faq.csv` or use the included sample.

---

## 📁 Project Structure

```

📦 FAQ-BOT/
├── streamlit\_app.py       # Streamlit web interface
├── app.py                 # CLI-based interface + backend logic
├── requirements.txt       # Required packages
├── faq.csv                # Sample FAQ file (CSV format)
└── README.md              # This file

````

---

## ⚙️ Setup Instructions

### ▶️ Run Locally

1. Clone the repository:
```bash
git clone https://github.com/Riiyansh/FAQ-BOT.git
cd FAQ-BOT
````

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the chatbot (CLI mode):

```bash
python app.py --csv faq.csv
```

5. Or run the Streamlit UI:

```bash
streamlit run streamlit_app.py -- -csv faq.csv
```

---

## 📄 FAQ File Format

The bot reads a CSV file with these two columns:

| question                    | answer                                                        |
| --------------------------- | ------------------------------------------------------------- |
| What is your return policy? | We accept returns within 30 days.                             |
| How can I contact support?  | Email us at [support@example.com](mailto:support@example.com) |

---

## 🌐 Embed Chatbot on Your Website

### 💬 Add a Floating Chat Button with Popup

Paste this snippet anywhere in your site’s HTML:

```html
<!-- 💬 Floating Chat Button -->
<div id="chatBtn" style="position:fixed;bottom:20px;right:20px;z-index:1000;">
  <button onclick="openChat()"
    style="padding:12px 18px;border:none;border-radius:50px;background:#4CAF50;color:white;font-size:16px;">
    💬 Chat
  </button>
</div>

<!-- 🧠 Chatbot Modal -->
<div id="chatModal" style="display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);z-index:9999;">
  <div style="position:relative;margin:5% auto;width:90%;max-width:600px;height:80%;background:white;border-radius:12px;overflow:hidden;">
    <span onclick="closeChat()" style="position:absolute;top:10px;right:20px;font-size:28px;cursor:pointer;">&times;</span>
    <iframe src="https://riiyansh-faq-bot.streamlit.app/" width="100%" height="100%" style="border:none;"></iframe>
  </div>
</div>

<script>
  function openChat() { document.getElementById('chatModal').style.display = 'block'; }
  function closeChat() { document.getElementById('chatModal').style.display = 'none'; }
</script>
```

✅ This will show a floating 💬 button that opens your chatbot in a pop-up modal.

---

## 🛠 Tech Stack

* **Python 3.10+**
* [Streamlit](https://streamlit.io/)
* [Sentence Transformers](https://www.sbert.net/)
* [FAISS (Facebook AI)](https://github.com/facebookresearch/faiss)
* Pandas, NLTK, RapidFuzz, Contractions

---

## 👨‍💻 Author

Made with ❤️ by [**Riyansh Chouhan**](https://github.com/Riiyansh)
Connect with me on [LinkedIn](https://www.linkedin.com/in/riyansh-chouhan/)

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## ⭐️ Like This Project?

Give it a ⭐ on GitHub to show support!


