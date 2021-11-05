from abc import ABC, abstractmethod

class Drink(ABC):
    def __init__(self, name, price, size):
        self._name = name
        self._price = price
        self._size = size

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        self._price = price

    @property
    def size(self):
        return self._size
