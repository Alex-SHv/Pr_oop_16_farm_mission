class BuyDTO:
    def __init__(self, price, fertilizer_name=None, fertilizer_price=0):
        self.price = price
        self.fertilizer_name = fertilizer_name
        self.fertilizer_price = fertilizer_price

    @property
    def total_price(self):
        return self.price + self.fertilizer_price