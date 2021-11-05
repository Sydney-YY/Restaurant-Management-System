import pytest
from decimal import *
from .backend.burger_system import BurgerSystem, STATUS_READY, STATUS_FAIL
from .backend.order import Order
from .backend.main import Main
from .backend.extra import Extra
from .backend.drink import Drink
from .backend.bun import Bun
from .backend.patty import Patty
from .backend.side import Fries, Nugget
from .backend.ingredient import Ingredient

@pytest.fixture
def sys():
    menu = {
        "bun": {
            "sesame": Bun("sesame", Decimal('0.2')),
            "muffin": Bun("muffin", Decimal('0.2')),
        },
        "patty": {
            "chicken": Patty("chicken", Decimal('0.4')),
            "vegetarian": Patty("vegetarian", Decimal('0.3')),
            "beef": Patty("beef", '0.5'),
        },
        "ingredient": {
            "tamato" : Ingredient("tamato", Decimal('0.05')),
            "lettuce" : Ingredient("lettuce", Decimal('0.05')),
            "tomato sauce": Ingredient("tomato cheese", Decimal('0.01')),
            "cheddar cheese": Ingredient("cheddar cheese", Decimal('0.01')),
        },
        "drink": {
            "cola small": Drink("cola", Decimal('0.3'), "small"),
            "cola medium": Drink("cola", Decimal('0.4'), "medium"),
            "cola large": Drink("cola", Decimal('0.5'), "large"),
            "sprite small": Drink("sprite", Decimal('0.3'), "small"),
            "sprite medium": Drink("sprite", Decimal('0.4'), "medium"),
            "sprite large": Drink("sprite", Decimal('0.5'), "large")
        },
        "side": {
            "fries small": Fries("fries", Decimal('0.3'), "small"),
            "fries medium": Fries("fries", Decimal('0.4'), "small"),
            "fries large": Fries("fries", Decimal('0.5'), "small"),
            "nugget small": Nugget("nugget", Decimal('0.3'), "small"),
            "nugget medium": Nugget("nugget", Decimal('0.4'), "small"),
            "nugget large": Nugget("nugget", Decimal('0.5'), "small"),
        }
    }
    system = BurgerSystem(menu)
    # set inventory
    system.inventory.bunInventory.setQuantity("sesame", 10)
    system.inventory.bunInventory.setQuantity("muffin", 10)

    system.inventory.pattyInventory.setQuantity("chicken", 5)
    system.inventory.pattyInventory.setQuantity("vegetarian", 5)
    system.inventory.pattyInventory.setQuantity("beef", 5)

    system.inventory.ingredientInventory.setQuantity("tamato", 10)
    system.inventory.ingredientInventory.setQuantity("lettuce", 10)
    system.inventory.ingredientInventory.setQuantity("tomato sauce", 10)
    system.inventory.ingredientInventory.setQuantity("cheddar cheese", 10)

    system.inventory.drinkInventory.setQuantity("sprite", 5, "bottle")
    system.inventory.drinkInventory.setQuantity("cola", 10, "can")

    system.inventory.sideInventory.setQuantity("nugget", 100)
    system.inventory.sideInventory.setQuantity("fries", 1000)
    return system


class TestGourmetBurgers():
    def test_make_order(self, sys):
        main = Main('burger', Decimal(1.0), 3, 2)
        main.addBun(sys.menu["bun"]["sesame"])
        main.addBun(sys.menu["bun"]["sesame"])
        main.addPatty(sys.menu["patty"]["chicken"])
        main.addIngredient(sys.menu["ingredient"]["tamato"])
        main.addIngredient(sys.menu["ingredient"]["lettuce"])

        extra = Extra()
        extra.addDrink(sys.menu["drink"]["cola large"])
        extra.addSide(sys.menu["side"]["fries small"])

        # add order
        order = Order(main, extra)
        sys.addOrder(order)
        assert len(sys.orders) == 1
        assert main.price == Decimal('1.9')
        assert order.orderTotal == Decimal('2.7')

        # make order
        res = sys.makeOrder(order.id)
        assert res == True
        assert sys.inventory.ingredientInventory.getQuantity("tamato") == 9
        assert sys.inventory.ingredientInventory.getQuantity("lettuce") == 9
        assert sys.inventory.bunInventory.getQuantity("sesame") == 8
        assert sys.inventory.pattyInventory.getQuantity("chicken") == 4
        assert sys.inventory.sideInventory.getQuantity("fries") == 925
        assert sys.inventory.drinkInventory.getQuantity("cola") == 3100
        assert order.status == STATUS_READY
        
        # remove order
        sys.removeOrder(order.id)
        assert len(sys.orders) == 0

    def test_order_exception(self, sys): 
        # bun num exceeds
        with pytest.raises(Exception):
            main = Main('burger', Decimal(1.0), 2, 1)
            main.addBun(sys.menu["bun"]["sesame"])
            main.addBun(sys.menu["bun"]["sesame"])
            main.addBun(sys.menu["bun"]["sesame"])
        
        # patty num exceeds
        with pytest.raises(Exception):
            main = Main('burger', Decimal(1.0), 2, 1)
            main.addPatty(sys.menu["patty"]["chicken"])
            main.addPatty(sys.menu["patty"]["chicken"])
        
        # unknown bun & patty name
        with pytest.raises(Exception):
            main = Main('burger', Decimal(1.0), 3, 2)
            main.addBun(sys.menu["bun"]["abc"])
            main.addPatty(sys.menu["patty"]["cd"])

        # make a unknown order
        with pytest.raises(Exception):
            sys.makeOrder(123)
    
    def test_insuffient_resource(self, sys):
        main = Main('burger',Decimal(1.0), 3, 2)

        extra = Extra()
        extra.addDrink(sys.menu["drink"]["cola large"])
        extra.addDrink(sys.menu["drink"]["cola large"])
        extra.addDrink(sys.menu["drink"]["cola large"])
        extra.addDrink(sys.menu["drink"]["cola large"])
        extra.addDrink(sys.menu["drink"]["cola large"])
        extra.addDrink(sys.menu["drink"]["cola large"])
        extra.addDrink(sys.menu["drink"]["cola large"])
        extra.addDrink(sys.menu["drink"]["cola large"])
        extra.addSide(sys.menu["side"]["fries small"])

        # add order
        order = Order(main, extra)
        # insuffient cola
        assert sys.addOrder(order) == False
