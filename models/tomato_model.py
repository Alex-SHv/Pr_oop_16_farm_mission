from pathlib import Path

class Tomato:
    def __init__(self, resources):
        data = resources.plants["tomato"]
        self.key = "tomato" 
        self.name = data["name"]
        self.baseGrowTime = data["baseGrowTime"]
        self.price = data["price"]
        base = Path(resources.images_path) / self.key
        self.image = data["image"]             
        self.image_small = base / data["image"]["small"]
        self.image_big = base / data["image"]["big"]                                  