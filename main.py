import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import json
import os
from click import open_file
import pyperclip

from file_summarizer import FileSummarizer
from file_downloader import FileDownloader


from dotenv import load_dotenv
#from cd_summary import parse_title_summary_results

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Summarizer App")
        self.root.geometry('600x400')
        self.sources = ["File", "Clipboard", "URL"]
        self.summary_methods = ['Simple','MapReduce']

        # Source selector label and dropdown
        self.source_label = tk.Label(self.root, text="Source")
        self.source_label.grid(row=0, column=0, pady=10)
        self.source_var = tk.StringVar(self.root)
        self.source_var.set(self.sources[0])  # default value
        self.source_selector = tk.OptionMenu(self.root, self.source_var, *self.sources, command=self.update_widgets)
        self.source_selector.grid(row=0, column=1, pady=10)

        # File selector label
        self.file_label = tk.Label(self.root, text="File")
        self.file_label.grid(row=1, column=0, pady=10)

        # File path label
        self.file_path_label = tk.Label(self.root, text="")
        self.file_path_label.grid(row=1, column=1, pady=10)

        # File selector button
        self.file_selector_btn = tk.Button(self.root, text="Select File", command=self.select_file)
        self.file_selector_btn.grid(row=2, column=1)

        # Add clipboard filename input field label and entry
        self.clipboard_filename_label = tk.Label(self.root, text="Filename for Clipboard Content:")
        self.clipboard_filename_input = tk.Entry(self.root)
        self.clipboard_filename_label.grid(row=1, column=0, pady=10)
        self.clipboard_filename_input.grid(row=1, column=1, pady=10)

        # URL input field label and entry
        self.url_label = tk.Label(self.root, text="URL")
        self.url_label.grid(row=2, column=0, pady=10)
        self.url_input_field = tk.Entry(self.root)
        self.url_input_field.grid(row=2, column=1, pady=10)

        # Destination selector label and button
        self.dest_label = tk.Label(self.root, text="Destination:")
        self.dest_label.grid(row=3, column=0, pady=10)

        # Destination path label
        self.dest_path_label = tk.Label(self.root, text="")
        self.dest_path_label.grid(row=3, column=1, columnspan=2, pady=10)

        self.dest_selector_btn = tk.Button(self.root, text="Select Destination", command=self.select_dest)
        self.dest_selector_btn.grid(row=4, column=1)

        # Summary Method selector label and dropdown
        self.summary_method_label = tk.Label(self.root, text="Summary Method")
        self.summary_method_label.grid(row=5, column=0, pady=10)
        self.summary_method_var = tk.StringVar(self.root)
        self.summary_method_var.set(self.summary_methods[0])  # default value
        self.summary_method_selector = tk.OptionMenu(self.root, self.summary_method_var, *self.summary_methods)
        self.summary_method_selector.grid(row=5, column=1, pady=10)

        # Summarize button
        self.summarize_btn = tk.Button(self.root, text="Summarize", command=self.summarize)
        self.summarize_btn.grid(row=6, column=0, columnspan=2, pady=30)



        # Load previous settings if available
        if os.path.isfile("settings.json"):
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.dest_dir = settings.get('destination_directory', '')
                self.source_type = settings.get('source_type', 'Clipboard')
                self.source_var.set(self.source_type)
        else:
            self.dest_dir = ''
            self.source_type = 'Clipboard'

        self.update_widgets(self.source_var.get())
        self.update_dest_label()

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

    def save_settings(self):
        settings = {
            'destination_directory': self.dest_dir,
            'source_type': self.source_var.get()
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

    def summarize(self):
        source_type = self.source_var.get()
        

        if source_type == 'URL':
            try:
                file_dl = FileDownloader(self.dest_dir)
                full_content_path = file_dl.download_full_content(self.url_input_field.get())
                messagebox.showinfo("Information", f"URL downloaded successfully to {full_content_path}!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        elif source_type == 'Clipboard':
            try:
                # Read from clipboard
                clipboard_content = pyperclip.paste()
                filename = self.clipboard_filename_input.get()
                if not filename:
                    filename='clipboard_content.txt'
                # Write to a file
                full_path = os.path.join(self.dest_dir, filename )

                with open(full_path, 'w') as f:
                    f.write(clipboard_content)
                messagebox.showinfo("Information", f"Clipboard saved to:  {full_path}")
            except Exception as e:
                messagebox.showerror("Error", str(e))
                print(e)
        else: # File
            full_content_path = self.file_path
            #

        self.summarize_file(full_content_path)

    def summarize_file(self, full_content_path):
        summarizer = FileSummarizer()
        summary_path = summarizer.summarize_file(full_content_path, self.summary_method_var.get(), self.dest_dir)
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
