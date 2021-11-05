from abc import ABC, abstractmethod

class Side(ABC):
    def __init__(self, name, price):
        self._name = name
        self._price = price

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

class Nugget(Side):
    def __init__(self, name, price, pack_cnt):
        Side.__init__(self, name, price)
        self._pack_cnt = pack_cnt

    @property
    def pack_cnt(self):
        return self._pack_cnt

class Fries(Side):
    def __init__(self, name, price, size):
        Side.__init__(self, name, price)
        self._size = size

    @property
    def size(self):
        return self._size
