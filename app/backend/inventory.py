from abc import ABC, abstractmethod
from side import Fries, Nugget

class inventory(ABC):
    def __init__(self):
        self._stocks = {}

    def increase(self, resourceName, amount):
        self._stocks[resourceName] += amount

    def decrease(self, resourceName, amount):
        if self._stocks[resourceName] < amount:
            raise Exception("insuffient [%s]" % resourceName)
        self._stocks[resourceName] -= amount


    def setQuantity(self, resourceName, quantity):
        self._stocks[resourceName] = quantity
    
    def getQuantity(self, resourceName):
        return self._stocks[resourceName]

    @abstractmethod
    def cost(self, obj):
        pass

    @abstractmethod
    def check(self, obj):
        pass


class BunInventory(Inventory):
    def cost(self, buns):
        for bun in buns:
            self.decrease(bun.name, 1)

    def check(self, buns):
        d = {}
        for item in buns:
            d[item.name] = d.get(item.name, 0) + 1

        for k, v in d.items():
            if self.getQuantity(k) < v:
                print("bun insuffient")
                return False
        return True

class PattyInventory(Inventory):
    def cost(self, patties):
        for patty in patties:
            self.decrease(patty.name, 1)

    def check(self, patties):
        d = {}
        for item in patties:
            d[item.name] = d.get(item.name, 0) + 1

        for k, v in d.items():
            if self.getQuantity(k) < v:
                print("patty insuffient")
                return False
        return True

class IngredientInventory(Inventory):
    def cost(self, ingredients):
        for ingredient in ingredients:
            self.decrease(ingredient.name, 1)

    def check(self, ingredients):
        d = {}
        for item in ingredients:
            d[item.name] = d.get(item.name, 0) + 1

        for k, v in d.items():
            if self.getQuantity(k) < v:
                print("ingredient insuffient")
                return False
        return True

class DrinkInventory(Inventory):
    def setQuantity(self, resourceName, quantity, container=None):
        if container is None:
            self._stocks[resourceName] = quantity
        elif container == 'bottle':
            self._stocks[resourceName] = quantity * 600
        elif container == 'can':
            self._stocks[resourceName] = quantity * 375
        else:
            raise Exception("Unknown drink container")

    def check(self, drinks):
        d = {}
        for item in drinks:
            if item.size == 'small':
                d[item.name] = d.get(item.name, 0) + 250
            elif item.size == 'medium':
                d[item.name] = d.get(item.name, 0) + 450
            elif item.size == 'large':
                d[item.name] = d.get(item.name, 0) + 650
            else:
                raise Exception("Unknown drink size")

        for k, v in d.items():
            if self.getQuantity(k) < v:
                print("drink insuffient")
                return False
        return True

    def cost(self, drinks):
        for drink in drinks:
            if drink.size == 'small':
                self.decrease(drink.name, 250)
            elif drink.size == 'medium':
                self.decrease(drink.name, 450)
            elif drink.size == 'large':
                self.decrease(drink.name, 650)
            else:
                raise Exception("Unknown drink size")

class SideInventory(Inventory):
    def check(self, sides):
        d = {}
        for item in sides:
            if type(item) is Fries:
                size = item.size
                if size == 'small':
                    d[item.name] = d.get(item.name, 0) + 75
                elif size == 'medium':
                    d[item.name] = d.get(item.name, 0) + 125
                elif size == 'large':
                    d[item.name] = d.get(item.name, 0) + 175
                else:
                    raise Exception("Unknown fries size")
            elif type(item) is Nugget:
                d[item.name] = d.get(item.name, 0) + item.pack_cnt
            else:
                raise Exception("Unknown side type")

        for k, v in d.items():
            if self.getQuantity(k) < v:
                print("side insuffient")
                return False
        return True

    def cost(self, sides):
        for side in sides:
            if type(side) is Fries:
                size = side.size
                if size == 'small':
                    self.decrease(side.name, 75)
                elif size == 'medium':
                    self.decrease(side.name, 125)
                elif size == 'large':
                    self.decrease(side.name, 175)
                else:
                    raise Exception("Unknown fries size")
            elif type(side) is Nugget:
                self.decrease(side.name, side.pack_cnt)
            else:
                raise Exception("Unknown side type")

class AllInventory(ABC):
    def __init__(self):
        self._bunInventory = BunInventory()
        self._pattyInventory = PattyInventory()
        self._ingredientInventory = IngredientInventory()
        self._drinkInventory = DrinkInventory()
        self._sideInventory = SideInventory()

    @property
    def bunInventory(self):
        return self._bunInventory

    @property
    def pattyInventory(self):
        return self._pattyInventory

    @property
    def ingredientInventory(self):
        return self._ingredientInventory

    @property
    def drinkInventory(self):
        return self._drinkInventory

    @property
    def sideInventory(self):
        return self._sideInventory


    def cost(self, order):
        main = order.main
        extra = order.extra
        self.bunInventory.cost(main.buns)
        self.pattyInventory.cost(main.patties)
        self.ingredientInventory.cost(main.ingredients)
        self.drinkInventory.cost(extra.drinks)
        self.sideInventory.cost(extra.sides)

    def check(self, order):
        main = order.main
        extra = order.extra
        return self.bunInventory.check(main.buns) \
         and self.pattyInventory.check(main.patties) \
         and self.ingredientInventory.check(main.ingredients) \
         and self.drinkInventory.check(extra.drinks) \
         and self.sideInventory.check(extra.sides)
