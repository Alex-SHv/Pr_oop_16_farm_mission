from DTO.buyDTO import BuyDTO

class BuyMapper:

    @staticmethod
    def from_resources(resources, fertilizer_name=None):
        price = 50

        if fertilizer_name:
            fert = resources.fertilizers[fertilizer_name]
            return BuyDTO(
                price=price,
                fertilizer_name=fertilizer_name,
                fertilizer_price=fert["price"]
            )

        return BuyDTO(price=price)