import tkinter as tk


class GameView:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Ферма")
        self.root.geometry("1700x1300")
        self.fields = []

        tk.Button(
            self.root, text="Открыть амбар", font=("Arial", 12),
            command=self.controller.open_barn
        ).place(x=1350, y=50)

        tk.Button(
            self.root, text="Открыть магазин", font=("Arial", 12),
            command=self.controller.open_shop
        ).place(x=1350, y=100)

        tk.Button(
           self.root, text="Миссии", font=("Arial", 12),
           command=self.controller.open_missions
        ).place(x=1350, y=150)

        tk.Button(
            self.root, text="Выход", font=("Arial", 12),
            command=self.root.destroy
        ).place(x=1350, y=200)

        self.money_label = tk.Label(self.root, text="", font=("Arial", 15))
        self.money_label.place(x=1350, y=250)

        self.inv_label = tk.Label(self.root, text="", font=("Arial", 12), justify="left", anchor="nw" )
        self.inv_label.place(x=1350, y=300)

    def open_fertilizer_select(self, finish_callback):
        win = tk.Toplevel(self.root)
        win.title("Выбор удобрения")
        win.geometry("300x300")

        tk.Label(win, text="Выберите удобрение", font=("Arial", 12)).pack(pady=10)

        for name in self.controller.resources.fertilizers.keys():
            tk.Button(
                 win,
                 text=name,
                 command=lambda n=name: (finish_callback(n), win.destroy())
              ).pack(pady=5)


        self.fields = []

    def create_field_cells(self, FieldCellClass, game, beds_count):
        start_x = 100
        start_y = 30
        gap_x = 300
        gap_y = 300
        
        for i in range(beds_count):
            row = i // 4
            col = i % 4
            x = start_x + col * gap_x
            y = start_y + row * gap_y
            cell = FieldCellClass(self.root, x, y, i, game)
            self.fields.append(cell)       

    def update_money(self, money):
        self.money_label.config(text=f"Баланс: {money}₴")

    def update_inventory(self, inv_text):
        self.inv_label.config(text=inv_text)
        
    def update_money_label(self, money):
        self.money_label.config(text=f"Баланс: {money}₴")      

    def open_plant_window(self, finish_callback, inventory, plants):
        win = tk.Toplevel(self.root)
        win.title("Посадка")
        win.geometry("550x600")

        tk.Label(win, text="Выберите растение:", font=("Arial", 14)).pack(pady=10)

        fert_var = tk.StringVar(value="Нет")
        tk.Label(win, text="Удобрение:", font=("Arial", 12)).pack()

        opts = ["Нет"] + list(inventory.keys())
        tk.OptionMenu(win, fert_var, *opts).pack()

        tk.Label(win, text="", font=("Arial", 8)).pack()
        for plant in plants:
            p_obj = plant(self.controller.resources)
            tk.Button(
                 win,
                 text=p_obj.name,
                 command=lambda p=p_obj: finish_callback(win, p, fert_var.get())
            ).pack(pady=5)

        return win

    def start(self):
        self.root.mainloop()