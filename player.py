from termcolor import cprint

from effects import StatusEffect
import utils

class Player:
	def __init__(self, name, maxHP, maxMP, strength, defense, agility, intelligence, charisma, luck):
		self.name = name
		self.maxHP = maxHP
		self.maxMP = maxMP
		self.health = maxHP
		self.mana = maxMP
		self.stat_effects = []
		self.strength = strength
		self.defense = defense
		self.agility = agility
		self.intelligence = intelligence
		self.charisma = charisma
		self.luck = luck
		self.points = 5
		self.coords = (0, 0)
	# A function to be used after the player dies, resets HP, Mana, and effects, can also reset points and coords
	def reset(self, resetPoints = False, resetCoords = False):
		self.hp = self.maxHP
		self.mp = self.maxHP
		self.stat_effects = []
		if resetPoints:
			self.points = 0
		if resetCoords:
			self.coords = (0, 0)
	def showStats(self):
		print("\nStatistics for: %s\n" % (self.name))
		cprint("Health: %d" % (self.getStats()["health"]), "red")
		cprint("Mana: %d" % (self.getStats()["mana"]), "cyan")
		cprint("Defense: %d" % (self.getStats()["defense"]), "blue")
		cprint("Agility: %d" % (self.getStats()["agility"]), "yellow")
		cprint("Intelligence: %d" % (self.getStats()["intelligence"]), "cyan")
		cprint("Charisma: %d" % (self.getStats()["charisma"]), "green")
		cprint("Luck: %d" % (self.getStats()["luck"]), "magenta")
		if len(self.stat_effects) > 0:
			print("\nStatus effects:")
			for s in self.stat_effects:
				cprint("%s: (%s HP %s MP %s STR %s DEF %s AGI %s INT %s CHR %s LUK)" % (s.name, utils.prefixNumber(s.health), utils.prefixNumber(s.mana), utils.prefixNumber(s.strength), utils.prefixNumber(s.defense), utils.prefixNumber(s.agility), utils.prefixNumber(s.intelligence), utils.prefixNumber(s.charisma), utils.prefixNumber(s.luck)), s.color)
			print("\n")
		else:
			print("\nPlayer has no status effects")
	def getStats(self) -> dict:
		return {
			"health": self.health + sum(map(lambda s: s.health, self.stat_effects)),
			"mana": self.mana + sum(map(lambda s: s.mana, self.stat_effects)),
			"defense": self.defense + sum(map(lambda s: s.defense, self.stat_effects)),
			"agility": self.agility + sum(map(lambda s: s.agility, self.stat_effects)),
			"intelligence": self.intelligence + sum(map(lambda s: s.intelligence, self.stat_effects)),
			"charisma": self.charisma + sum(map(lambda s: s.charisma, self.stat_effects)),
			"luck": self.luck + sum(map(lambda s: s.luck, self.stat_effects))
		}
