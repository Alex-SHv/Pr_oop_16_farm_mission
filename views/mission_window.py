import tkinter as tk

class MissionsWindow:
    def __init__(self, parent, mission_manager):
        self.mm = mission_manager

        self.top = tk.Toplevel(parent)
        self.top.title("Миссии")
        self.top.geometry("500x300")

        self.text = tk.Text(self.top, font=("Arial", 11))
        self.text.pack(fill="both", expand=True)

        self.refresh()

    def refresh(self):
        self.text.delete("1.0", tk.END)
        for i, (name, desc, cur, need, done) in enumerate(self.mm.get_status(), start=1):
             status = "✔" if done else "✖"
             self.text.insert(
                 tk.END,
                 f"{i}. {status} {name}  {desc}  {cur}/{need}\n"
             )  
            
      
    