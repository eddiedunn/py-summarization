import tkinter as tk
from controller import Controller
from model import Model
from dotenv import load_dotenv

def main():
    load_dotenv()
    root = tk.Tk()
    model = Model()
    Controller(root, model)
    root.mainloop()

if __name__ == "__main__":
    main()