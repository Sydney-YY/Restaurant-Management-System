from abc import ABC, abstractmethod

class Order(ABC):
    def __init__(self, main, extra):
        self._main = main
        self._extra = extra
        self._status = ""
        self._id = 0

        self._orderTotal = self._main.price
        for side in self._extra.sides:
            self._orderTotal += side.price
        for drink in self._extra.drinks:
            self._orderTotal += drink.price

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def orderTotal(self):
        return self._orderTotal

    @property
    def main(self):
        return self._main

    @property
    def extra(self):
        return self._extra

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, oid):
        self._id = oid
