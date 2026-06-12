import tkinter as tk
import interface

def main():
    root = tk.Tk()
    
    root.title("Mistrz Klawiatury")
    root.resizable(False, False)
    
    app = interface.MistrzKlawiaturyUI(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()