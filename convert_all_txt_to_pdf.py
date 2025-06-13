import os
from fpdf import FPDF

# Define input and output folders
source_base = "data/cleaned_data"
target_base = "data/pdfs"

# Loop through all year folders in cleaned_data
for year in os.listdir(source_base):
    year_folder = os.path.join(source_base, year)
    if not os.path.isdir(year_folder):
        continue

    output_folder = os.path.join(target_base, year)
    os.makedirs(output_folder, exist_ok=True)

    for file_name in os.listdir(year_folder):
        if file_name.endswith(".txt"):
            txt_path = os.path.join(year_folder, file_name)
            pdf_path = os.path.join(output_folder, file_name.replace(".txt", ".pdf"))

            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            try:
                with open(txt_path, "r", encoding="utf-8") as file:
                    for line in file:
                        # Replace unsupported characters to avoid crash
                        safe_line = line.encode("latin-1", "replace").decode("latin-1")
                        pdf.multi_cell(0, 10, safe_line)

                pdf.output(pdf_path)
                print(f"✅ Converted: {txt_path} → {pdf_path}")

            except Exception as e:
                print(f"❌ Error converting {txt_path}: {e}")
