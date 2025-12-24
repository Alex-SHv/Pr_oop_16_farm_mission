class Fertilizer:
    def __init__(self, key, resources):
        data = resources.fertilizers[key]
        self.key = key
        self.name = data["name"]
        self.price = data["price"]
        self.multiplier = data["multiplier"]