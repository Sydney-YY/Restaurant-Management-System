from abc import ABC

class Main(ABC):
    def __init__(self, main_type, base_price, max_bun_num, max_patty_num):
        self._main_type = main_type
        self._base_price = base_price
        self._max_bun_num = max_bun_num
        self._max_patty_num = max_patty_num
        self._buns = []
        self._patties = []
        self._ingredients = []

    @property
    def main_type(self):
        return self._main_type

    @property
    def buns(self):
        return self._buns

    @property
    def patties(self):
        return self._patties

    @property
    def ingredients(self):
        return self._ingredients

    def addBun(self, bun):
        if len(self.buns) >= self._max_bun_num:
            raise Exception("Exceed max bun num")
        self.buns.append(bun)

    def addPatty(self, patty):
        if len(self.patties) >= self._max_patty_num:
            raise Exception("Exceed max patty num")
        self._patties.append(patty)

    def addIngredient(self, ingredient):
        self._ingredients.append(ingredient)

    def removeBun(self, bunNum):
        del self._buns[bunNum]

    def removePatty(self, pattyNum):
        del self._patties[pattyNum]

    @property
    def price(self):
        price = self._base_price
        for bun in self.buns:
            price += bun.price

        for patty in self.patties:
            price += patty.price

        for ingredient in self.ingredients:
            price += ingredient.price

        return price
