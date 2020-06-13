from termcolor import cprint, colored

import menu
import player
import utils

def getRooms() -> dict:
	return {
		"main_room": Room({}, "Jedborough", "green", "You find yourself in Jedborough, the city of generic adventurer characters. You, however, are slightly less generic due to this self-aware description. Of course the narrative wou- I digress.", exits = (True, True, True, True)),
		"debug_room": Room({}, "Debug Room", "red", "You should not be here... NOW SCRAM!", exits = (True, True, True, True))
	}

class Room:
	"""
	A note on how to implement rooms:

	The argument for all options is a Tuple of: (Player, Room[][], string)
	The argument returned must be a Tuple of: (Player, string)

	**The function must return: ((Player, string), bool)**
	"""
	def __init__(self, options, name, color, description, exits = (False, False, False, False)):
		self.__options = options
		self.__name = name
		self.__color = color
		self.__description = description
		self.exits: (bool, bool, bool, bool) = exits # Up, Down, Left, Right
		return
	def openExits(self, sideNos: list):
		for i in sideNos:
			self.exits[i] = True
	def closeExits(self, sideNos: list):
		for i in sideNos:
			self.exits[i] = False
	def getMenu(self) -> menu.Menu:
		return menu.Menu(utils.combine({
			"Exit": lambda arg: self.__exit(arg),
			"Map": lambda arg: self.__map(arg)
		}, self.__options), title = self.__name, titleColor = self.__color, description = self.__description)
	def describe(self):
		cprint(self.__description, self.__color)
	# Default room options
	def __exit(self, arg):
		p = arg[0]
		map = arg[1]
		state = arg[2]
		men = menu.Menu(utils.getExitOptions(p, self, (len(map[0]), len(map))), title = "Pick an exit", titleColor = "Yellow")
		p = men.prompt(p)
		return ((p, state), True)
	def __map(self, arg):
		map = arg[1]
		w = len(map[0])
		h = len(map)
		chars = []
		for y in range(0, h):
			buf1 = []
			buf2 = []
			buf3 = []
			for x in range(0, w):
				buf1.append(" %s " % ("|" if map[x][y].exits[0] and y > 0 else " "))
				buf2.append("%s%s%s" % ("-" if map[x][y].exits[2] and x > 0 else " ", colored("#", "red" if arg[0].coords == (x, y) else "white"), "-" if map[x][y].exits[3] and x < (w - 1) else " "))
				buf3.append(" %s " % ("|" if map[x][y].exits[1] and y < (h - 1) else " "))
				pass
			for l in [buf1, buf2, buf3]:
				for i in l:
					print(i, end = "")
				print("\n", end = "")
		input("Press enter to exit map...")
		return ((arg[0], arg[2]), True)
