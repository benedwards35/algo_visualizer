import tkinter as tk
from ui.app import MainApp

def main():
    root = tk.Tk()
    root.geometry("1200x600")
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()