from termcolor import cprint

class Player:
	def __init__(self, name, maxHP, maxMP, strength, defense, agility, intelligence, charisma, luck):
		self.name = name
		self.maxHP = maxHP
		self.health = maxHP
		self.maxMP = maxMP
		self.mana = maxMP
		self.stat_effects = []
		self.strength = strength
		self.defense = defense
		self.agility = agility
		self.intelligence = intelligence
		self.charisma = charisma
		self.luck = luck
		self.points = 5
	# a function to be used after the player dies, resets HP, Mana, and effects
	def reset(resetPoints = False):
		self.hp = self.maxHP
		self.mp = self.maxHP
		self.stat_effects = []
		if resetPoints:
			self.points = 0
	def showStats(self):
		cprint("Health: %d" % (self.health), "red")
		cprint("Mana: %d" % (self.mana), "cyan")
		cprint("Defense: %d" % (self.strength), "blue")
		cprint("Agility: %d" % (self.strength), "yellow")
		cprint("Intelligence: %d" % (self.strength), "cyan")
		cprint("Charisma: %d" % (self.strength), "green")
		cprint("Luck: %d" % (self.strength), "magenta")