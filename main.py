import tkinter as tk
from tkinter import ttk

from app import ImageEditorApp


def main():
    root = tk.Tk()

    # ttk Theme
    try:
        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")
    except Exception:
        pass

    ImageEditorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
