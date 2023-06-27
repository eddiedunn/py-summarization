from view import View
import tkinter as tk
import os
import json

class Controller:
    def __init__(self, root, model):
        self.model = model
        self.load_settings()
        self.sources = ["", "File", "Clipboard", "URL"]
        self.summary_methods = ["", "Simple", "Bullet-points"]
        self.model_names = [model['model_name'] for model in self.llm_models]


        self.view = View(root, self, self.model_names, self.sources, self.summary_methods)

        



        # Ensure the correct GUI elements are visible
        self.view.update_widgets(self.source_type)

    def load_settings(self):
        self.settings = self.load_json("settings.json")
        self.llm_models = self.load_json("openai_llm_models.json")

        self.dest_dir = self.settings.get('destination_directory', '')
        self.source_type = self.settings.get('source_type', 'Clipboard')
        self.summary_method = self.settings.get('summary_method', 'Simple')
        model_name_from_settings = self.settings.get('model_name', self.model_names[0])

        if model_name_from_settings in self.model_names:
            self.model_var.set(model_name_from_settings)
        else:
            self.model_var.set(self.model_names[0])

        model_settings = self.get_model_settings(self.model_var.get())

    def load_json(self, filename):
        """Loads a JSON file and returns its content."""
        with open(filename, 'r') as f:
            return json.load(f)

    def get_model_settings(self, model_name):
        """Returns the settings for the specified model."""
        for model in self.llm_models:
            if model['model_name'] == model_name:
                return model
        return None
            
    def update_button_text(self):
        self.view.update_button_text(self.model.update_button_text())

    def update_model(self, model_name):
        if self.model.update_model(model_name, self.models[model_name]["max_tokens"]):
            self.save_settings()  # Save the settings when model is updated


    def update_source(self, source_type):
        self.source_type = source_type  # Save the new source type in the instance variable
        self.model.update_source(source_type)
        self.view.update_widgets(source_type)
        self.save_settings()  # Save the settings when source is updated



    def update_summary_method(self, summary_method):
        self.model.update_summary_method(summary_method)
        self.save_settings()  # Save the settings when summary method is updated

    def select_file(self):
        self.model.set_file_path(self.view.get_file_path())
        self.view.update_file_path_label(self.model.get_file_path())

    def select_dest(self):
        new_dest_dir = self.view.get_dest_directory()
        if new_dest_dir:  # A new directory was selected
            self.model.update_dest_dir(new_dest_dir)
            self.view.update_dest_label(new_dest_dir)
            self.dest_dir = new_dest_dir  # save the destination directory in the instance variable
            self.save_settings()  # save the settings with the updated destination directory


    def summarize(self):
        source_type = self.view.get_source_type()
        is_clipboard = False
        if source_type == 'URL':
            url = self.view.get_url()
            full_content_path, error = self.model.download_url(url)
            if error:
                self.view.display_message("Error", f"Failed to download URL: {error}")
            else:
                self.view.display_message("Information", f"URL downloaded successfully to {full_content_path}!")
        elif source_type == 'Clipboard':
            is_clipboard = True
            full_content_path = self.view.get_clipboard_filename()
        else:  # File
            full_content_path = self.model.get_file_path()

        full_content_path = self.model.transcribe_file(full_content_path, is_clipboard)
        self.summarize_file(full_content_path)

    def summarize_file(self, full_content_path):
        summary_path = self.model.summarize_file(full_content_path)
        self.view.open_file(summary_path)

    def update_model_and_gui(self, model_name):
        if self.model.update_model(model_name, self.models[model_name]["max_tokens"]):
            self.model_var.set(model_name)  # Update the GUI
            self.save_settings()  # Save the settings when model is updated




        # Load settings to GUI
        self.view.source_var.set(self.source_type)
        self.view.summary_method_var.set(self.summary_method)
        self.view.model_var.set(self.model_var.get())
        self.view.dest_path_label["text"] = self.dest_dir


    def save_settings(self):
        settings = {
            'destination_directory': self.dest_dir,
            'source_type': self.source_type,
            'summary_method': self.summary_method,
            'model_name': self.model_var.get()
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f)