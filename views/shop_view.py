import tkinter as tk
import threading
import time
from tkinter import messagebox
from loggings.logger import get_logger
logger = get_logger("SHOP_VIEW")

class ShopWindow:
    def __init__(self, parent, game):
        self.game = game

        self.top = tk.Toplevel(parent)
        self.top.title("Магазин")
        self.top.geometry("550x800")

        tk.Label(self.top, text="Баланс:", font=("Arial", 14)).pack()
        self.money_label = tk.Label(self.top, text=f"{self.game.money} ₴",
                                    font=("Arial", 14))
        self.money_label.pack()
        
        tk.Label(self.top, text="\nУдобрения:", font=("Arial", 16)).pack()

        for name, data in self.game.resources.fertilizers.items():
            price = data["price"]
            tk.Button(
                self.top,
                text=f"{name} ({price} ₴)",
                command=lambda n=name: self.buy_fertilizer(n)
            ).pack(pady=3)

        
        tk.Label(self.top, text="\nПродажа урожая:", font=("Arial", 16)).pack()

        self.sell_frame = tk.Frame(self.top)
        self.sell_frame.pack()

        self.refresh_sell_buttons()

    def refresh_sell_buttons(self):
        for widget in self.sell_frame.winfo_children():
            widget.destroy()

        if not self.game.barn_storage:
            tk.Label(self.sell_frame, text="Амбар пуст").pack()
            return

        for name, count in self.game.barn_storage.items():
            tk.Button(
                self.sell_frame,
                text=f"Продать {name} ({count} шт)",
                command=lambda n=name: self.sell(n)
            ).pack(pady=3)

    def sell(self, name):
        try:
            price = 12
            self.game.missions.inc("sold_items")
            self.game.missions.inc("money_earned", price)
            self.game.missions.set_balance(self.game.money)
            self.game.remove_item(name, 1)
            self.game.money += price

            self.money_label.config(text=f"{self.game.money} ₴")
            self.game.view.update_money_label(self.game.money)

            self.refresh_sell_buttons()

            logger.info(f"Продан урожай: {name}, цена: {price}")

        except Exception as e:
            logger.exception(f"Ошибка при продаже урожая: {name}")
            messagebox.showerror("Ошибка", "Ошибка при продаже урожая")
 
    
    def buy_fertilizer(self, name):
        cost = self.game.resources.fertilizers[name]["price"] 

        if self.game.money < cost:
            messagebox.showinfo("Ошибка", "Недостаточно денег!")
            return

        self.game.money -= cost
        self.game.inventory[name] = self.game.inventory.get(name, 0) + 1
        self.money_label.config(text=f"{self.game.money} ₴")        
        self.game.view.update_money_label(self.game.money)

        self.game.refresh_inventory()
        logger.info(f"Куплено удобрение: {name}")
        logger.debug(f"Баланс после покупки: {self.game.money}")