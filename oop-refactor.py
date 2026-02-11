import tkinter as tk, random, string, os, sys
from tkinter import messagebox, filedialog, Label, Button, Entry, Frame, ttk

def main():
    pass

def simple_handling(widget, key, event):
    widget.bind(key, lambda e: event())

def err_msg(text):
    messagebox.showerror(title="Error", message=text)

def info_msg(text):
    messagebox.showinfo(title="Info", message=text)

def set_window_icon(root):
    try:
        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(os.path.dirname(sys.executable), 'icon.ico')
            if not os.path.exists(icon_path):
                icon_path = os.path.join(os.getcwd(), 'icon.ico')
        else:

            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets/images/icon.ico')
        
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
    except Exception:
        pass

def dynamic_res(d_root, horizontal, vertical):
    screen_height = d_root.winfo_screenheight()
    screen_width = d_root.winfo_screenwidth()
    x = (screen_width // 2) - (horizontal // 2)
    y = (screen_height // 2) - (vertical // 2)
    d_root.geometry(f"{horizontal}x{vertical}+{x}+{y}")


class Controller():
    def __init__(self):
        pass

class PassGenApp(tk.Tk):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

class CharFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

class GenerationFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

class ButtonsFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

if __name__ == "__main__":
    main()