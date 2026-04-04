import tkinter as tk
from system import LibrarySystem
from gui import LibraryGUI

if __name__ == "__main__":
    library = LibrarySystem()
    library.add_sample_books()

    root = tk.Tk()
    app = LibraryGUI(root, library)
    root.mainloop()
