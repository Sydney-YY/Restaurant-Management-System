from abc import ABC
#from inventory import AllInventory
import traceback

STATUS_PREPAREING   = "ORDER_PREPAREING"
STATUS_READY        = "ORDER_READY"
STATUS_FAIL         = "ORDER_FAIL"

class BurgerSystem(ABC):
    def __init__(self, menu):
        self._menu = menu
        self._inventory = AllInventory()
        self._orders = []
        self._oid = 1

    def addOrder(self, order):
        if not self.inventory.check(order):
            return False
        order.id = self._oid
        self._oid += 1
        self._orders.append(order)
        order.status = STATUS_PREPAREING
        return True

    def makeOrder(self, orderId):
        for order in self.orders:
            if order.id == orderId:
                try:
                    self.inventory.cost(order)
                    order.status = STATUS_READY
                except:
                    traceback.print_exc()
                    order.status = STATUS_FAIL
                    return False
                return True
        raise Exception("cannot find order id %s" % orderId)

    def removeOrder(self, orderId):
        res = None
        for order in self.orders:
            if order.id == orderId:
                res = order
        self._orders.remove(res)

    @property
    def orders(self):
        return self._orders

    @property
    def inventory(self):
        return self._inventory

    @property
    def menu(self):
        return self._menu
