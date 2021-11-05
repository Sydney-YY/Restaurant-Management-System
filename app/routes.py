from app import app
import pickle
import traceback
from decimal import *
from flask import render_template, request, flash, redirect, url_for, g, abort
from app.backend.burger_system import BurgerSystem, STATUS_READY, STATUS_FAIL
from app.backend.order import Order
from app.backend.main import Main
from app.backend.extra import Extra
from app.backend.drink import Drink
from app.backend.bun import Bun
from app.backend.patty import Patty
from app.backend.side import Fries, Nugget
from app.backend.ingredient import Ingredient

menu = {
    "bun": {
        "sesame": Bun("sesame", Decimal('0.2')),
        "muffin": Bun("muffin", Decimal('0.2')),
    },
    "patty": {
        "chicken": Patty("chicken", Decimal('0.4')),
        "vegetarian": Patty("vegetarian", Decimal('0.3')),
        "beef": Patty("beef", Decimal('0.5')),
    },
    "ingredient": {
        "tomato": Ingredient("tomato", Decimal('0.05')),
        "lettuce": Ingredient("lettuce", Decimal('0.05')),
        "tomato_sauce": Ingredient("tomato sauce", Decimal('0.01')),
        "cheddar_cheese": Ingredient("cheddar cheese", Decimal('0.01')),
    },
    "drink": {
        "cola_small": Drink("cola", Decimal('0.3'), "small"),
        "cola_medium": Drink("cola", Decimal('0.4'), "medium"),
        "cola_large": Drink("cola", Decimal('0.5'), "large"),
        "sprite_small": Drink("sprite", Decimal('0.3'), "small"),
        "sprite_medium": Drink("sprite", Decimal('0.4'), "medium"),
        "sprite_large": Drink("sprite", Decimal('0.5'), "large")
    },
    "side": {
        "fries_small": Fries("fries", Decimal('0.3'), "small"),
        "fries_medium": Fries("fries", Decimal('0.4'), "small"),
        "fries_large": Fries("fries", Decimal('0.5'), "small"),
        "nugget_small": Nugget("nugget", Decimal('0.3'), 6),
        "nugget_medium": Nugget("nugget", Decimal('0.4'), 9),
        "nugget_large": Nugget("nugget", Decimal('0.5'), 12),
    }
}

try:
    fr = open('system.pkl', 'rb')
    system = pickle.load(fr)
    fr.close()
except:
    system = BurgerSystem(menu)
    # set inventory
    system.inventory.bunInventory.setQuantity("sesame", 10)
    system.inventory.bunInventory.setQuantity("muffin", 10)

    system.inventory.pattyInventory.setQuantity("chicken", 5)
    system.inventory.pattyInventory.setQuantity("vegetarian", 5)
    system.inventory.pattyInventory.setQuantity("beef", 5)

    system.inventory.ingredientInventory.setQuantity("tomato", 10)
    system.inventory.ingredientInventory.setQuantity("lettuce", 10)
    system.inventory.ingredientInventory.setQuantity("tomato sauce", 10)
    system.inventory.ingredientInventory.setQuantity("cheddar cheese", 10)

    system.inventory.drinkInventory.setQuantity("sprite", 5, "bottle")
    system.inventory.drinkInventory.setQuantity("cola", 10, "can")

    system.inventory.sideInventory.setQuantity("nugget", 100)
    system.inventory.sideInventory.setQuantity("fries", 1000)

@app.route('/')
@app.route('/index', methods=['GET'])
def home():
    return render_template("home.html")
@app.route('/user_order', methods=['GET'])
def user_order():
    return render_template("order.html")

@app.route('/user_order_base', methods=['GET', 'POST'])
def user_order_base():
    if request.method=='POST':
        try:
            main_type = request.form['maintype']
            if main_type == 'burger':
                main = Main("buger", Decimal(1.5), 4, 3)
                main.addBun(system.menu["bun"]["sesame"])
                main.addBun(system.menu["bun"]["sesame"])
                main.addPatty(system.menu["patty"]["chicken"])
            else:
                main = Main("wrap", Decimal(1.0), 1, 1)
                main.addBun(system.menu["bun"]["sesame"])
                main.addPatty(system.menu["patty"]["chicken"])

            extra = Extra()
            for k, v in request.form.items():
                if v == '':
                    continue
                if k == 'maintype':
                    continue
                v = int(v)
                a, b = k.split(':')
                if a == 'drink':
                    for i in range(v):
                        extra.addDrink(system.menu[a][b])
                elif a == 'side':
                    for i in range(v):
                        extra.addSide(system.menu[a][b])
                else:
                    continue

            # add order
            order = Order(main, extra)
            if system.addOrder(order):
                return render_template("success.html", order_id=order.id, price=order.orderTotal)
            else:
                return render_template("fail.html", error_msg="Insuffient resources")
        except Exception as e:
            traceback.print_exc()
            return render_template("fail.html", error_msg=e)
    return render_template("order_base.html", inven=system.inventory)

@app.route('/user_order_custom', methods=['GET', 'POST'])
def user_order_custom():
    if request.method=='POST':
        try:
            main_type = request.form['maintype']
            if main_type == 'burger':
                base_price = 1.5
            else:
                base_price = 1.0

            main = Main(main_type, Decimal(base_price), 4, 3)
            extra = Extra()
            for k, v in request.form.items():
                if k == 'maintype':
                    continue
                if v == '':
                    continue
                v = int(v)
                a, b = k.split(':')
                if a == 'bun':
                    for i in range(v):
                        main.addBun(system.menu[a][b])
                elif a == 'patty':
                    for i in range(v):
                        main.addPatty(system.menu[a][b])
                elif a == 'ingredient':
                    for i in range(v):
                        main.addIngredient(system.menu[a][b])
                elif a == 'drink':
                    for i in range(v):
                        extra.addDrink(system.menu[a][b])
                elif a == 'side':
                    for i in range(v):
                        extra.addSide(system.menu[a][b])
                else:
                    continue

            # add order
            order = Order(main, extra)
            if system.addOrder(order):
                return render_template("success.html", order_id=order.id, price=order.orderTotal)
            else:
                return render_template("fail.html", error_msg="Insuffient resources")
        except Exception as e:
            return render_template("fail.html", error_msg=e)
    return render_template("order_custom.html", inven=system.inventory)

@app.route('/order_list', methods=['GET'])
def orders():
    return render_template('order_list.html', orders=system.orders)

@app.route('/order_ready', methods=['GET'])
def make_order():
    order_id=request.args.get("order_id")
    order_id=int(order_id)
    system.makeOrder(order_id)
    save()
    return redirect(url_for('orders'))

@app.route('/change_order_status', methods=['GET'])
def delete_order():
    order_id=request.args.get("order_id")
    order_id = int(order_id)
    system.removeOrder(order_id)
    save()
    return redirect(url_for('orders'))

@app.route('/inventory_manager', methods=['GET', 'POST'])
def inventories():
    if request.method == 'POST':
        for k, v in request.form.items():
            v = int(v)
            a, b = k.split(':')
            if a == 'bun':
                system.inventory.bunInventory.setQuantity(b, v)
            elif a == 'patty':
                system.inventory.pattyInventory.setQuantity(b, v)
            elif a == 'ingredient':
                system.inventory.ingredientInventory.setQuantity(b, v)
            elif a == 'drink':
                system.inventory.drinkInventory.setQuantity(b, v)
            elif a == 'side':
                system.inventory.sideInventory.setQuantity(b, v)
            else:
                continue
        save()
        return render_template("inventories.html", inven=system.inventory)
    return render_template("inventories.html", inven=system.inventory)

def save():
    fw = open('system.pkl', 'wb')
    pickle.dump(system, fw, -1)
    fw.close()
