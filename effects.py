class StatusEffect:
	"""
	This class represents a satus effect, which can affect a players stats or other things
	Besides that it looks pretty in Player.showStats()
	If you implement this, feel free to add custom effects
	"""
	def __init__(self, name, color, hp, mana, strength, defense, agility, intelligence, charisma, luck):
		self.name = name
		self.color = color
		self.health = hp
		self.mana = mana
		self.strength = strength
		self.defense = defense
		self.agility = agility
		self.intelligence = intelligence
		self.charisma = charisma
		self.luck = luck