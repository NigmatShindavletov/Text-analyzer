import os
import re
import customtkinter as ctk
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Анализатор текста")
app.geometry("1000x600")
app.resizable(False, False)

def count_sentences(text):
    text = re.sub(r"\.{3}", "...", text)
    endings = re.findall(r"\.{3}(?=\s+[А-ЯЁA-Z])|[.!?]+(?=\s+[А-ЯЁA-Z]|\s*$)", text)
    return len(endings)

def analyze_text(text):
    global report_saved
    report_saved = False

    if not text.strip():
        return
    sentence_count = count_sentences(text)
    word_count = len(text.split())
    char_count = len(text)
    line_count = text.count("\n") + 1
    report_text.delete("1.0", "end")
    report_text.insert("1.0", f"Отчет анализа текста\nКоличество строк: {line_count}\nКоличество слов: {word_count}\nКоличество символов: {char_count}\nКоличество предложений: {sentence_count}")

title = ctk.CTkLabel(app, text="Анализатор текста", font=("Arial", 30, "bold"))
title.pack(pady=20)

input_text = ctk.CTkTextbox(app)
input_text.pack(pady=10, padx=20, fill="both", expand=True)
input_text.insert("1.0", "Вставьте сюда текст...")
def clear_placeholder(event):
    if input_text.get("1.0", "end-1c") == "Вставьте сюда текст...":
        input_text.delete("1.0", "end")

input_text.bind("<FocusIn>", clear_placeholder)

button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10, padx=20, fill="x")

analys_button = ctk.CTkButton(button_frame, text="Анализировать", command=lambda: analyze_text(input_text.get("1.0", "end-1c")), height=80, width=300, font=("Arial", 20, "bold"))
analys_button.grid(row=0, column=0, padx=10, sticky="ew")

report_frame = ctk.CTkFrame(app)
report_frame.pack(pady=15, padx=20, fill="both", expand=True)

report_text = ctk.CTkTextbox(report_frame)
report_text.pack(fill="both", expand=True)

def save_report():
    global report_saved

    if report_saved:
        return

    report_content = report_text.get("1.0", "end-1c")

    if not report_content.strip():
        return

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"report_{timestamp}.txt"
    filepath = os.path.join(os.getcwd(), filename)

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(report_content)

    report_text.delete("1.0", "end")
    report_text.insert("1.0", f"Отчет сохранен:\n{filepath}")

    report_saved = True

save_report_button = ctk.CTkButton(button_frame, text="Сохранить отчет", command=save_report, height=80, width=300, font=("Arial", 20, "bold"))
save_report_button.grid(row=0, column=1, padx=10, sticky="ew")

exit_button = ctk.CTkButton(button_frame, text="Выход", command=app.destroy, height=80, width=300, font=("Arial", 20, "bold"))
exit_button.grid(row=0, column=2, padx=10, sticky="ew")

app.mainloop()