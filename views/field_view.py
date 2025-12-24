import tkinter as tk
import threading
import time
from PIL import Image, ImageTk
from loggings.logger import get_logger
logger = get_logger("FIELD_VIEW")

class FieldCell:
    def __init__(self, root, x, y, index, game):
        try:
            self.state = "locked"       #  "locked"  | growing | ready
            self.plant = None
            self.fertilizer = None
            self.game = game
            self.index = index
            self.is_bought = False

            # Основная кнопка грядки 
        
            self.btn = tk.Button(
                root,
                text=f"Грядка {index + 1}\n(не куплена)",
                bg="gray60",
                fg="black",
                font=("Arial", 10),
                command=self.on_click
            )
            self.btn.place(x=x, y=y, width=250, height=250)

            self.label = tk.Label(root, text="Стадия: блок", font=("Arial", 8))
            self.label.place(x=x, y=y + 255, width=250, height=25)

            self.img_label = tk.Label(self.btn, bg="grey60")
            self.img_label.place(x=20, y=20)

            self.photo = None

            self.img_label.bind("<Button-1>", lambda e: self.on_click())
        except Exception as e:
            logger.exception(f"Ошибка при инициализации FieldCell #{index + 1}")

    def on_click(self):
        try:
            if not self.is_bought:
                self.game.open_bed_shop(self)
                return
            if self.state == "empty":
                self.game.open_plant_select(self)
            elif self.state == "ready":
                self.collect()
            logger.debug(f"Клик по грядке #{self.index + 1}, состояние={self.state}, куплена={self.is_bought}") 
        except Exception as e:
            logger.exception(f"Ошибка при клике на грядке #{self.index + 1}")

    def unlock(self):
        try:
            self.is_bought = True
            self.state = "empty"

            self.btn.config(
                text=f"Грядка {self.index + 1}",
                bg="sienna4",
                fg="white"
            )
            self.img_label.config(bg="sienna4")
            self.img_label.place(x=20, y=20)   
            self.label.config(text="Стадия: пусто")
            logger.info(f"Грядка #{self.index + 1} разблокирована")
        except Exception as e:
            logger.exception(f"Ошибка при разблокировке грядки #{self.index + 1}")
   
    
    def set_image(self, image_path, size):
        try:
            img = Image.open(image_path).resize(size)
            self.photo = ImageTk.PhotoImage(img)
            self.img_label.config(image=self.photo)
        except Exception as e:
            logger.error(f"Ошибка загрузки изображения: {image_path} -> {e}")

    def plant_seed(self, plant, fertilizer=None):
        try:
            self.state = "growing"
            self.plant = plant
            self.fertilizer = fertilizer
            self.btn.config(text="", bg="yellow")
            self.label.config(text="Стадия: растёт", fg="yellow")
            self.img_label.config(bg="yellow")
            self.img_label.place(x=20, y=20)
            self.set_image(plant.image_small, (150, 150))

            grow_time = plant.baseGrowTime
            if fertilizer:
                grow_time *= fertilizer.get("multiplier", 1)

            threading.Thread(target=self.grow_timer, args=(grow_time,), daemon=True).start()
            logger.info(f"Рост начат: {plant.name} на грядке #{self.index + 1}")
            logger.debug(f"Время роста: {grow_time} сек, удобрение={self.fertilizer}")
        except Exception as e:
            logger.exception(f"Ошибка при посадке семени на грядке #{self.index + 1}")

    def grow_timer(self, sleep_time):
        try:
            time.sleep(sleep_time)
            self.btn.after(0, self.finish_growing)  
        except Exception as e:
            logger.exception(f"Ошибка в таймере роста грядки #{self.index + 1}")

    def finish_growing(self):
        try:
            self.state = "ready"
            self.label.config(text="Стадия: созрело", fg="green4")
            self.btn.config(text="", bg="green4")
            self.img_label.config(bg="green4")
            self.img_label.place(x=20, y=20)
            self.set_image(self.plant.image_big, (200, 200))
            logger.info(f"Созрело: {self.plant.name} на грядке #{self.index + 1}")
        except Exception as e:
            logger.exception(f"Ошибка при завершении роста на грядке #{self.index + 1}")

    def collect(self):
        try:
            if self.plant is None:
                logger.warning(f"Ничего не собрано: грядка #{self.index + 1} пуста")
                return  # Или покажите сообщение пользователю в GUI
            # Если не None, продолжаем
            logger.info(f"Собран урожай: {self.plant.name} с грядки #{self.index + 1}")
            if not self.plant:
                return  # если грядка пустая — ничего не делаем
    
            self.game.add_item(self.plant.name)

            # Сбрасываем состояние грядки
    
            self.state = "empty"
            self.plant = None
            self.fertilizer = None

   
            self.btn.config(   
                text=f"Грядка {self.index + 1}",
                bg="sienna4",
                fg="white",
                activebackground="sienna4" 
            )

            self.label.config(text="Стадия: пусто")
            self.img_label.config(image="", bg="sienna4")
            self.photo = None
            self.btn.update()
            self.img_label.update()
        except Exception as e:
            logger.exception(f"Ошибка при сборе урожая с грядки #{self.index + 1}")