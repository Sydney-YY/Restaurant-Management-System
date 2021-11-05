from burger_system import BurgerSystem
from main import Main
from bun import Bun
from patty import Patty
from ingredient import Ingredient

class TestCreateMain():
	def setup_method(self):
		#creating menu; not testing prices so all prices are 1
		menu = {
			#creating buns
			"bun": {
				"regular": Bun("regular", 1),
				"sesame": Bun("sesame", 1),
			},
			#creating patties
			"patty": {
				"beef": Patty("beef", 1),
				"chicken": Patty("chicken", 1),
				"vegetarian": Patty("vegetarian", 1),
			},
			#creating ingredients
			"ingredient": {
				"cheese": Ingredient("cheese", 1),
				"lettuce": Ingredient("lettuce", 1),
				"pickle": Ingredient("pickle", 1),
				"sauce": Ingredient("sauce", 1),
				"tomato": Ingredient("tomato", 1),
			}
		}
		self.menu = menu

		#creating max for patty and bun
		self.main = Main(1, 3, 2)

		#creating inventory
		#self.sys = BurgerSystem(menu)

		#bun inventory
		#sys.inventory.bunInventory.setQuantity("regular", 6)
		#sys.inventory.bunInventory.setQuantity("sesame", 6)

		#patty inventory
		#sys.inventory.pattyInventory.setQuantity("beef", 3)
		#sys.inventory.pattyInventory.setQuantity("chicken", 3)
		#sys.inventory.pattyInventory.setQuantity("vegetarian", 3)

		#ingredient inventory
		#sys.inventory.ingredientInventory.setQuantity("cheese", 6)
		#sys.inventory.ingredientInventory.setQuantity("lettuce", 6)
		#sys.inventory.ingredientInventory.setQuantity("pickle", 6)
		#sys.inventory.ingredientInventory.setQuantity("sauce", 6)
		#sys.inventory.ingredientInventory.setQuantity("tomato", 6)

	def test_valid_bun_name(self):
		result = self.main.addBun(self.menu["bun"]["regular"])
		assert(result == None)

	def test_invalid_bun_name1(self):
		try:
			result = self.main.addBun(self.menu["bun"]["tasty"])
		except:
			assert(KeyError)
		else:
			assert(False)
	def test_invalid_bun_name2(self):
		try:
			result = self.main.addBun(self.menu["notabun"]["regular"])
		except:
			assert(KeyError)
		else:
			assert(False)

	def test_invalid_bun_name3(self):
		try:
			result = self.main.addBun(self.menu["notabun"]["tasty"])
		except:
			assert(KeyError)
		else:
			assert(False)

	def test_bun_number_exceed_max(self):
		try:
			self.main.addBun(self.menu["bun"]["regular"])
			self.main.addBun(self.menu["bun"]["regular"])
			self.main.addBun(self.menu["bun"]["regular"])
			self.main.addBun(self.menu["bun"]["regular"])
		except Exception:
			assert("Exceed max bun num")
		else:
			assert(False)
	
	def test_valid_patty_name(self):
		result = self.main.addPatty(self.menu["patty"]["chicken"])
		assert(result == None)

	def test_invalid_patty_name1(self):
		try:
			result = self.main.addPatty(self.menu["patty"]["tasty"])
		except:
			assert(KeyError)
		else:
			assert(False)
	def test_invalid_patty_name2(self):
		try:
			result = self.main.addPatty(self.menu["notapatty"]["chicken"])
		except:
			assert(KeyError)
		else:
			assert(False)

	def test_invalid_patty_name3(self):
		try:
			result = self.main.addPatty(self.menu["notapatty"]["tasty"])
		except:
			assert(KeyError)
		else:
			assert(False)
	
	def test_patty_number_exceed_max(self):
		try:
			self.main.addPatty(self.menu["patty"]["chicken"])
			self.main.addPatty(self.menu["patty"]["chicken"])
			self.main.addPatty(self.menu["patty"]["chicken"])
		except Exception:
			assert("Exceed max patty num")
		else:
			assert(False)
