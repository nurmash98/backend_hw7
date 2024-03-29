from attrs import define
from pydantic import BaseModel

class Flower(BaseModel):
    name: str
    count: int
    cost: int
    id: int = 0


class FlowersRepository:
    flowers: list[Flower]

    def __init__(self):
        self.flowers = [Flower(name = "Rose", count = 10, cost = 5, id = 1)]

    # необходимые методы сюда
    def get_all(self):
        return self.flowers
    
    def get_flower_by_id(self, id):
        for flower in self.flowers:
            if flower.id == id:
                return flower
        return None
   

    def save(self, flower: Flower):
        id = len(self.flowers) + 1
        flower.id = id 
        self.flowers.append(flower)
        return id
    
    def get_flowers_by_cart(self, cart_ids):
        flowers = []
        sum = 0
        for id in cart_ids:
            isHas = False
            for flower in self.flowers:

                if int(id) == flower.id:
                    flowers.append(flower)
                    sum += flower.cost * flower.count
                    isHas = True
                    break 
                    
            if not isHas:
                return None
        return flowers, sum