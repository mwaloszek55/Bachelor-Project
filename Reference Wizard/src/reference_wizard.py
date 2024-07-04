import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from gpt4all import GPT4All
from threading import Thread
from tkinter import ttk, filedialog
from tkinter.scrolledtext import ScrolledText
import time
import re
from gpt4all import GPT4All

model = GPT4All("mistral-7b-openorca.gguf2.Q4_0.gguf")

system_template = """
Imagine you are a reference wizard, when a user presents you with a reference, your task is to reformat any given reference into its corresponding BibTeX.
Use the author's name and year to form cite keys. Your response should ONLY include the BiBTeX.
If the ISSN, DOI or any other fields are not explicitly provided in the reference, do not add them to the BiBTeX.
"""


prompt_template = 'USER: {0}\nASSISTANT: '



settings = {
    'temp': 0.1,
    'top_k': 40,
    'top_p': 0.4,
    'max_tokens': 512,
    'n_batch': 8
}


def preprocess_input(text):
    cleaned_text = re.sub(r'-\s*\n\s*|\-\s+', '', text)
    return cleaned_text


def segment_references(reference_text):
    return reference_text.split('\n\n')


def generate_bibtex_for_segment(segment):
    prompt = system_template + prompt_template.format(segment)
    response = model.generate(prompt, temp=0, top_k=settings['top_k'], top_p=settings['top_p'], max_tokens=settings["max_tokens"], n_batch=settings["n_batch"])
    return response

def generate_bibtex_threaded():
    generate_button.config(state=tk.DISABLED)
    global start_time
    start_time = time.time()
    thread = Thread(target=generate_bibtex)
    thread.daemon = True #to terminate when program terminates
    thread.start()

def update_output(response, elapsed_time):
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, response)
    elapsed_time_label.config(text=f"Elapsed time: {elapsed_time:.2f} seconds")
    generate_button.config(state=tk.NORMAL)

def generate_bibtex():
    reference_raw = input_text.get("1.0", tk.END).strip()
    #print(reference_raw)
    reference = preprocess_input(reference_raw)
    #print(reference)

    global settings
    segments = segment_references(reference)

    aggregated_responses = []
    for segment in segments:
        response = generate_bibtex_for_segment(segment)
        aggregated_responses.append(response)

    final_response = "\n".join(aggregated_responses)
    elapsed_time = time.time() - start_time
    root.after(0, update_output(final_response, elapsed_time))
    root.after(0, lambda: generate_button.config(state=tk.NORMAL))


def import_references():
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not filepath:
        return
    with open(filepath, 'r', encoding='utf-8') as file:
        references = file.read()
    input_text.delete('1.0', tk.END)  # clear
    input_text.insert('1.0', references) 

def export_bibtex():
    filepath = filedialog.asksaveasfilename(defaultextension=".bib", filetypes=[("BibTeX files", "*.bib")])
    if not filepath:
        return
    bibtex_entries = output_text.get('1.0', tk.END)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(bibtex_entries)

def copy_to_clipboard():
    root.clipboard_clear()
    text = output_text.get("1.0", tk.END)
    root.clipboard_append(text)
    root.update()


def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")

    tk.Label(settings_window, text="Temperature:").grid(row=0, column=0)
    temp_entry = tk.Entry(settings_window)
    temp_entry.insert(0, str(settings['temp']))
    temp_entry.grid(row=0, column=1)

    #topk
    tk.Label(settings_window, text="Top K:").grid(row=1, column=0)
    top_k_entry = tk.Entry(settings_window)
    top_k_entry.insert(0, str(settings['top_k']))  # default
    top_k_entry.grid(row=1, column=1)

    #topp
    tk.Label(settings_window, text="Top P:").grid(row=2, column=0)
    top_p_entry = tk.Entry(settings_window)
    top_p_entry.insert(0, str(settings['top_p']))  # default
    top_p_entry.grid(row=2, column=1)

     #maxtokens
    tk.Label(settings_window, text="Max tokens:").grid(row=3, column=0)
    token_entry = tk.Entry(settings_window)
    token_entry.insert(0, str(settings['max_tokens']))  # default
    token_entry.grid(row=3, column=1)

    #n_batch
    tk.Label(settings_window, text="n_batch:").grid(row=4, column=0)
    n_batch_entry = tk.Entry(settings_window)
    n_batch_entry.insert(0, str(settings['n_batch']))  # default
    n_batch_entry.grid(row=4, column=1)

    #save
    save_button = ttk.Button(settings_window, text="Save Settings", command=lambda: save_settings(temp_entry.get(), top_k_entry.get(), top_p_entry.get(), n_batch_entry.get(), token_entry.get()))
    save_button.grid(row=5, column=0, columnspan=2)

def save_settings(temp, top_k, top_p, n_batch, max_tokens):
    try:
        settings['temp'] = float(temp)
        settings['top_k'] = int(top_k)
        settings['top_p'] = float(top_p)
        settings['max_tokens'] = int(max_tokens)
        settings['n_batch'] = int(n_batch)

        print("Settings saved:", settings)
    except ValueError as e:
        print("Error saving settings:", e)

def show_help():
    help_intro = "This help guide provides an overview of the adjustable parameters and their impact on the model's output."
    help_text = """
Temperature (temp):
Controls the randomness of the output. Lower values make the output more deterministic.

Top K (top_k):
Limits the number of top probabilities considered in each step, reducing randomness.

Top P (top_p):
Uses only the top probabilities that add up to this value for sampling, controlling diversity.

Max Tokens (max_tokens):
The maximum number of tokens generated in one call. Higher values allow for longer outputs.

n_batch:
Number of prompt tokens processed in parallel. Higher values can decrease latency but might use more computational resources.
    """
    help_window = tk.Toplevel(root)
    help_window.title("Help")

    intro_label = tk.Label(help_window, text=help_intro, justify=tk.LEFT, font='Helvetica', wraplength=400)
    intro_label.pack(padx=10, pady=(10, 0))
    
    help_label = tk.Label(help_window, text=help_text, justify=tk.LEFT, font='Helvetica', wraplength=400)
    help_label.pack(padx=10, pady=(10, 0))


#tkinter ui
root = tk.Tk()
root.title("Reference Wizard")


top_frame = ttk.Frame(root)
top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)


import_button = ttk.Button(top_frame, text="Import", command=import_references, width=10)
import_button.grid(row=0, column=0, padx=5, pady=2)

export_button = ttk.Button(top_frame, text="Export", command=export_bibtex, width=10)
export_button.grid(row=0, column=1, padx=5, pady=2)

settings_button = ttk.Button(top_frame, text="Settings", command=open_settings, width=10)
settings_button.grid(row=0, column=2, padx=5, pady=2)

help_button = ttk.Button(top_frame, text="Help", command=show_help, width=10)
help_button.grid(row=0, column=3, padx=5, pady=2)

elapsed_time_label = ttk.Label(top_frame, text="Elapsed time: 0.00 seconds")
elapsed_time_label.grid(row=0, column=4, padx=5, pady=2)


content_frame = ttk.Frame(root)
content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


content_frame.grid_rowconfigure(0, weight=1)
content_frame.grid_columnconfigure(0, weight=1)
content_frame.grid_columnconfigure(1, weight=1)


input_text = ScrolledText(content_frame, height=20, width=50)
input_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

output_text = ScrolledText(content_frame, height=20, width=50)
output_text.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

generate_button = ttk.Button(content_frame, text="Generate BibTeX", command=generate_bibtex_threaded)
generate_button.grid(row=2, column=0, pady=10, padx=10, sticky="ew")

copy_button = ttk.Button(content_frame, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.grid(row=2, column=1, pady=10, padx=10, sticky="ew")


root.mainloop()