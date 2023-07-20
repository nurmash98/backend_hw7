from attrs import define
from pydantic import BaseModel


class Purchase(BaseModel):
    user_id: int = 0
    flower_id: int = 0


class PurchasesRepository:
    purchases: list[Purchase]

    def __init__(self):
        self.purchases = []

    # необходимые методы сюда
    def save(self, purchase: Purchase):
        self.purchases.append(purchase)
    # конец решения

    def get_flowers_id(self, user_id):
        flowers = []
        for purchase in self.purchases:
            if purchase.user_id == user_id:
                flowers.append(purchase.flower_id)
        return flowers