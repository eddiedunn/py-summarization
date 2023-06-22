import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import json
import os

from file_summarizer import FileSummarizer
from file_downloader import FileDownloader
from file_transcriber import FileTranscriber


from dotenv import load_dotenv
#from cd_summary import parse_title_summary_results

class App:
    def __init__(self, root):

        # Load the models.json file
        with open('models.json', 'r') as f:
            self.models = json.load(f)
        self.model_names = [model['model_name'] for model in self.models]

        # Set the root window properties
        self.root = root
        self.root.title("Summarizer App")
        self.root.geometry('700x500')
        self.root.minsize(700, 500)

        # Use ttk styles for a more modern look
        style = ttk.Style(self.root)
        style.theme_use('clam')  # Use the 'clam' theme if available

        # Set default grid padding
        padding = {"padx": 10, "pady": 10}

        self.sources = ["File", "Clipboard", "URL"]
        self.summary_methods = ['Simple','MapReduce']

        # Source selector label and dropdown
        self.source_label = ttk.Label(self.root, text="Source")
        self.source_label.grid(row=0, column=0, **padding)
        self.source_var = tk.StringVar(self.root)
        self.source_selector = ttk.OptionMenu(self.root, self.source_var, *self.sources, command=self.update_source)
        self.source_selector.grid(row=0, column=1, **padding)

        # File selector label
        self.file_label = ttk.Label(self.root, text="File")
        self.file_label.grid(row=1, column=0, **padding)

        # File path label
        self.file_path_label = ttk.Label(self.root, text="")
        self.file_path_label.grid(row=1, column=1, **padding)

        # File selector button
        self.file_selector_btn = ttk.Button(self.root, text="Select File:", command=self.select_file)
        self.file_selector_btn.grid(row=2, column=1)

        # Add clipboard filename input field label and entry
        self.clipboard_filename_label = ttk.Label(self.root, text="Filename for Clipboard Content:")
        self.clipboard_filename_input = ttk.Entry(self.root)
        self.clipboard_filename_label.grid(row=1, column=0, **padding)
        self.clipboard_filename_input.grid(row=1, column=1, **padding)

        # URL input field label and entry
        self.url_label = ttk.Label(self.root, text="URL")
        self.url_label.grid(row=2, column=0, **padding)
        self.url_input_field = ttk.Entry(self.root)
        self.url_input_field.grid(row=2, column=1, **padding)

        # Destination selector label and button
        self.dest_label = ttk.Label(self.root, text="Destination:")
        self.dest_label.grid(row=3, column=0, **padding)

        # Destination path label
        self.dest_path_label = ttk.Label(self.root, text="")
        self.dest_path_label.grid(row=3, column=1, columnspan=2, **padding)

        self.dest_selector_btn = ttk.Button(self.root, text="Select Destination:", command=self.select_dest)
        self.dest_selector_btn.grid(row=4, column=1)

        # Summary Method selector label and dropdown
        self.summary_method_label = ttk.Label(self.root, text="Summary Method:")
        self.summary_method_label.grid(row=5, column=0, **padding)
        self.summary_method_var = tk.StringVar(self.root)
        self.summary_method_selector = ttk.OptionMenu(self.root, self.summary_method_var, *self.summary_methods, command=self.update_summary_method)
        self.summary_method_selector.grid(row=5, column=1, **padding)

        # Model selector label and dropdown
        self.model_label = ttk.Label(self.root, text="Select Model:")
        self.model_label.grid(row=6, column=0, **padding)
        self.model_var = tk.StringVar(self.root)
        self.model_var.set(self.model_names[0])  # default value
        self.model_selector = ttk.OptionMenu(self.root, self.model_var, *self.model_names, command=self.update_model)
        self.model_selector.grid(row=6, column=1, **padding)
        

        # Summarize button
        self.summarize_btn = ttk.Button(self.root, text="Summarize", command=self.summarize)
        self.summarize_btn.grid(row=7, column=0, columnspan=2, pady=30)



        # Load previous settings if available
        if os.path.isfile("settings.json"):
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.dest_dir = settings.get('destination_directory', '')
                self.source_type = settings.get('source_type', 'Clipboard')
                self.summary_method = settings.get('summary_method', 'Simple')
                # Load model name from settings
                model_name_from_settings = settings.get('model_name', self.model_names[0])
                # If model name from settings is in model_names list, set it as default, else set first model as default
                if model_name_from_settings in self.model_names:
                    self.model_var.set(model_name_from_settings)
                else:
                    self.model_var.set(self.model_names[0])
        else:
            self.dest_dir = ''
            self.source_type = 'Clipboard'
            self.summary_method = 'Simple'
            # Set first model as default if settings file doesn't exist
            self.model_var.set(self.model_names[0])

        # Set the source_var to the loaded source type
        self.source_var.set(self.source_type)
        # Set the summary_method_var to the loaded summary method
        self.summary_method_var.set(self.summary_method)


        self.update_model(self.model_var.get())

        self.update_widgets(self.source_var.get())
        self.update_dest_label()

    def update_model(self, model_name):
        model = next((m for m in self.models if m["model_name"] == model_name), None)
        if model is not None:
            self.max_tokens = model["max_tokens"]
            self.endpoint = model["endpoint"]
            self.save_settings()  # save settings every time a new model is selected
        else:
            raise ValueError(f"No model found with the name {model_name}")

    def update_source(self, source_type):
        self.source_type = source_type
        self.update_widgets(source_type)
        self.save_settings()  # save settings every time a new source type is selected

    def update_summary_method(self, summary_method):
        self.summary_method = summary_method
        self.save_settings()  # save settings every time a new summary method is selected


    def update_widgets(self, source_type):
        if source_type == "URL":
            self.file_label.grid_remove()
            self.file_selector_btn.grid_remove()
            self.file_path_label.grid_remove()
            self.url_label.grid()
            self.url_input_field.grid()
            self.dest_label.grid()
            self.dest_selector_btn.grid()
            self.dest_path_label.grid()
            self.clipboard_filename_label.grid_remove()
            self.clipboard_filename_input.grid_remove()
        elif source_type == "Clipboard":
            self.file_label.grid_remove()
            self.file_selector_btn.grid_remove()
            self.file_path_label.grid_remove()
            self.url_label.grid_remove()
            self.url_input_field.grid_remove()
            self.dest_label.grid_remove()
            self.dest_selector_btn.grid_remove()
            self.dest_path_label.grid_remove()
            self.clipboard_filename_label.grid()
            self.clipboard_filename_input.grid()
        else: # File
            self.file_label.grid()
            self.file_selector_btn.grid()
            self.file_path_label.grid()
            self.url_label.grid_remove()
            self.url_input_field.grid_remove()
            self.dest_label.grid()
            self.dest_selector_btn.grid()
            self.dest_path_label.grid()
            self.clipboard_filename_label.grid_remove()
            self.clipboard_filename_input.grid_remove()


    def select_file(self):
        self.file_path = filedialog.askopenfilename()
        self.file_path_label.config(text=self.file_path)  # Update the file path label with the selected file


    def select_dest(self):
        new_dest_dir = filedialog.askdirectory()
        if new_dest_dir:  # A new directory was selected
            self.dest_dir = new_dest_dir
            # update the destination path label
            self.update_dest_label()
            # save to settings
            self.save_settings()

    def update_dest_label(self):
        self.dest_path_label.config(text=self.dest_dir)
        self.save_settings()

    def save_settings(self):
        settings = {
            'destination_directory': self.dest_dir,
            'source_type': self.source_var.get(),
            'model_name': self.model_var.get(),
            'summary_method': self.summary_method_var.get()
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f)


    def summarize(self):
        source_type = self.source_var.get()
        
        is_clipboard = False
        if source_type == 'URL':
            try:
                file_dl = FileDownloader(self.dest_dir)
                full_content_path = file_dl.download_full_content(self.url_input_field.get())
                messagebox.showinfo("Information", f"URL downloaded successfully to {full_content_path}!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        elif source_type == 'Clipboard':
            is_clipboard = True
            full_content_path = self.clipboard_filename_input.get()
        else: # File
            full_content_path = self.file_path

        transcriber = FileTranscriber(self.dest_dir)
        full_content_path = transcriber.transcribe(full_content_path, is_clipboard)

        self.summarize_file(full_content_path)

            
    def summarize_file(self, full_content_path):
        summarizer = FileSummarizer(self.model_var.get(), self.max_tokens)
        summary_path = summarizer.summarize_file(full_content_path, 
                                                 self.summary_method_var.get(), 
                                                 self.dest_dir)
        self.open_file(summary_path)

    def open_file(self, summary_path):
        if summary_path:
            new_window = tk.Toplevel(root)
            new_window.title(summary_path)

            # Set the window size. Width=800 and Height=600
            new_window.geometry("800x600")

            text_area = scrolledtext.ScrolledText(new_window, wrap = tk.WORD)
            text_area.pack(padx = 10, pady = 10, expand=True, fill='both')

            with open(summary_path, 'r') as file_content:
                text = file_content.read()
            text_area.insert(tk.INSERT, text)




if __name__ == "__main__":
    load_dotenv()
    root = tk.Tk()
    app = App(root)
    root.mainloop()
