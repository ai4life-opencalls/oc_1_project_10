import tkinter as tk
from tkinter import filedialog


def ask_directory(title):
    root = tk.Tk()
    # root.overrideredirect(1)
    root.withdraw()

    sel_dir = filedialog.askdirectory(
        title="Select your data directory",
        mustexist=True,
        parent=root
    )

    root.quit()
    # root.destroy()

    return sel_dir
