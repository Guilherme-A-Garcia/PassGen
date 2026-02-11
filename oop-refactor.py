import tkinter as tk, random, string, os, sys
from tkinter import messagebox, filedialog, Label, Button, Entry, Frame, ttk

def main():
    app = Controller()
    app.app.mainloop()

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
        self.app = PassGenApp(self)
        self.app

class PassGenApp(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.bind("<Button-1>", lambda e: e.widget.focus())
        self.title("PassGen")
        dynamic_res(self, 500, 280)
        self.resizable(False, False)
        set_window_icon(self)

        self.main_label = Label(text="Password Generator", font=("Arial", 20))
        self.main_label.pack(pady=(25,0))

        self.char_frame = CharFrame(self)
        self.char_frame.pack(pady=(20,0))

        self.gen_button = Button(self, text="Generate", font=("",15))  # command=generate
        self.gen_button.pack(pady=15)
        # simple_handling(gen_button, KEY_RETURN, generate)

        self.separator = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.separator.pack(fill="x", pady=(0,15), padx=53)

        self.generation_frame = GenerationFrame(self, "gray", 1)
        self.generation_frame.pack(pady=(0,5))

        self.buttons_frame = ButtonsFrame(self)
        self.buttons_frame.pack(pady=5)

        self.char_frame.char_entry.focus_set()

class CharFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

        self.char_label = Label(self, text="Enter the character amount:", font=("Arial", 13))
        self.char_label.grid(column=0, row=0)

        self.char_entry = Entry(self, bd=0, relief="solid", font=("Arial", 13), insertwidth=1, highlightcolor="#8d8d8d", highlightbackground="#d3d3d3", highlightthickness=1)
        self.char_entry.grid(column=1, row=0)
        # simple_handling(char_entry, KEY_RETURN, generate)

class GenerationFrame(tk.Frame):
    def __init__(self, parent, hlcolor, hlthick):
        super().__init__(parent, highlightcolor=hlcolor, highlightbackground=hlcolor, highlightthickness=hlthick)
        self.hlcolor = hlcolor
        self.hlthick = hlthick

        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

        selfgenerated_label = Label(self, text="Password generated: ", font=("", 13))
        selfgenerated_label.grid(column=0, row=0)

        self.generated_entry_label = Entry(self, state="readonly", font=("Arial", 13,), fg="black", bd=0)
        self.g_entry_label_text = tk.StringVar(value="")
        self.generated_entry_label.config(textvariable=self.g_entry_label_text)
        self.generated_entry_label.grid(column=1, row=0)

class ButtonsFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure((0, 2), weight=1)
        self.rowconfigure(0, weight=1)

        self.save_to_txt_button = Button(self, text="Save", font=("Arial", 12))  # command=save
        self.save_to_txt_button.grid(row=0, column=0)
        # simple_handling(self.save_to_txt_button, KEY_RETURN, save)

        self.clear_button = Button(self, text="Clear fields", font=("Arial", 12))  # command=clear
        self.clear_button.grid(row=0, column=1, padx=5)
        # simple_handling(clear_button, KEY_RETURN, clear)

        self.copy_button = Button(self, text="Copy", font=("Arial", 12))  # command=copy
        self.copy_button.grid(row=0, column=2)
        # simple_handling(copy_button, KEY_RETURN, copy)

if __name__ == "__main__":
    main()