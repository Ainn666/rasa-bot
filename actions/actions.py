import os
import re
from fpdf import FPDF
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import google.generativeai as genai

# 🛡️ Configure Gemini
genai.configure(api_key="AIzaSyDCwNZjhMJgOOKmzIcSmY8C1lwvDQEN7To")

class ActionSearchGazette(Action):
    def name(self):
        return "action_search_gazette"

    def run(self, dispatcher, tracker, domain):
        year = tracker.get_slot("year")
        date = tracker.get_slot("date")

        if not year:
            dispatcher.utter_message(text="Please provide a year or date.")
            return []

        folder_path = os.path.join("data", "cleaned_data", year)
        pdf_folder = os.path.join("data", "pdfs", year)

        if not os.path.exists(folder_path):
            dispatcher.utter_message(text=f"No Gazette found for year {year}.")
            return []

        # 🗓️ If user asked for a specific date (e.g., 01-02-1939)
        if date:
            pdf_filename = f"{date}.pdf"
            pdf_path = os.path.join(pdf_folder, pdf_filename)
            message = ""

            if os.path.exists(pdf_path):
                pdf_url = f"http://localhost:8080/data/pdfs/{year}/{pdf_filename}"
                message = f"📄 Gazette from {date} is available.\n🔗 View PDF: {pdf_url}"

                txt_file_path = os.path.join(folder_path, f"{date}.txt")
                if os.path.exists(txt_file_path):
                    with open(txt_file_path, 'r', encoding='utf-8') as f:
                        lines = [line.strip() for line in f if line.strip()]
                        if lines:
                            preview = lines[0][:200] + ("..." if len(lines[0]) > 200 else "")
                            message += f"\n📝 Preview: {preview}"
            else:
                message = f"Sorry, the Gazette issue from {date} is not available as a PDF."

            dispatcher.utter_message(text=message)
            return []

        # 📂 If user asked for all issues from a year
        response = f"📅 Gazette issues from {year}:\n\n"
        if os.path.exists(pdf_folder):
            pdfs = sorted([f for f in os.listdir(pdf_folder) if f.endswith(".pdf")])[:5]

            if not pdfs:
                response += "No Gazette PDFs found for this year."
            else:
                for file_name in pdfs:
                    label = file_name.replace(".pdf", "")
                    file_url = f"http://localhost:8080/data/pdfs/{year}/{file_name}"
                    response += f"📎 {label} – View PDF: {file_url}\n"
        else:
            response += "No PDF folder found for this year."

        dispatcher.utter_message(text=response.strip())
        return []

class ActionFindEditorByDate(Action):
    def name(self):
        return "action_find_editor_by_date"

    def run(self, dispatcher, tracker, domain):
        date = tracker.get_slot("date") or tracker.get_slot("year")
        dispatcher.utter_message(text=f"The editor of the Gazette in {date} was Unknown.")
        return []

class ActionFindArticlesByPerson(Action):
    def name(self):
        return "action_find_articles_by_person"

    def run(self, dispatcher, tracker, domain):
        person = tracker.get_slot("person")
        year = tracker.get_slot("year")
        if not person:
            dispatcher.utter_message(text="Please provide a person's name to search for.")
            return []

        base_path = "data/cleaned_data"
        folder_path = os.path.join(base_path, year) if year else base_path
        found = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".txt"):
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        if person.lower() in f.read().lower():
                            found.append(file)
        if found:
            dispatcher.utter_message(text=f"📄 Articles mentioning '{person}':\n- " + "\n- ".join(found[:5]))
        else:
            dispatcher.utter_message(text=f"Sorry, no articles found that mention '{person}'.")
        return []

class ActionSummarizeTopic(Action):
    def name(self):
        return "action_summarize_topic"

    def run(self, dispatcher, tracker, domain):
        topic = tracker.get_slot("topic")
        if not topic:
            dispatcher.utter_message(text="Please specify a topic to summarize.")
            return []

        base_path = "data/cleaned_data"
        matched = []

        for year_folder in sorted(os.listdir(base_path)):
            year_path = os.path.join(base_path, year_folder)
            if not os.path.isdir(year_path):
                continue

            for file in sorted(os.listdir(year_path)):
                if file.endswith(".txt"):
                    file_path = os.path.join(year_path, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    paragraphs = re.split(r"\n\s*\n", content)
                    topic_paragraphs = [p.strip() for p in paragraphs if topic.lower() in p.lower()]

                    if topic_paragraphs:
                        matched.append({
                            "file": file,
                            "year": year_folder,
                            "paragraphs": topic_paragraphs[:2]
                        })

                if len(matched) >= 5:
                    break
            if len(matched) >= 5:
                break

        if not matched:
            dispatcher.utter_message(text=f"Sorry, I couldn’t find any articles about '{topic}'.")
            return []

        message = f"📚 **Articles related to '{topic}':**\n\n"
        model = genai.GenerativeModel("gemini-1.5-pro-latest")

        for match in matched:
            label = match["file"].replace(".txt", "")
            pdf_url = f"http://localhost:8080/data/pdfs/{match['year']}/{label}.pdf"
            prompt = f"Summarize the following Gazette content about '{topic}' in 2–3 bullet points:\n\n" + "\n\n".join(match["paragraphs"])

            try:
                chat = model.start_chat()
                response = chat.send_message(prompt)
                summary = response.text.strip()
            except Exception as e:
                summary = f"⚠️ Gemini error: {str(e)}"

            message += f"📎 **{label}** ({match['year']})\n{summary}\n🔗 View PDF: {pdf_url}\n\n"

        dispatcher.utter_message(text=message.strip())
        return []

class ActionAskIssueByDate(Action):
    def name(self):
        return "action_ask_issue_by_date"

    def run(self, dispatcher, tracker, domain):
        date = tracker.get_slot("date")
        if date:
            dispatcher.utter_message(text=f"Let me see if I can find the edition published on {date}.")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find the publication date.")
        return []

class ActionAskTopic(Action):
    def name(self):
        return "action_ask_topic"

    def run(self, dispatcher, tracker, domain):
        topic = tracker.get_slot("topic")
        dispatcher.utter_message(text=f"Here is some information about {topic} from the Gazette.")
        return []

class ActionAskEditor(Action):
    def name(self):
        return "action_ask_editor"

    def run(self, dispatcher, tracker, domain):
        date = tracker.get_slot("date")
        dispatcher.utter_message(text=f"Here is the information about the editor for the Gazette on {date}.")
        return []

class ActionAskByPerson(Action):
    def name(self):
        return "action_ask_by_person"

    def run(self, dispatcher, tracker, domain):
        person = tracker.get_slot("person")
        dispatcher.utter_message(text=f"Here is some information about articles written by {person}.")
        return []

class ActionDescribePerson(Action):
    def name(self):
        return "action_describe_person"

    def run(self, dispatcher, tracker, domain):
        person = tracker.get_slot("person")
        if not person:
            dispatcher.utter_message(text="Please tell me the name you'd like to know more about.")
            return []

        job_keywords = ["officer", "secretary", "editor", "clerk", "minister", "manager", "superintendent", "assistant", "director", "surveyor"]
        base_path = "data/cleaned_data"
        description = None

        for root, _, files in os.walk(base_path):
            for file in files:
                if file.endswith(".txt"):
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        content = f.read()
                        matches = re.findall(rf"([^.]*\b{re.escape(person)}\b[^.]*\.)", content, re.IGNORECASE)
                        for match in matches:
                            if any(word in match.lower() for word in job_keywords):
                                description = match.strip()
                                break
                        if not description and matches:
                            description = " ".join(matches[:2]).strip()
                if description:
                    break
            if description:
                break

        if description:
            dispatcher.utter_message(text=f"🧾 Based on the Gazette: {description}")
        else:
            dispatcher.utter_message(text=f"Sorry, I couldn't find any information about {person} in the Gazette.")
        return []

class ActionGenerateSummaryPDF(Action):
    def name(self):
        return "action_generate_summary_pdf"

    def run(self, dispatcher, tracker, domain):
        topic = tracker.get_slot("topic")
        if not topic:
            dispatcher.utter_message(text="I need a topic to generate the PDF summary.")
            return []

        output_dir = "data/generated_summaries"
        os.makedirs(output_dir, exist_ok=True)
        pdf_filename = f"summary_{topic.replace(' ', '_')}.pdf"
        pdf_path = os.path.join(output_dir, pdf_filename)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        text = f"Summary of Gazette Articles on Topic: {topic.title()}\n\n(This is a placeholder summary. Replace with model output if desired.)"
        for line in text.split("\n"):
            pdf.multi_cell(0, 10, line)

        pdf.output(pdf_path)
        pdf_url = f"http://localhost:8080/data/generated_summaries/{pdf_filename}"
        dispatcher.utter_message(text=f"✅ Summary PDF generated!\n🔗 [Download PDF here]({pdf_url})")
        return []
