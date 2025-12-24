import tkinter as tk
from tkinter import messagebox

from views.game_view import GameView
from views.field_view import FieldCell
from views.barn_view import BarnWindow
from views.shop_view import ShopWindow

from models.tomato_model import Tomato
from models.cucumber_model import Cucumber
from models.carrot_model import Carrot
from resources.resources_load import Resources

from DTO.buyMapper import BuyMapper

from loggings.logger import get_logger
logger = get_logger("GAME_CONTROLLER")

from models.mission_manager import MissionManager
from views.mission_window import MissionsWindow

class GameController:
    def __init__(self):
        try:
            # Сначала загрузим ресурсы (чтобы всегда корректно вычислять beds_count, start_money и т.д.)
            self.resources = Resources()
            self.view = GameView(self)

            self.money = self.resources.start_money
            self.inventory = {}
            self.barn_storage = {}
            self.barn_window = None
            self.missions = MissionManager()
            self.missions_window = None
            logger.info("Игра запущена")
            logger.debug(f"Стартовые деньги: {self.money}")

            self.view.create_field_cells(FieldCell, self, self.resources.beds_count)

            self.refresh_money()
            self.refresh_inventory()

            self.view.start()
        except Exception as e:
            logger.exception("Ошибка при инициализации GameController")
   
    # Амбар

    def add_item(self, plant_name):
        try:
            self.barn_storage[plant_name] = self.barn_storage.get(plant_name, 0) + 1
            self.refresh_barn()
        except Exception as e:
            logger.exception(f"Ошибка при добавлении предмета '{plant_name}' в амбар")

    def remove_item(self, name, count):
        try:
            if name in self.barn_storage and self.barn_storage[name] >= count:
                self.barn_storage[name] -= count
                if self.barn_storage[name] == 0:
                    del self.barn_storage[name]
            self.refresh_barn()
        except Exception as e:
            logger.exception(f"Ошибка при удалении предмета '{name}' из амбара")

    def refresh_barn(self):
        try:
            if self.barn_window and self.barn_window.top.winfo_exists():
                self.barn_window.refresh()
        except Exception as e:
            logger.exception("Ошибка при обновлении амбара")

    def open_barn(self):
        try:
            if self.barn_window is None or not self.barn_window.top.winfo_exists():
                self.barn_window = BarnWindow(self.view.root, self.barn_storage)
            else:
                self.barn_window.top.deiconify()
                self.barn_window.top.lift()
            self.refresh_barn()
        except Exception as e:
            logger.exception("Ошибка при открытии амбара")
    
    # Деньги / инвентарь

    def refresh_money(self):
        try:
            self.view.update_money(self.money)
            self.missions.set_balance(self.money)
        except Exception as e:
            logger.exception("Ошибка при обновлении денег")

    def refresh_inventory(self):
        try:
            if not self.inventory:
                self.view.update_inventory("Удобрения: нет")
            else:
                lines = ["Удобрения:"]
                for k, v in self.inventory.items():
                    lines.append(f"{k}: {v}")
                txt = "\n".join(lines)
                self.view.update_inventory(txt)
        except Exception as e:
            logger.exception("Ошибка при обновлении инвентаря")
            
    # Магазин и посадка

    def open_shop(self):
        try:
            ShopWindow(self.view.root, self)
        except Exception as e:
            logger.exception("Ошибка при открытии магазина")

    def open_plant_select(self, field):
        try:
            plants = [Carrot, Tomato, Cucumber]
            self.view.open_plant_window(
                finish_callback=lambda win, plant, fert: self.finish_plant(win, field, plant, fert),
                inventory=self.inventory,
                plants=plants
            )
        except Exception as e:
            logger.exception("Ошибка при открытии выбора растения")

    def finish_plant(self, win, field, plant, fert_name):
        try:
            fert_data = None
            self.missions.inc("planted")

            if fert_name != "Нет":
                self.missions.inc("fertilizers_used")
                fert_data = self.resources.fertilizers[fert_name]
                self.inventory[fert_name] -= 1
                if self.inventory[fert_name] == 0:
                    del self.inventory[fert_name]
           
            logger.info(f"Посадка {plant.name} на грядке #{field.index + 1}, удобрение: {fert_name}")                
            logger.debug(f"Инвентарь удобрений: {self.inventory}")            
            self.refresh_inventory()
            field.plant_seed(plant, fert_data)
            win.destroy()
        except Exception as e:
            logger.exception(f"Ошибка при завершении посадки на грядке #{field.index + 1}")

   #Покупка грядки и грядки + удобрения 
               
    def open_bed_shop(self, field):
        try:
            win = tk.Toplevel(self.view.root)
            win.title("Покупка грядки")
            win.geometry("400x300")
            logger.debug(f"Открыт магазин грядки #{field.index + 1}")

            tk.Label(win, text="Купить грядку", font=("Arial", 14)).pack(pady=10)

            tk.Button(
                win,
                text="Купить грядку (50 ₴)",
                command=lambda: self.buy_bed(field, win)
            ).pack(pady=10)

            tk.Button(
                win,
                text="Купить грядку + удобрение",
                command=lambda: self.buy_bed_with_fert(field, win)
            ).pack(pady=10) 
        except Exception as e:
            logger.exception(f"Ошибка при открытии магазина грядки #{field.index + 1}")
           
    def buy_bed(self, field, win):
        try:
            logger.info(f"Попытка купить грядку #{field.index + 1}")
            self.missions.inc("beds_bought")
            buy_dto = BuyMapper.from_resources(self.resources)
            if self.money < buy_dto.price:
                messagebox.showinfo("Ошибка", "Недостаточно денег")
                return

            logger.info(f"Грядка #{field.index + 1} куплена за {buy_dto.price} ₴")
            self.money -= buy_dto.price
            self.refresh_money()
            field.unlock()
            win.destroy()  
        except Exception as e:
            logger.exception(f"Ошибка при покупке грядки #{field.index + 1}") 
                 
    def buy_bed_with_fert(self, field, win):
        try:
            win.destroy()
            self.view.open_fertilizer_select(
                finish_callback=lambda fert: self.finish_bed_with_fert(field, fert)
            )
        except Exception as e:
            logger.exception(f"Ошибка при покупке грядки с удобрением #{field.index + 1}")

    def finish_bed_with_fert(self, field, fert_name):
        try:
            self.missions.inc("beds_bought")
            buy_dto = BuyMapper.from_resources(
                self.resources,
                fertilizer_name=fert_name
            )                    

            if self.money < buy_dto.total_price:
                messagebox.showinfo("Ошибка", "Недостаточно денег")
                return

            self.money -= buy_dto.total_price
            self.refresh_money()
            self.inventory[buy_dto.fertilizer_name] = \
                self.inventory.get(buy_dto.fertilizer_name, 0) + 1

            self.refresh_inventory()
            field.unlock() 
        except Exception as e:
            logger.exception(f"Ошибка при завершении покупки грядки с удобрением #{field.index + 1}")    
            
    def open_missions(self):
          if self.missions_window is None or not self.missions_window.top.winfo_exists():
              self.missions_window = MissionsWindow(self.view.root, self.missions)
          else:
              self.missions_window.refresh()
              self.missions_window.top.lift()  
                                                                                                                                                                                                                                                                                                                        
 #  СТАРТ #        
          
if __name__ == "__main__":    
    try:
        GameController()
    except Exception as e:
        logger.exception("Критическая ошибка при запуске игры")   