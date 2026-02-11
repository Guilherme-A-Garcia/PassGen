import tkinter as tk, random, string, os, sys
from tkinter import messagebox, filedialog, Label, Button, Entry, Frame, ttk

def main():
    pass

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