from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
import random
import string
import sys
import os

def main():
    app = Controller()
    app.app.mainloop()

def err_msg(text):
    CTkMessagebox(title="Error", message=text, icon="cancel", option_focus=1, button_color="#950808", button_hover_color="#630202", )

def info_msg(text):
    CTkMessagebox(title="Info", message=text, icon="info", option_focus=1, button_color="#950808", button_hover_color="#630202")

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

def simple_handling(widget, key, event):
    widget.bind(key, lambda e: event())

def dynamic_res(d_root, horizontal, vertical):
    screen_height = d_root.winfo_screenheight()
    screen_width = d_root.winfo_screenwidth()
    x = (screen_width // 2) - (horizontal // 2)
    y = (screen_height // 2) - (vertical // 2)
    d_root.geometry(f"{horizontal}x{vertical}+{x}+{y}")


class Controller:
    RETURN_KEY = "<Return>"

    def __init__(self):
        self.app = PassGenApp(self)

        self.app.gen_button.configure(command=self.generate)
        self.app.buttons_frame.save_to_txt_button.configure(command=self.save)
        self.app.buttons_frame.copy_button.configure(command=self.copy)
        self.app.buttons_frame.clear_button.configure(command=self.clear)

        simple_handling(self.app.char_frame.char_entry, Controller.RETURN_KEY, self.generate)
        simple_handling(self.app.gen_button, Controller.RETURN_KEY, self.generate)
        simple_handling(self.app.buttons_frame.save_to_txt_button, Controller.RETURN_KEY, self.save)
        simple_handling(self.app.buttons_frame.clear_button, Controller.RETURN_KEY, self.clear)
        simple_handling(self.app.buttons_frame.copy_button, Controller.RETURN_KEY, self.copy)

        self.app.bind("<Button-1>", lambda e: e.widget.focus())
        
    def generate(self):
        self.value = self.app.char_frame.char_entry.get().strip()
        
        if not self.value:
            err_msg("Please, enter a number of characters.")
            self.app.char_frame.char_entry.focus_set()
            return
        
        if not self.value.isdigit():
            err_msg("Please, enter a valid number of characters to be generated.")
            self.app.char_frame.char_entry.select_range(0, ctk.END)
            self.app.char_frame.char_entry.focus_set()
            return
        
        self.char_count = int(self.value)

        if self.char_count <= 5:
            err_msg("Too short. \nThe minimum length is 6 for better security.")
            self.app.char_frame.char_entry.select_range(0, ctk.END)
            self.app.char_frame.char_entry.focus_set()
            return
        
        if self.char_count > 300:
            err_msg("Too long. \nThe maximum length is 300.")
            self.app.char_frame.char_entry.select_range(0, ctk.END)
            self.app.char_frame.char_entry.focus_set()
            return

        pool = " " + string.ascii_letters + string.digits + string.punctuation
        password =  ''.join(random.choices(pool, k=int(self.app.char_frame.char_entry.get())))
        self.app.generation_frame.g_entry_label_text.set(password)
        info_msg("Password generated successfully.")

    def clear(self):
        self.app.char_frame.char_entry.delete(0, ctk.END)
        if not self.app.generation_frame.g_entry_label_text.get():
            err_msg("There is nothing to be cleared.")
        else:
            self.app.generation_frame.g_entry_label_text.set("")
            info_msg("All fields have been cleared successfully.")
    
    def save(self):
        if not self.app.generation_frame.g_entry_label_text.get():
            err_msg("There is nothing to be saved. Try generating a password first.")
        else:
            self.file = ctk.filedialog.asksaveasfile(title="Select a directory", defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            print(self.file)
            if self.file:
                try:
                    self.file.write(self.app.generation_frame.g_entry_label_text.get())
                    self.file.close()
                except Exception as e:
                    err_msg(f"Error: {e}")
    
    def copy(self):
        if not self.app.generation_frame.g_entry_label_text.get():
            err_msg("There is nothing to be copied. Try generating a password first.")
        else:
            self.text = self.app.generation_frame.generated_entry_label.get()
            self.app.clipboard_clear()
            self.app.clipboard_append(self.text)

class PassGenApp(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._set_appearance_mode("System")

        self.title("PassGen")
        dynamic_res(self, 500, 280)
        self.resizable(False, False)
        set_window_icon(self)

        self.main_label = ctk.CTkLabel(self, text="Password Generator", font=("Arial", 20), fg_color="transparent")
        self.main_label.pack(pady=(25,0))

        self.char_frame = CharFrame(self)
        self.char_frame.pack(pady=(20,0))
        
        self.gen_button = ctk.CTkButton(self, text="Generate", font=("",15), fg_color="#950808", hover_color="#630202", corner_radius=10, border_color="#440000", border_width=1)
        self.gen_button.pack(pady=15)
        
        self.separator = ctk.CTkFrame(self, height=2, fg_color="#1C1C1C")
        self.separator.pack(fill="x", pady=(0,15), padx=53)

        self.generation_frame = GenerationFrame(self)
        self.generation_frame.pack(pady=(0,5))

        self.buttons_frame = ButtonsFrame(self)
        self.buttons_frame.pack(pady=5)

        self.char_frame.char_entry.focus_set()

class CharFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

        self.char_label = ctk.CTkLabel(self, text="Enter the character amount:", font=("Arial", 16), fg_color="transparent")
        self.char_label.grid(column=0, row=0, padx=(0,5))

        self.char_entry = ctk.CTkEntry(self, border_width=1, corner_radius=5, font=("Arial", 13))
        self.char_entry.grid(column=1, row=0)

class GenerationFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3, minsize=230)
        self.rowconfigure(0, weight=1)

        self.generated_label = ctk.CTkLabel(self, text="Generated password: ", font=("Arial", 14), fg_color="transparent")
        self.generated_label.grid(column=0, row=0)

        self.generated_entry_label = ctk.CTkEntry(self, state="readonly", font=("Arial", 13,), border_width=0)
        self.g_entry_label_text = ctk.StringVar(value="")
        
        self.generated_entry_label.configure(textvariable=self.g_entry_label_text)
        self.generated_entry_label.grid(column=1, row=0, sticky="NSEW")

class ButtonsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.columnconfigure((0, 2), weight=1)
        self.rowconfigure(0, weight=1)

        self.save_to_txt_button = ctk.CTkButton(self, text="Save", font=("Arial", 12), fg_color="#950808", hover_color="#630202", corner_radius=10, border_color="#440000", border_width=1)
        self.save_to_txt_button.grid(row=0, column=0)

        self.clear_button = ctk.CTkButton(self, text="Clear fields", font=("Arial", 12), fg_color="#950808", hover_color="#630202", corner_radius=10, border_color="#440000", border_width=1)
        self.clear_button.grid(row=0, column=1, padx=5)

        self.copy_button = ctk.CTkButton(self, text="Copy", font=("Arial", 12), fg_color="#950808", hover_color="#630202", corner_radius=10, border_color="#440000", border_width=1)
        self.copy_button.grid(row=0, column=2)

if __name__ == "__main__":
    main()