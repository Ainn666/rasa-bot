# 📰 Sarawak Gazette Chatbot

A RASA-based chatbot that enables users to interact with digitized content from the historical **Sarawak Gazette** archive. This project uses **Natural Language Understanding (NLU)** and **custom actions** to retrieve relevant articles by year, topic, editor, or author — with integration to **Google Gemini API** for topic summarization.

---

## 📌 Features

- 🔍 Search Gazette content by **year**, **topic**, **editor**, or **author**
- 📂 Reads pre-cleaned `.txt` files from Gazette archive
- 🤖 Integrates **Gemini API** for summarizing related articles
- 📄 Generates summaries and PDF download links
- 🌐 Web-based chatbot interface using `index.html`

---

## ⚙️ Tech Stack

- **RASA** 3.6 (Open-source conversational AI)
- **Python** 3.10+
- **Google Gemini API** (Text summarization)
- **FPDF** (PDF generation)
- **Render.com** (Deployment)

---

## 🚀 Deployment Guide (Render.com)

### 1. Clone this Repository

```bash
git clone https://github.com/YOUR_USERNAME/sarawak-gazette-chatbot.git
cd sarawak-gazette-chatbot


2. Project Structure

.
├── actions/                  # Custom action files (e.g., action_summarize_topic.py)
├── data/                     # NLU, rules, stories
├── models/                   # Trained RASA model (optional)
├── index.html                # Chatbot frontend
├── domain.yml                # Domain configuration
├── config.yml                # Pipeline and policies
├── endpoints.yml             # Custom action server config
├── requirements.txt          # Python dependencies
├── Dockerfile                # Render deployment container config
└── README.md                 # This file

3. Render.com Setup

    Create a new Web Service on https://render.com

    Connect to your GitHub repo

    Select Docker as Runtime

    Set port to 5005

    Deploy and wait for build

📄 Sample Intents

    ask_issue_by_year: "Show me the Gazette from 1948"

    ask_topic: "What are the articles about agriculture?"

    ask_editor: "Who was the editor in 1937?"

    ask_by_person: "Show me articles by John Smith"

🧠 Future Work

    Add support for Malay queries

    Include OCR for scanned Gazette images

    Add voice input/output

    Improve UI/UX and mobile responsiveness

🧑‍🎓 Author

Ainul Maisarah Binti Mohd Aznil
Final Year Project – Faculty of Computer Science & IT
Universiti Malaysia Sarawak (UNIMAS)
📜 License

This project is for academic use. Commercial use or redistribution is not permitted without permission.