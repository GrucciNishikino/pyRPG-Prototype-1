from fuzzywuzzy import fuzz
from termcolor import cprint, colored

import utils

class Menu:
	"""
	
	Example options:
	options = {
		"Test1": lambda arg: func1(arg),
		"Test2": lambda arg: func2(arg),
	}
	Functions MUST return a tuple where the second value is a bool
	
	Second value action:

	True -> Exit menu
	False -> return to menu after function finishes, useful for "Help" options

	** Options will ignore casing **

	"""
	def __init__(self, options, title = "Pick an option:", titleColor: str = "cyan", description = None):
		if options == None:
			cprint("Menu %s has none options!" % (title), "red");
		self.__options = options
		self.title = title
		self.titleColor = titleColor.lower()
		self.description = description

	def prompt(self, arg = None) -> (object, bool):
		utils.clear()
		cprint(self.title, self.titleColor)

		if self.description != None:
			print("\n%s\n" % (self.description))

		for o in self.__options:
			print(" > %s" % (o))
		selection = input("> ")
		t = None
		for o in self.__options:
			if fuzz.ratio(selection.lower(), o.lower()) >= 75:
				t = self.__options[o](arg)
				break
		if t != None and t[1]:
			return t[0]
		else:
			return self.prompt(arg)
