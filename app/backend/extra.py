from abc import ABC, abstractmethod

class Extra(ABC):
    def __init__(self):
        self.drinks = []
        self.sides = []

    def getDrinks(self):
        return self.drinks

    def getSides(self):
        return self.sides

    def addDrink(self, drink):
        self.drinks.append(drink)

    def addSide(self, side):
        self.sides.append(side)

    def removeDrink(self, drinkNum):
        del self.drinks[drinkNum]

    def removeSide(self, sideNum):
        del self.drinks[sideNum]
