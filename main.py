from CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk
from bs4 import BeautifulSoup
import customtkinter as ctk
import urllib.request
import subprocess
import threading
import requests
import secrets
import string
import sys
import os

def main():
    app = Controller()
    app.app.mainloop()

def err_msg(text):
    CTkMessagebox(title="Error", message=text, icon="cancel", option_focus=1, button_color="#950808", button_hover_color="#630202")

def info_msg(text):
    CTkMessagebox(title="Info", message=text, icon="info", option_focus=1, button_color="#950808", button_hover_color="#630202")

def isWindows():
    if os.name == "nt":
        return True

def set_window_icon(root):
    try:
        if isWindows():
            if getattr(sys, 'frozen', False):
                icon_path = os.path.join(os.path.dirname(sys.executable), 'icon.ico')
                if not os.path.exists(icon_path):
                    icon_path = os.path.join(os.getcwd(), 'icon.ico')
            else:
                icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets/images/icon.ico')
            
            if os.path.exists(icon_path):
                root.iconbitmap(icon_path)
        else:
            if getattr(sys, 'frozen', False):
                icon_path = os.path.join(os.path.dirname(sys.executable), 'icon.png')
                if not os.path.exists(icon_path):
                    icon_path = os.path.join(os.getcwd(), 'icon.png')
            else:
                icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets/images/icon.png')
            
            if os.path.exists(icon_path):
                pil_img = Image.open(icon_path).convert("RGBA")
                imagetk = ImageTk.PhotoImage(pil_img)
                root.iconphoto(False, imagetk)
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
    CURRENT_VERSION = "v2.4.0"
    RETURN_KEY = "<Return>"
    def __init__(self):
        self.different_version = False
        self.app = PassGenApp(self)
        self.button_wiring()
        self.event_wiring()
        self.auto_update_thread()
    
    def set_theme(self):
        theme = self.app.themes.theme_variable.get()
        ctk.set_appearance_mode(theme)
    
    def button_wiring(self):
        buttons_actions = [(self.app.gen_button, self.generate),
                   (self.app.buttons_frame.save_to_txt_button, self.save),
                   (self.app.buttons_frame.copy_button, self.copy),
                   (self.app.buttons_frame.clear_button, self.clear)]
        for button, action in buttons_actions:
            button.configure(command=action)

    def event_wiring(self):
        elements_events = [(self.app.char_frame.char_entry, self.generate),
                          (self.app.gen_button, self.generate),
                          (self.app.buttons_frame.save_to_txt_button, self.save),
                          (self.app.buttons_frame.clear_button, self.clear),
                          (self.app.buttons_frame.copy_button, self.copy)]
        for element, event in elements_events:
            simple_handling(widget=element, key=Controller.RETURN_KEY, event=event)
        self.app.bind("<Button-1>", lambda e: e.widget.focus())

    def is_linux(self):
        return sys.platform.startswith('linux')

    def is_letters_checked(self):
        if self.app.checkboxes.letters_state.get() == "on":
            return True

    def is_space_checked(self):
        if self.app.checkboxes.spaces_state.get() == "on":
            return True
        
    def is_digits_checked(self):
        if self.app.checkboxes.digits_state.get() == "on":
            return True 
        
    def is_punctuation_checked(self):
        if self.app.checkboxes.punctuation_state.get() == "on":
            return True 

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

        self.pool = ""
        
        if self.is_letters_checked():
            self.pool = string.ascii_letters
        
        if self.is_space_checked():
            self.pool = self.pool + " "
        
        if self.is_digits_checked():
            self.pool = self.pool + string.digits
        
        if self.is_punctuation_checked():
            self.pool = self.pool + string.punctuation
        
        if self.pool == "":
            err_msg("Please, check at least one box aside from the 'spaces' one.")
        elif self.pool == " ":
            err_msg("Please, check at least one box aside from the 'spaces' one.")
        else:
            password = ''.join(secrets.choice(self.pool) for _ in range(int(self.app.char_frame.char_entry.get())))
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

    def show_update_window(self):
        self.app.withdraw()
        UpdateWindow(self.app, self)

    def fetch_git_version(self):
        try:
            req_url = "https://github.com/Guilherme-A-Garcia/PassGen/releases/latest"
            req_response = requests.get(req_url)
            soup = BeautifulSoup(req_response.text, 'html.parser')
            git_version = soup.find('span', class_='css-truncate-target').text.strip()
            print(f'GitHub located version: {git_version}')
            
            if git_version != Controller.CURRENT_VERSION:
                self.different_version = True
        except Exception as e:
            print(e)
    
    def auto_update_thread(self):
        def update_thread(inputted_thread):
            if inputted_thread.is_alive():
                self.app.after(10, lambda: update_thread(inputted_thread))
            else:
                print(f"Thread {inputted_thread} ended successfully!")
                if inputted_thread == self.thread1:
                    check_update()
                    
        self.thread1 = threading.Thread(target=self.fetch_git_version)
        self.thread1.start()
        update_thread(self.thread1)
        
        def check_update():
            if self.different_version:
                msg = CTkMessagebox(message="A newer version has been detected, would you like to update?", title='Update Detected', option_1='Yes', option_2='No', option_focus=2, button_color="#950808", button_hover_color="#630202")
                if msg.get() == 'Yes':
                    self.show_update_window()
                    self.thread2 = threading.Thread(target=self.update_app)
                    self.thread2.start()
                    update_thread(self.thread2)
                else:
                    return
                    
    def update_app(self):
        url = ''
        cwd = self.get_app_dir()
        file_path = ''
        
        print("Update directory: ", cwd)
        
        if os.path.exists(cwd):
            if self.is_linux():
                url = 'https://github.com/Guilherme-A-Garcia/PassGen/releases/latest/download/PassGen-x86_64.AppImage'
                file_path = os.path.join(cwd, 'PassGen-x86_64-NEW.AppImage')
            else:
                url = 'https://github.com/Guilherme-A-Garcia/PassGen/releases/latest/download/PassGen.exe'
                file_path = os.path.join(cwd, 'PassGen-NEW.exe')
                
            print("Downloading to: ", file_path)
            
            try:
                urllib.request.urlretrieve(url, file_path)
            except Exception as e:
                err_msg(f"An error has occurred while downloading the update, the application will now close: {e}")
                self.app.destroy()
            success_msg('Update finished successfully. Closing application...')
            self.close_and_rename()
    
    def get_app_dir(self):
        if getattr(sys, 'frozen', False):
            try:
                path = os.path.abspath(sys.argv[0])
                dir_path = os.path.dirname(path)
                if os.path.exists(dir_path):
                    return dir_path
            except Exception:
                pass
            
            try:
                cwd = os.getcwd()
                if os.path.exists(cwd):
                    return cwd
            except Exception:
                pass
            
            try:
                temp_dir = os.path.dirname(sys.executable)
                parent = os.path.abspath(os.path.join(temp_dir, '..'))
                if os.path.exists(parent):
                    return parent
            except Exception:
                pass
        return os.getcwd()
    
    def close_and_rename(self):
        if self.is_linux():
            new_file = 'PassGen-x86_64-NEW.AppImage'
            file_name = 'PassGen-x86_64.AppImage'
            
            cmd = ['sh', '-c', f'(sleep 1; mv "{new_file}" "{file_name}"; chmod +x "{file_name}"; exec "{os.path.abspath(file_name)}") >/dev/null 2>&1']
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True, close_fds=True)
            os.exit(0)
        else:
            cwd = self.get_app_dir()
            
            new_file = 'PassGen-NEW.exe'
            file_name = 'PassGen.exe'
            
            new_file_abs = os.path.join(cwd, new_file)
            file_name_abs = os.path.join(cwd, file_name)
            
            os.system(f'start /b cmd /c "timeout /nobreak > nul 2 & move /y "{new_file_abs}" "{file_name_abs}" >nul 2>&1 &"')
            os._exit(0)
            os.system('exit')
            
        
        self.app.destroy()
        sys.exit()

class PassGenApp(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        ctk.set_appearance_mode("System")

        self.title("PassGen")
        dynamic_res(self, 500, 290)
        self.resizable(False, False)
        set_window_icon(self)

        self.themes = ThemeFrame(self, controller)
        self.themes.pack(anchor="w", padx=10)
        
        self.main_label = ctk.CTkLabel(self, text="Password Generator", font=('', 35), fg_color="transparent")
        self.main_label.pack(pady=(10,0))

        self.char_frame = CharFrame(self)
        self.char_frame.pack(pady=(5,0))
        
        self.checkboxes = CheckboxFrame(self)
        self.checkboxes.pack(pady=10)
        
        self.gen_button = ctk.CTkButton(self, text="Generate", font=("",15), fg_color="#950808", hover_color="#630202", corner_radius=10, border_color="#440000", border_width=1)
        self.gen_button.pack(pady=(3, 0))
        
        self.separator = ctk.CTkFrame(self, height=2, fg_color="#1C1C1C")
        self.separator.pack(fill="x", pady=10, padx=53)

        self.generation_frame = GenerationFrame(self)
        self.generation_frame.pack(pady=(0,5))

        self.buttons_frame = ButtonsFrame(self)
        self.buttons_frame.pack(pady=5)

        self.char_frame.char_entry.focus_set()
        
class UpdateWindow(ctk.CTkToplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.master = master
        self.controller = controller
        
        set_window_icon(self)
        dynamic_res(self, 450, 100)
        self.resizable(False, False)
        self.title('Updating in process...')
        self.bind("<Button-1>", lambda e: e.widget.focus())
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.progress_label1 = ctk.CTkLabel(self, text="Update in progress.", font=("", 20))
        self.progress_label1.pack()
        
        self.progress_label2 = ctk.CTkLabel(self, text="Please, don't close this window while the application is being updated.", font=("", 12))
        self.progress_label2.pack()
        
        self.progress_bar = ctk.CTkProgressBar(self, orientation="horizontal", height=10, width=400, corner_radius=10, progress_color="#770505", fg_color="#808080", mode="indeterminate", border_color="#1d0000", border_width=1)
        self.progress_bar.pack(pady=10)
        self.progress_bar.start()
        
    def on_closing(self):
        self.destroy()
        self.master.destroy()
        

class ThemeFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.initial_theme = ctk.get_appearance_mode()
        self.theme_variable = ctk.StringVar(value=self.initial_theme)
        self.theme_switch = ctk.CTkSwitch(self, text="Toggle themes (Dark/Light)", font=("", 12), progress_color="#630202", fg_color="#630202", variable=self.theme_variable, command=self.controller.set_theme, offvalue="Dark", onvalue="Light")
        self.theme_switch.grid(row=0, column=0, padx=0)

class CharFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

        self.char_label = ctk.CTkLabel(self, text="Set the length:", font=("Arial", 16), fg_color="transparent")
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

        self.generated_entry_label = ctk.CTkEntry(self, state="readonly", font=("Arial", 13,), border_width=1)
        self.g_entry_label_text = ctk.StringVar(value="")
        
        self.generated_entry_label.configure(textvariable=self.g_entry_label_text)
        self.generated_entry_label.grid(column=1, row=0, sticky="NSEW")

class ButtonsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.columnconfigure((0, 2), weight=1)
        self.rowconfigure(0, weight=1)

        self.save_to_txt_button = ctk.CTkButton(self, text="Save", font=("Arial", 12), fg_color="#950808", hover_color="#630202", corner_radius=10, border_color="#440000", border_width=1, width=80, height=22)
        self.save_to_txt_button.grid(row=0, column=0)

        self.clear_button = ctk.CTkButton(self, text="Clear fields", font=("Arial", 12), fg_color="#950808", hover_color="#630202", corner_radius=10, border_color="#440000", border_width=1, width=80, height=22)
        self.clear_button.grid(row=0, column=1, padx=15)

        self.copy_button = ctk.CTkButton(self, text="Copy", font=("Arial", 12), fg_color="#950808", hover_color="#630202", corner_radius=10, border_color="#440000", border_width=1, width=80, height=22)
        self.copy_button.grid(row=0, column=2)

class CheckboxFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.columnconfigure((0,1,2,3,4), weight=1)
        self.rowconfigure(0, weight=1)
        
        self.checkbox_label = ctk.CTkLabel(self, text="Include:", font=("", 15))
        self.checkbox_label.grid(row=0, column=0, padx=10)

        self.letters_state = ctk.StringVar(value="off")
        self.letters = ctk.CTkCheckBox(self, text="letters", corner_radius=5, border_width=2, width=10, fg_color="#950808", hover_color="#630202", font=("", 15), onvalue="on", offvalue="off", variable=self.letters_state)
        self.letters.grid(row=0, column=1)

        self.spaces_state = ctk.StringVar(value="off")
        self.spaces = ctk.CTkCheckBox(self, text="spaces", corner_radius=5, border_width=2, width=10, fg_color="#950808", hover_color="#630202", font=("", 15), onvalue="on", offvalue="off", variable=self.spaces_state)
        self.spaces.grid(row=0, column=2, padx=5)

        self.digits_state = ctk.StringVar(value="off")
        self.digits = ctk.CTkCheckBox(self, text="digits", corner_radius=5, border_width=2, width=10, fg_color="#950808", hover_color="#630202", font=("", 15), onvalue="on", offvalue="off", variable=self.digits_state)
        self.digits.grid(row=0, column=3, padx=5)
        
        self.punctuation_state = ctk.StringVar(value="off")
        self.punctuation = ctk.CTkCheckBox(self, text="punctuation", corner_radius=5, border_width=2, width=10, fg_color="#950808", hover_color="#630202", font=("", 15), onvalue="on", offvalue="off", variable=self.punctuation_state)
        self.punctuation.grid(row=0, column=4)
        
if __name__ == "__main__":
    main()
