import tkinter as tk, random, string, os, sys
from tkinter import messagebox, filedialog, Label, Button, Entry, Frame, ttk

# Functions

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

def generate():
    value = char_entry.get().strip()
    
    if not value:
        err_msg("Please, enter a number of characters.")
        char_entry.focus_set()
        return
    
    if not value.isdigit():
        err_msg("Please, enter a valid number of characters to be generated.")
        char_entry.select_range(0, tk.END)
        char_entry.focus_set()
        return
    
    char_count = int(value)

    if char_count <= 5:
        err_msg("Too short. \nThe minimum length is 6 for better security.")
        char_entry.select_range(0, tk.END)
        char_entry.focus_set()
        return
    
    if char_count > 300:
        err_msg("Too long. \nThe maximum length is 300.")
        char_entry.select_range(0, tk.END)
        char_entry.focus_set()
        return

    pool = " " + string.ascii_letters + string.digits + string.punctuation
    password =  ''.join(random.choices(pool, k=int(char_entry.get())))
    g_entry_label_text.set(password)
    info_msg("Password generated successfully.")


def clear():
    char_entry.delete(0, tk.END)
    if not g_entry_label_text.get():
        err_msg("There is nothing to be cleared.")
    else:
        g_entry_label_text.set("")
        info_msg("All fields have been cleared successfully.")

def save():
    if not g_entry_label_text.get():
        err_msg("There is nothing to be saved. Try generating a password first.")
    else:
        file = filedialog.asksaveasfile(title="Select a directory", defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        print(file)
        if file:
            try:
                file.write(generated_entry_label.get())
                file.close()
            except Exception as e:
                err_msg(f"Error: {e}")

def copy():
    if not g_entry_label_text.get():
        err_msg("There is nothing to be copied. Try generating a password first.")
    else:
        text = generated_entry_label.get()
        mainroot.clipboard_clear()
        mainroot.clipboard_append(text)

# Main instance and loose code

if __name__ == '__main__':
    KEY_RETURN = '<Return>'

    mainroot = tk.Tk()
    mainroot.bind("<Button-1>", lambda e: e.widget.focus())
    mainroot.title("PassGen")
    dynamic_res(mainroot, 500, 280)
    mainroot.resizable(False, False)
    set_window_icon(mainroot)

    main_label = Label(text="Password Generator", font=("Arial", 20))
    main_label.pack(pady=(25,0))

    char_frame = Frame(mainroot)
    char_frame.pack(pady=(20,0))
    char_frame.columnconfigure((0, 1), weight=1)
    char_frame.rowconfigure(0, weight=1)

    char_label = Label(char_frame, text="Enter the character amount:", font=("Arial", 13))
    char_label.grid(column=0, row=0)

    char_entry = Entry(char_frame, bd=0, relief="solid", font=("Arial", 13), insertwidth=1, highlightcolor="#8d8d8d", highlightbackground="#d3d3d3", highlightthickness=1)
    char_entry.grid(column=1, row=0)
    simple_handling(char_entry, KEY_RETURN, generate)

    gen_button = Button(mainroot, text="Generate", font=("",15), command=generate, )
    gen_button.pack(pady=15)
    simple_handling(gen_button, KEY_RETURN, generate)

    separator = ttk.Separator(mainroot, orient=tk.HORIZONTAL)
    separator.pack(fill="x", pady=(0,15), padx=53)

    generated_frame = Frame(mainroot, highlightcolor="gray", highlightbackground="gray", highlightthickness=1)
    generated_frame.pack(pady=(0,5))
    generated_frame.columnconfigure((0, 1), weight=1)
    generated_frame.rowconfigure(0, weight=1)

    generated_label = Label(generated_frame, text="Password generated: ", font=("", 13))
    generated_label.grid(column=0, row=0)

    generated_entry_label = Entry(generated_frame, state="readonly", font=("Arial", 13,), fg="black", bd=0)
    g_entry_label_text = tk.StringVar(value="")
    generated_entry_label.config(textvariable=g_entry_label_text)
    generated_entry_label.grid(column=1, row=0)

    buttons_frame = Frame(mainroot)
    buttons_frame.pack(pady=5)
    char_frame.columnconfigure((0, 2), weight=1)
    char_frame.rowconfigure(0, weight=1)

    save_to_txt_button = Button(buttons_frame, text="Save", font=("Arial", 12), command=save)
    save_to_txt_button.grid(row=0, column=0)
    simple_handling(save_to_txt_button, KEY_RETURN, save)

    clear_button = Button(buttons_frame, text="Clear fields", font=("Arial", 12), command=clear)
    clear_button.grid(row=0, column=1, padx=5)
    simple_handling(clear_button, KEY_RETURN, clear)

    copy_button = Button(buttons_frame, text="Copy", font=("Arial", 12), command=copy)
    copy_button.grid(row=0, column=2)
    simple_handling(copy_button, KEY_RETURN, copy)

    char_entry.focus_set()
    mainroot.mainloop()
