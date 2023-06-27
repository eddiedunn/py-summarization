import tkinter as tk
from tkinter import  ttk

class View:
    def __init__(self, root, controller, model_names, sources, summary_methods):
        self.controller = controller
        self.root = root
        self.root.title("Summarizer App")
        self.root.geometry('600x500')
        self.root.minsize(600, 500)

        style = ttk.Style(self.root)
        style.theme_use('clam')

        padding = {"padx": 10, "pady": 10}

        self.source_label = ttk.Label(self.root, text="Source")
        self.source_label.grid(row=0, column=0, **padding)
        self.source_var = tk.StringVar(self.root)

        self.source_selector = ttk.OptionMenu(self.root, self.source_var, *sources, command=self.controller.update_source)
        self.source_selector.grid(row=0, column=1, **padding)

        self.file_label = ttk.Label(self.root, text="File")
        self.file_path_label = ttk.Label(self.root, text="")

        self.file_selector_btn = ttk.Button(self.root, text="Select File:", command=self.controller.select_file)

        self.clipboard_filename_label = ttk.Label(self.root, text="Filename for Clipboard Content:")
        self.clipboard_filename_input = ttk.Entry(self.root)

        self.url_label = ttk.Label(self.root, text="URL")
        self.url_input_field = ttk.Entry(self.root)

        self.dest_label = ttk.Label(self.root, text="Destination:")
        self.dest_label.grid(row=3, column=0, padx=10, pady=10)

        self.dest_path_label = ttk.Label(self.root, text="")
        self.dest_path_label.grid(row=3, column=1, padx=10, pady=10)
        

        self.dest_selector_btn = ttk.Button(self.root, text="Select Destination:", command=self.controller.select_dest)
        self.dest_selector_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        
        self.summary_method_label = ttk.Label(self.root, text="Summary Method:")
        self.summary_method_label.grid(row=5, column=0, **padding)
        self.summary_method_var = tk.StringVar(self.root)

        self.summary_method_selector = ttk.OptionMenu(self.root, self.summary_method_var, *summary_methods, command=self.controller.update_summary_method)
        self.summary_method_selector.grid(row=5, column=1, **padding)

        self.model_label = ttk.Label(self.root, text="Select Model:")
        self.model_label.grid(row=6, column=0, **padding)
        self.model_var = tk.StringVar(self.root, value=controller.model.model_var)
        self.model_selector = ttk.OptionMenu(self.root, self.model_var, *model_names, command=self.controller.update_model_and_gui)
        self.model_selector.grid(row=6, column=1, **padding)

        self.summarize_btn = ttk.Button(self.root, text="Summarize", command=self.controller.summarize)
        self.summarize_btn.grid(row=7, column=0, columnspan=2, **padding)

        # Transcribe checkbox
        self.transcribe_var = tk.IntVar()
        self.transcribe_checkbox = ttk.Checkbutton(self.root, text="Transcribe Only", variable=self.transcribe_var, command=self.update_button_text)
        self.transcribe_checkbox.grid(row=8, column=0, columnspan=2, **padding)

        self.status_label = ttk.Label(self.root, text="Status: Ready")
        self.status_label.grid(row=9, column=0, columnspan=2, **padding)

    def update_button_text(self):
        if self.transcribe_var.get() == 1:
            self.summarize_btn.config(text="Transcribe")
        else:
            self.summarize_btn.config(text="Summarize")

    def update_widgets(self, source_type):
        if source_type == "File":
            self.create_file_input()
        elif source_type == "Clipboard":
            self.create_clipboard_input()
        elif source_type == "URL":
            self.create_url_input()

    def create_file_input(self):
        self.remove_existing_input_widgets()
        padding = {"padx": 10, "pady": 10}
        self.file_label.grid(row=1, column=0, **padding)
        self.file_path_label.grid(row=1, column=1, **padding)
        self.file_selector_btn.grid(row=2, column=0, columnspan=2, **padding)

    def create_clipboard_input(self):
        self.remove_existing_input_widgets()
        padding = {"padx": 10, "pady": 10}
        self.clipboard_filename_label.grid(row=1, column=0, **padding)
        self.clipboard_filename_input.grid(row=1, column=1, **padding)

    def create_url_input(self):
        self.remove_existing_input_widgets()
        padding = {"padx": 10, "pady": 10}
        self.url_label.grid(row=1, column=0, **padding)
        self.url_input_field.grid(row=1, column=1, **padding)

    def remove_existing_input_widgets(self):
        self.file_label.grid_remove()
        self.file_path_label.grid_remove()
        self.file_selector_btn.grid_remove()
        self.clipboard_filename_label.grid_remove()
        self.clipboard_filename_input.grid_remove()
        self.url_label.grid_remove()
        self.url_input_field.grid_remove()
