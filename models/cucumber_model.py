from pathlib import Path

class Cucumber:
    def __init__(self, resources):
        data = resources.plants["cucumber"]
        self.key = "cucumber" 
        self.name = data["name"]
        self.baseGrowTime = data["baseGrowTime"]
        self.price = data["price"]
        base = Path(resources.images_path) / self.key
        self.image = data["image"]             
        self.image_small = base / data["image"]["small"]
        self.image_big = base / data["image"]["big"]              