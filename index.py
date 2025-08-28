import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import tkinter as tk
from tkinter import ttk, messagebox
import time
from threading import Thread


data = pd.read_csv("Crop_recommendation.csv")
X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = data['label']
model = RandomForestClassifier()
model.fit(X, y)

# lang 
languages = {
    "en": {
        "title": "🌿 Crop Recommendation System",
        "predict": "🌱 Predict",
        "reset": "🔄 Reset",
        "language": "🌐 Language: English",
        "placeholders": {
            "Nitrogen (N)": "e.g. 90",
            "Phosphorus (P)": "e.g. 42",
            "Potassium (K)": "e.g. 43",
            "Temperature (°C)": "e.g. 20.5",
            "Humidity (%)": "e.g. 80",
            "pH": "e.g. 6.5",
            "Rainfall (mm)": "e.g. 200"
        },
        "error": "Please enter valid numeric values.",
        "result": "✅ Recommended crop: {}"
    },
    "ru": {
        "title": "🌿 Система Рекомендации Урожая",
        "predict": "🌱 Предсказать",
        "reset": "🔄 Сброс",
        "language": "🌐 Язык: Русский",
        "placeholders": {
            "Азот (N)": "напр. 90",
            "Фосфор (P)": "напр. 42",
            "Калий (K)": "напр. 43",
            "Температура (°C)": "напр. 20.5",
            "Влажность (%)": "напр. 80",
            "pH": "напр. 6.5",
            "Осадки (мм)": "напр. 200"
        },
        "error": "Пожалуйста, введите числовые значения.",
        "result": "✅ Рекомендуемая культура: {}"
    }
}

current_lang = "en"
fields = {}
entries = {}

# GUI
root = tk.Tk()
root.title("🌾 Crop App")
root.geometry("460x640")
root.resizable(False, False)
root.configure(bg="white")

style = ttk.Style(root)
style.theme_use("clam")

def clear_placeholder(event, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, tk.END)
        entry.config(foreground="black")
        result_label.config(text="")

def restore_placeholder(event, entry, placeholder):
    if entry.get().strip() == "":
        entry.insert(0, placeholder)
        entry.config(foreground="gray")

def update_language():
    global current_lang, fields, entries
    lang = languages[current_lang]

    title_label.config(text=lang["title"])
    predict_button.config(text=lang["predict"])
    lang_button.config(text=lang["language"])
    reset_button.config(text=lang["reset"])

    for child in input_frame.winfo_children():
        child.destroy()
    entries.clear()

    fields = lang["placeholders"]
    for label_text, placeholder in fields.items():
        ttk.Label(input_frame, text=label_text, background="white").pack(anchor="w", pady=(6, 0))
        entry = ttk.Entry(input_frame, width=30, foreground="gray")
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda e, entry=entry, p=placeholder: clear_placeholder(e, entry, p))
        entry.bind("<FocusOut>", lambda e, entry=entry, p=placeholder: restore_placeholder(e, entry, p))
        entry.pack()
        entries[label_text] = entry

def toggle_language():
    global current_lang
    current_lang = "ru" if current_lang == "en" else "en"
    update_language()

def show_input_table(values):
    # clean table
    for widget in table_frame.winfo_children():
        widget.destroy()

    columns = ["N", "P", "K", "Temp", "Humidity", "pH", "Rain"]

    table = ttk.Treeview(table_frame, columns=columns, show="headings", height=1)
    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=60, anchor="center")

    table.insert("", "end", values=values)
    table.pack()

def predict_action():
    lang = languages[current_lang]
    placeholders = lang["placeholders"]
    progress_bar.start()
    time.sleep(2)
    try:
        user_input = []
        for field, entry in entries.items():
            value = entry.get()
            if value == placeholders[field] or value.strip() == "":
                raise ValueError()
            user_input.append(float(value))
        prediction = model.predict([user_input])[0]
        result_label.config(text=lang["result"].format(prediction), foreground="green")
        show_input_table(user_input)
    except:
        messagebox.showerror("Error", lang["error"])
    finally:
        progress_bar.stop()

def predict():
    Thread(target=predict_action).start()

def reset_fields():
    lang = languages[current_lang]
    placeholders = lang["placeholders"]
    result_label.config(text="")
    for label, entry in entries.items():
        entry.delete(0, tk.END)
        entry.insert(0, placeholders[label])
        entry.config(foreground="gray")
    for widget in table_frame.winfo_children():
        widget.destroy()

# UI
title_label = ttk.Label(root, text="", font=("Arial", 16, "bold"), background="white", foreground="#111827")
title_label.pack(pady=(20, 10))

input_frame = tk.Frame(root, bg="white")
input_frame.pack()

progress_bar = ttk.Progressbar(root, mode="indeterminate", length=220)
progress_bar.pack(pady=10)

result_label = ttk.Label(root, text="", font=("Arial", 13), background="white", foreground="#10B981")
result_label.pack(pady=5)

# meaning of table
table_frame = tk.Frame(root, bg="white")
table_frame.pack(pady=(5, 10))

# buttons
button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=(5, 10))

predict_button = ttk.Button(button_frame, text="", command=predict)
predict_button.grid(row=0, column=0, padx=5)

reset_button = ttk.Button(button_frame, text="", command=reset_fields)
reset_button.grid(row=0, column=1, padx=5)

lang_button = ttk.Button(button_frame, text="", command=toggle_language)
lang_button.grid(row=0, column=2, padx=5)

update_language()
root.mainloop()
