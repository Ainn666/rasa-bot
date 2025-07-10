# 📰 Sarawak Gazette Chatbot

A RASA-based chatbot that enables users to interact with digitized content from the historical **Sarawak Gazette** archive. This project uses **Natural Language Understanding (NLU)** and **custom actions** to retrieve relevant articles by year, topic, editor, or author — with integration to the **Google Gemini API** for topic summarization and summary PDF generation.

---

## 📌 Features

- 🔍 Search Gazette content by **year**, **topic**, **editor**, or **author**
- 📂 Reads pre-cleaned `.txt` files from the Gazette archive
- 🤖 Integrates **Gemini API** to summarize articles related to a given topic
- 📄 Automatically generates and links summary PDFs
- 💬 Localhost-based chatbot interface using `index.html` (XAMPP-compatible)

---

## ⚙️ Tech Stack

- **RASA** 3.6
- **Python** 3.10+
- **Google Gemini API** (Generative summarization)
- **FPDF** (PDF summary generation)
- **XAMPP** (Local web server to serve `index.html`)

---

## 🖥️ Localhost Setup Guide

### 1. Train the Chatbot

Before running the chatbot, make sure your model is trained:

```bash
rasa train

2. Run the Chatbot Locally (Three-Terminal Setup)
Terminal 1 – Run Action Server

rasa run actions

Terminal 2 – Run RASA Backend

rasa run --enable-api --cors "*"

Terminal 3 – Serve Frontend via XAMPP

    Move index.html, data/, and related folders to:

C:\xampp\htdocs\chatbot\

    Start Apache in XAMPP Control Panel

    Open chatbot in browser:

http://localhost/chatbot/index.html

    💡 If any URLs inside actions.py use http://localhost:8080/, change them to http://localhost/chatbot/ to match XAMPP structure.

📁 Project Structure

.
├── actions/                  # Custom action files (e.g. summarization, article search)
├── data/
│   ├── cleaned_data/         # Gazette .txt files grouped by year
│   ├── pdfs/                 # Corresponding PDF files
│   └── generated_summaries/  # Output from PDF generator
├── models/                   # Trained RASA models
├── index.html                # Chatbot frontend (JS-based)
├── domain.yml                # Domain config (intents, actions, responses)
├── config.yml                # Pipeline & policy config
├── endpoints.yml             # Action server connection
├── requirements.txt          # Python packages needed
└── README.md                 # This file

🧪 Sample Intents

    "Show me the Gazette from 1948" → ask_issue_by_year

    "What are the articles about agriculture?" → ask_topic

    "Who was the editor in 1937?" → ask_editor

    "Show me articles by John Smith" → ask_by_person

🔮 Future Work

    Add support for Bahasa Melayu queries

    Integrate OCR for scanned Gazette image files

    Add voice input/output via Web Speech API

    Enhance chatbot UI/UX for mobile devices

👩‍💻 Author

Ainul Maisarah Binti Mohd Aznil
Final Year Project – Faculty of Computer Science & IT
Universiti Malaysia Sarawak (UNIMAS)
📜 License

This project is for academic use.
Commercial redistribution or deployment is not permitted without prior written consent.