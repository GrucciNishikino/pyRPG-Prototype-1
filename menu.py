from fuzzywuzzy import fuzz
from termcolor import cprint, colored

from utils import clear

class Menu:
	"""
	Example options:
	{
		"Test1": lambda: func1(),
		"Test2": lambda: func2(),
	}
	Functions MUST return a tuple where the second value is a bool
	Second value action:
	True -> Exit menu
	False -> return to menu after function finishes, useful for "Help" options

	** Options will ignore casing **
	"""
	def __init__(self, options, title = "Pick an option:", titleColor = "cyan"):
		self.options = options
		self.title = title
		self.titleColor = titleColor

	def prompt(self, arg = None):
		clear()
		cprint(self.title, self.titleColor)
		for o in self.options:
			print(" > %s" % (o))
		selection = input("> ")
		t = None
		for o in self.options:
			if fuzz.ratio(selection, o) >= 75:
				t = self.options[o](arg)
				break
		if t != None and t[1]:
			return t[0]
		else:
			return self.prompt(arg)
