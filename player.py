from termcolor import cprint

from utils import prefixNumber
from effects import *

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
	# a function to be used after the player dies, resets HP, Mana, and effects
	def reset(resetPoints = False):
		self.hp = self.maxHP
		self.mp = self.maxHP
		self.stat_effects = []
		if resetPoints:
			self.points = 0
	def showStats(self):
		print("\nStatistics for: %s\n" % (self.name))
		cprint("Health: %d" % (self.health + sum(map(lambda s: s.health, self.stat_effects))), "red")
		cprint("Mana: %d" % (self.mana + sum(map(lambda s: s.mana, self.stat_effects))), "cyan")
		cprint("Defense: %d" % (self.defense + sum(map(lambda s: s.defense, self.stat_effects))), "blue")
		cprint("Agility: %d" % (self.agility + sum(map(lambda s: s.agility, self.stat_effects))), "yellow")
		cprint("Intelligence: %d" % (self.intelligence + sum(map(lambda s: s.intelligence, self.stat_effects))), "cyan")
		cprint("Charisma: %d" % (self.charisma + sum(map(lambda s: s.charisma, self.stat_effects))), "green")
		cprint("Luck: %d" % (self.luck + sum(map(lambda s: s.luck, self.stat_effects))), "magenta")
		print("Points: %d" % (self.points))
		if len(self.stat_effects) > 0:
			print("\nStatus effects:")
			for s in self.stat_effects:
				cprint("%s: (%s HP %s MP %s STR %s DEF %s AGI %s INT %s CHR %s LUK)" % (s.name, prefixNumber(s.health), prefixNumber(s.mana), prefixNumber(s.strength), prefixNumber(s.defense), prefixNumber(s.agility), prefixNumber(s.intelligence), prefixNumber(s.charisma), prefixNumber(s.luck)), s.color)
			print("\n")