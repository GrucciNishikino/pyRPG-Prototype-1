#Imports
#Haven't used cmd, don't know why it's here. I'll keep it in my back pocket. ~ 5/23/20
import cmd
#Used for long text.
import textwrap
#Used to exit.
import sys
#Used to clear screen. Very important.
import os
#Used for sleep instructions. Also very important.
import time
#Randomizes stuff.
import random
#Self-explanatory.
import math
#Also self-explanatory.
from fuzzywuzzy import fuzz, process
#Also also self-explanatory.
from termcolor import colored, cprint
#Used exactly once in the clear helper function to make sure it runs the right one.
import subprocess
#Using jsonpickle because why the hell not
import jsonpickle

wrapper = textwrap.TextWrapper(width=50)
screen_width = 100
#Helper function so that I don't need to keep typing the try except.
def clear():
	subprocess.call("clear" if os.name == "posix" else "cls", shell=True)
#Player Class
class Player:
	def __init__(self,name,maxHp,hp,maxMp,mp,stat_effects,strength,defense,agility,intelligence,charisma,luck,location):
		self.name = name
		self.maxHp = maxHp
		self.hp = hp
		self.maxMp = maxMp
		self.mp = mp
		self.stat_effects = stat_effects
		self.strength = strength
		self.defense = defense
		self.agility = agility
		self.intelligence = intelligence
		self.charisma = charisma
		self.luck = luck
		self.location = location
	#I pity the fool who doesn't have word wrap on right now. Additionally, I was forced to create the termcolor variables within the method, which is poor practice. Too bad!
	def describe(self):
		self.tcHealth = colored(str(self.hp) + "/" + str(self.maxHp) + " health, ", "green", attrs=["bold","dark"])
		self.tcMagic = colored(str(self.mp) + "/" + str(self.maxMp) + " magic, ", "cyan", attrs=["bold","dark"])
		self.tcStrength = colored(str(self.strength) + " strength, ", "red")
		self.tcDefense = colored(str(self.defense) + " defense, ", "blue")
		self.tcAgility = colored(str(self.agility) + " agility, ", "yellow")
		self.tcIntelligence = colored(str(self.intelligence) + " intelligence, ", "cyan")
		self.tcCharisma = colored(str(self.charisma) + " charisma, ", "green")
		self.tcLuck = colored(str(self.luck) + " luck", "magenta")
		# Hope you've got word wrap on for this one. Also ignore my inconsistent hash count in comments. It just seems right as I make them.
		if self.stat_effects == []:
			return wrapper.fill(self.name + " has " + self.tcHealth + self.tcMagic + "no status effects, " + self.tcStrength + self.tcDefense + self.tcAgility + self.tcIntelligence + self.tcCharisma + "and " + self.tcLuck + ".")
	def whereami(self):
		retVal = self.location.internalName + " is the internal name, and " + self.location.name + " is the title."
		return retVal
#### Class for the various areas of the world. ####
"""
TODO: Navigation, Shops, and battles, IN THAT ORDER!
Children of the Room Class will vary from high encounters and low shops to low encounters and high shops, as well as a dungeon child class. 
Chests and whatnot will be children of the Event Class.
Battles will be a seperate class, but the specifics will be attributes of areas.
"""
#### Shop class. Is subject to change. ####
class Shop:
	def __init__(self,shopkeepText,items,prices,buyType):
		self.shopkeepText = ["Welcome to my shop! Buy or sell?","What would you like to buy?","What would you like to sell?"]
		self.items = []
		self.prices = []
		self.buyType = "all"
	def buysellChoice(self):
		cprint(self.shopkeepText[0], "cyan", attrs=['underline'])
		option = input("> ")
		if option.lower() == "buy":
			self.buyMenu()
		elif option.lower() == "sell":
			self.sellMenu()
		elif option.lower() == "exit":
			return None
		while option.lower() not in ["buy","sell","exit"]:
			cprint("Come again?", "cyan", attrs=['underline'])
			option = input("> ")
			if option.lower() == "buy":
				self.buyMenu()
			elif option.lower() == "sell":
				self.sellMenu()
			elif option.lower() == "exit":
				return None
	def buyMenu(self):
		cprint(self.shopkeepText[1], "cyan", attrs=['underline'])
		pass
	def sellMenu(self):
		cprint(self.shopkeepText[2], "cyan", attrs=['underline'])
		pass
class roomObject:
	def __init__(self,name,description,interactions,secretExit):
		self.name = name
		self.description = description
		self.interactions = interactions
		self.secretExit = secretExit
	def describe(self,description):
		return self.description
class Room:
	# This here? This is ripped straight from the concepts of Zork. It's a smart system.
	# Also, the actions and prepositions are empty because they'll be read from files.
	actions = []
	prepositions = []
	buzzwords = []
	def __init__(self,internalName,name,description,exits,encountersEnabled,encounterPool,shops,objects,secretExits):
		self.internalName = internalName
		self.name = name
		self.description = description
		self.exits = []
		self.encountersEnabled = encountersEnabled
		self.encounterPool = encounterPool
		self.shops = shops
		self.objects = []
		self.secretExits = secretExits
	def describe(self):
		exitList = []
		for i in range(len(self.exits)):
			exitList.append(self.exits[i].name)
		exitRet = ", ".join(exitList)
		objList = []
		for i in range(len(self.objects)):
			objList.append(self.objects[i].name)
		objRet = ", ".join(objList)
		if len(objList) >= 1:
			return print(self.description + " The exits are as follows: " + exitRet + ". The objects here are as follows: " + objRet + ". What do you do?")
		elif len(objList) < 1:
			return print(self.description + " The exits are as follows: " + exitRet + ". What do you do?")
	def parse(self,choice):
		"""
		Prototype 2 will not use this terribleness. The idea here is a ""smart"" parser like that of Zork.
		Just like Zork, it takes one action and up to two objects. Then it uses prepositions to deal with
		things like 'look at' and 'look under' vs just 'look'. Also, once more, I'm sorry to anyone else
		who may be reading this code, it hurt me to write this garbage code just as much as it hurts to
		read it.
		"""
		objectWork = self.objects + self.exits
		### Reading actions etc. from respective files. I hate this. Too bad, it's easier to read.
		with open("./actions.txt", "r") as filehandle:
			for line in filehandle:
				if not line.startswith("#"):
					nextItem = line[:-1]
					self.actions.append(nextItem)
		with open("./prepositions.txt", "r") as filehandle:
			for line in filehandle:
				if not line.startswith("#"):
					nextItem = line[:-1]
					self.prepositions.append(nextItem)
		with open("./buzzwords.txt", "r") as filehandle:
			for line in filehandle:
				if not line.startswith("#"):
					nextItem = line[:-1]
					self.buzzwords.append(nextItem)
		### Now with that terribleness out of the way, we split the input into individual words.
		words = choice.split(" ")
		wordsMinusBuzz = []
		### Find the action.
		for i in words:
			if i in self.actions:
				action = i
				break
		## Check to see if we failed to find a verb
		try:
			action
		except NameError:
			return print("You proceed to do nothing.")
		### Then we have to do it again for the preposition.
		for i in words:
			if i in self.prepositions:
				preposition = i
				break
		## Check to see if we failed to find a preposition.
		try:
			preposition
		except NameError:
			#If preposition = 0, obey proceeds without using it.
			preposition = 0
		### Now we have both prepositions and actions, so we get objects now.
		objectList = []
		for i in words:
			for j in objectWork:
				if i == j.name:
					objectList.append(j)
		### Filter out buzzwords
		buzzwordList = []
		for i in words:
			if i not in self.buzzwords:
				#Iterate over words but add non matches to a different list.
				#This is because you cannot remove from the iterated list.
				wordsMinusBuzz.append(i)
				words = wordsMinusBuzz
		"""#If the user types in bullshit... bullshit just like this fucking block...
		for i in words:
			for j in objectWork:
				if i != j.name:
					if i not in self.actions:
						if i not in self.buzzwords:
							if i not in self.prepositions:
								#Tell them to fuck right off with that word!
								return print("I don't know the word " + i + ".")
		"""
		### All the preliminary checks and categories are done. Now to parse.
		## First we check for special cases.
		if action == "menu":
			return pauseMenu()
		elif action == "quicksave":
			return quicksave()
		elif action == "quickload":
			return quickload()
		elif action == "status":
			return status()
		elif action == "look" and len(words) == 1:
			return None
		else:
			#Here comes hell.
			self.obey(action,preposition,objectList)
	def obey(self,verb,prep,nouns):
		## Fuck this function in advance.
		#Change rooms
		if verb in ["travel","move","go","exit","enter"]:
			verb = "go"
		#Initiate fight
		elif verb in ["attack","fight","kill"]:
			verb = "attack"
		#Describe something
		elif verb in ["look","inspect","examine"]:
			verb = "look"
		#Close something
		elif verb in ["close","shut"]:
			verb = "close"
		#Omitting open because there's only one verb for it.
		#Take something out of inventory
		elif verb in ["drop","put","throw"]:
			verb = "drop"
		#Add item to inventory
		elif verb in ["get","grab","take"]:
			verb = "take"
		#Omitting drink, eat and push, all one case.
		#Also omitting use, one case for many actions, will be able to substitute drink/eat but not vice versa.
		"""
		This is where the fun begins. That's right, another comment block. Each verb only accepts
		some prepositions. You don't attack in something, you just attack something.
		Let's go through all of these.
		Room change verbs will use all except 'at', 'over', 'using', and 'with'. If that's the preposition,
		we have to ask the user to elaborate.
		Battle verbs will use no prepositions, and they will be ignored.
		Description verbs will use 'at', 'in', 'on', 'above', 'below', 'behind', and 'beneath'.
		Closing verbs will taken no prepositions.
		Open takes no prepositions.
		Removal verbs take 'on', 'at', 'over', 'under', and 'to'.
		Addition verbs take 'from', optionally followed by 'under', 'beneath', 'behind',
		'above', and 'over'.
		Drink and eat both optionally take 'from' and nothing else.
		Push takes 'to' after an object followed by a place.
		Use is weird and doesn't employ prepositions.
		"""
		#First we check if preposition/verb combos are invalid.
		if verb == "go" and prep in ["at","over","using","with"] or verb == "go" and prep == 0:
			return "Go where?"
		elif verb == "attack" and prep != 0:
			prep = 0
		elif verb == "look" and prep not in ["at","in","on","above","below","behind","beneath","up","down","left","right","forwards","backwards"]:
			return thePlayer.location.describe()
		elif verb == "close" and prep != 0:
			prep = 0
		elif verb == "open" and prep != 0:
			prep = 0
		elif verb == "drop" and prep not in ["on","at","over","under","to"] and prep != 0:
			prep = 0
		elif verb == "take" and prep not in ["from","under","beneath","behind","above","over"] and prep != 0:
			prep = 0
		elif verb == "drink" and prep != "from" and prep != 0:
			prep = 0
		elif verb == "eat" and prep != "from" and prep != 0:
			prep = 0
		elif verb == "use" and prep != 0:
			prep = 0
		#Next we try and see if the object(s) chosen can be interacted with in the specified way.
		for i in range(len(nouns)):
			#This is here so the code doesn't fucking die like wario does while watching Seinfeld and eating Lays original chips.
			#To be precise, it makes sure the code treats objects as objects and exits as exits.
			try:
				if verb not in nouns[i].interactions:
					return print("You cannot act on that object in that way.")
			except AttributeError:
				if verb != "go":
					return print("You can't perform the following action on exits: " + verb + ".")
		#### Now we act on the object, finally. ####
		## If the object is, in fact, an exit, and the player exits through it, move the player's location to said exit and output relevant data.
		if verb == "go":
			thePlayer.location = nouns[0]
			return print("You go to " + nouns[0].name+ ".")
		## If the object is, in fact, an object, and the player uses a command on it, find out how they're interacting with it.
		for i in range(len(nouns)):
			#Error code just in case I hyucked up earlier. Yes line 277 is a comment as I write this.
			if verb not in nouns[i].interactions:
				return cprint("ERROR: Previous interactionability check failed. Contact developer with this message. Line 277.", "red")
				time.sleep(5)
				raise Exception("Error 277: Interaction check failure.")
		#Too lazy to implement these right now. Someone else who stumbles upon this repo is welcome to, but I'm leaving this for now. Family guy funny haha moments.
		if verb == "look":
			if prep == "up":
				return print("You look up and see... nothing. You just looked outside the prototype. Traumatized, you quickly gaze forwards again. (We don't support that yet, sorry.)")
			elif prep == "down":
				return print("You look down and see... nothing. You just looked into the abyss, and it stared back. Traumatized, you quickly gaze forwards again. (We don't support that yet, sorry.)")
			elif prep == "left":
				return print("You look left, but something is in your eye, forcing your head forwards again as you try to rub it out. (We don't support that yet, sorry.)")
			elif prep == "right":
				return print("Your vision adjusts to the right, but a spectre slaps you, forcing your head to return to a forward facing position. (We don't support that yet, sorry.)")
			elif prep == "forwards":
				return print("You're always facing forwards, silly!")
			elif prep == "backwards":
				return print("Really? No, I'm not letting you break your neck trying.")
			#Look at an object? Describe! Also would work if you looked at an exit, but that's disallowed at, like, line 282. If you can look at an exit, tell me. I fucked up.
			elif prep == "at":
				return print(nouns[0].describe())
		#If the player says to push a pushable object, move it and update any potential secrets.
		if verb == "push":
			try:
				self.objects.remove(nouns[0])
			except IndexError:
				pass
			#Find the key in the secretExits dict that corresponds to the object.
			for key in self.secretExits.keys():
				#I'm a bad programmer. I'm gonna commit this and beg for help. Anyone well versed in python 3, I once more apologize for this mess. Please try your best to fix it.
				try:
					if nouns[0].name == key.name and self.secretExits[key] == False:
						self.secretExits[key] = True
						print("You push the " + nouns[0].name + " away from where it was.")
						self.exits.append(self.secretExits)
						return print("Secret found!")
					else:
						cprint("DEBUG: first obj name " + nouns[0].name,"magenta")
						cprint("DEBUG: key " + str(key),"magenta")
						cprint("DEBUG: secretExits List " + str(self.secretExits),"magenta")
						input("Press enter to scream internally about this crap.")
				except IndexError:
#### Children of Room Class inbound! ####
## A room in a city ##
class CityCell(Room):
	def __init__(self,internalName,name,description,exits,encountersEnabled,encounterPool,shops,objects,secretExits):
		super().__init__(internalName,name,description,exits,encountersEnabled,encounterPool,shops,objects,secretExits)
		self.encountersEnabled = False
		self.encounterPool = None
	def describe(self):
		super().describe()
	def parse(self,choice):
		super().parse(choice)
	def obey(self,verb,prep,nouns):
		super().obey(verb,prep,nouns)
### Generic outdoor parent class. ###
class Outdoors(Room):
	def __init__(self,internalName,name,description,exits,encountersEnabled,encounterPool,shops,objects,secretExits):
		super().__init__(internalName,name,description,exits,encountersEnabled,encounterPool,shops,objects,secretExits)
		self.encountersEnabled = True
		self.shops = False
	def describe(self):
		super().describe()
	def parse(self,choice):
		super().parse(choice)
	def obey(self,verb,prep,nouns):
		super().obey(verb,prep,nouns)
## Different types of outdoor rooms. ##
class Swamp(Outdoors):
	def __init__(self,internalName,name,description,exits,encountersEnabled,encounterPool,shops,objects,secretExits):
		super().__init__(internalName,name,description,exits,encountersEnabled,encounterPool,shops,objects,secretExits)
	def describe(self):
		super().describe()
	def parse(self,choice):
		super().parse(choice)
	def obey(self,verb,prep,nouns):
		super().obey(verb,prep,nouns)
class Plains(Outdoors):
	def __init__(self,internalName,name,description,exits,encountersEnabled,encounterPool,shops,objects,secretExits):
		super().__init__(internalName,name,description,exits,encountersEnabled,encounterPool,shops,objects,secretExits)
	def describe(self):
		super().describe()
	def parse(self,choice):
		super().parse(choice)
	def obey(self,verb,prep,nouns):
		super().obey(verb,prep,nouns)
class Forest(Outdoors):
	def __init__(self,internalName,name,description,exits,encountersEnabled,encounterPool,shops,objects,secretExits):
		super().__init__(internalName,name,description,exits,encountersEnabled,encounterPool,shops,objects,secretExits)
	def describe(self):
		super().describe()
	def parse(self,choice):
		super().parse(choice)
	def obey(self,verb,prep,nouns):
		super().obey(verb,prep,nouns)
class Cave(Outdoors):
	def __init__(self,internalName,name,description,exits,encountersEnabled,encounterPool,shops,objects,secretExits):
		super().__init__(internalName,name,description,exits,encountersEnabled,encounterPool,shops,objects,secretExits)
	def describe(self):
		super().describe()
	def parse(self,choice):
		super().parse(choice)
	def obey(self,verb,prep,nouns):
		super().obey(verb,prep,nouns)
class Desert(Outdoors):
	def __init__(self,internalName,name,description,exits,encountersEnabled,encounterPool,shops,objects,secretExits):
		super().__init__(internalName,name,description,exits,encountersEnabled,encounterPool,shops,objects,secretExits)
	def describe(self):
		super().describe()
	def parse(self,choice):
		super().parse(choice)
	def obey(self,verb,prep,nouns):
		super().obey(verb,prep,nouns)
class Savanna(Outdoors):
	def __init__(self,internalName,name,description,exits,encountersEnabled,encounterPool,shops,objects,secretExits):
		super().__init__(internalName,name,description,exits,encountersEnabled,encounterPool,shops,objects,secretExits)
	def describe(self):
		super().describe()
	def parse(self,choice):
		super().parse(choice)
	def obey(self,verb,prep,nouns):
		super().obey(verb,prep,nouns)
class Snowlands(Outdoors):
	def __init__(self,internalName,name,description,exits,encountersEnabled,encounterPool,shops,objects,secretExits):
		super().__init__(internalName,name,description,exits,encountersEnabled,encounterPool,shops,objects,secretExits)
	def describe(self):
		super().describe()
	def parse(self,choice):
		super().parse(choice)
	def obey(self,verb,prep,nouns):
		super().obey(verb,prep,nouns)
class Jungle(Outdoors):
	def __init__(self,internalName,name,description,exits,encountersEnabled,encounterPool,shops,objects,secretExits):
		super().__init__(internalName,name,description,exits,encountersEnabled,encounterPool,shops,objects,secretExits)
	def describe(self):
		super().describe()
	def parse(self,choice):
		super().parse(choice)
	def obey(self,verb,prep,nouns):
		super().obey(verb,prep,nouns)
class Dungeon(Room):
	def __init__(self,internalName,name,description,exits,encountersEnabled,encounterPool,shops,objects,secretExits):
		super().__init__(internalName,name,description,exits,encountersEnabled,encounterPool,shops,objects,secretExits)
	def describe(self):
		super().describe()
	def parse(self,choice):
		super().parse(choice)
	def obey(self,verb,prep,nouns):
		super().obey(verb,prep,nouns)
#### Title ####
def title_selections():
	option = input("> ")
	if option.lower() == ("play"):
		new_game()
	elif option.lower() == ("load game"):
		pass
		#load_game()
	elif option.lower() == ("help"):
		help()
	elif option.lower() == ("quit"):
		print("Bye bye!")
		sys.exit()
	while option.lower() not in ["play", "load game", "help", "quit"]:
		print("Come again? That's not valid, sorry.")
		option = input("> ")
		if option.lower() == ("play"):
			new_game()
		elif option.lower() == ("load game"):
			pass
			#load_game()
		elif option.lower() == ("help"):
			help()
		elif option.lower() == ("quit"):
			print("Bye bye!")
			sys.exit()

def title_screen():
	clear()
	cprint("############################", "red")
	cprint("#   Text RPG Prototype 1   #", "green")
	cprint("############################", "blue")
	print("          - Play -          ")
	print("          - Load -          ")
	print("          - Help -          ")
	print("          - Quit -          ")
	print("   Copyright 2020 Lololol   ")
	title_selections()

#### Displays help and information. ####
def help():
	print("Welcome to the TEXT RPG PROTOTYPE! Version 1.0, of course.")
	print("- Use 'look' to look around you.")
	print("- Use 'look at', 'inspect', or 'examine' to examine a specific thing.")
	print("- Use 'fight' to pick a fight with someone or something, for better or worse.")
	print("- Use 'enter' or 'go' to enter buildings, caves, or other locations.")
	print("- Winning fights gets you loot, experience, and of course, money.")
	print("All of these things can get you further in the game with ease.")
	print("- If you misspell something, it doesn't matter too much! We knew what you meant.")
	print("- Enjoy my game! *wink*")
	input("#    Press enter to continue    #")
	title_screen()




#### Name and stat rolling, as well as map initialization. ####
def new_game():
	#### This will cause extremely long load times because python. Too bad! Loading an entire world takes time! ####
	## Areas initialized.
	jedboroughPlaza = CityCell("[0,0,0]","plaza","You find yourself in Jedborough, the city of generic adventurer characters. You, however, are slightly less generic due to this self-aware description. Of course the narrative wou- I digress.",[],False,None,None,[],{})
	jedboroughMarket = CityCell("[0,0,1]","marketplace","The Jedborough Marketplace is full of shops, each with a different specialty. Money can be exchanged for goods and services.",[],False,None,[],[],None)
	jedPlazaSewersEntr = Dungeon("[0,-1,0]","sewers","You are in the entrance area of the Sewers of Jedborough. There are monsters lurking.",[],True,"sewers",[],[],{None : False})
	## Linking areas...
	jedboroughPlaza.exits.append(jedboroughMarket)
	jedboroughMarket.exits.append(jedboroughPlaza)
	## Objects initialized.
	jedPlazaManholeCover = roomObject("cover","It's a manhole cover. What did you expect?",["look","push"],"sewer")
	jedboroughPlaza.objects.append(jedPlazaManholeCover)
	## Objects that lead to rooms linked.
	jedboroughPlaza.secretExits.update({jedPlazaManholeCover : False})
	cprint("Adventure is upon us! What is your name, adventurer?", attrs=['underline'])
	name = input("> ")
	cprint("Time to create your stats, " + name + "!", attrs=['underline'])
	time.sleep(0.5)
	points = 5
	strength = 5
	defense = 5
	agility = 5
	intelligence = 5
	charisma = 5
	luck = 5
	#<clusterfuck>
	while True:
		#Prints stats in COLOR!!!
		cprint("Strength: " + str(strength), "red")
		cprint("Defense: " + str(defense), "blue")
		cprint("Agility: " + str(agility), "yellow")
		cprint("Intelligence: " + str(intelligence), "cyan")
		cprint("Charisma: " + str(charisma), "green")
		cprint("Luck: " + str(luck), "magenta")
		print("Points Remaining: " + str(points))
		#Here's the messy part: I suck at python, so I had to do a gajillion nested ifs. More on that in each section.
		print("Would you like to 'add points' to a stat, 'remove points' from a stat, or 'continue' as is?")
		option = input("> ")
		#### I use fuzzywuzzy here to detect if the user types something similar, because typing is hard. This absolutely isn't necessary, but it helps speed up typing a little bit.
		if fuzz.ratio(option.lower(),"add points") >= 70:
			print("How many points would you like to add?")
			#Creates a variable for the number, which has to be used as a string, then converted to an int, then converted to a string again once the math is done. Fuck types.
			count = input("> ")
			#Checks to see if the user accidentally pressed return too soon or entered a non-whole number into the terminal.
			if count.isdigit() == False:
				print("That is not a number of points.")
				time.sleep(2)
				clear()
				continue
			elif int(count) < 0:
				print("That is not a positive number of points.")
				time.sleep(2)
				clear()
				continue
			#This will add the number provided as input to the stat chosen. See above for why I used fuzzy.
			else:
				print("Which stat would you like to add " + count + " points to?")
				stat = input("> ")
				if fuzz.ratio(stat.lower(),"strength") >= 70:
					strength += int(count)
					points -= int(count)
					clear()
				elif fuzz.ratio(stat.lower(),"defense") >= 70:
					defense += int(count)
					points -= int(count)
					clear()
				elif fuzz.ratio(stat.lower(),"agility") >= 70:
					agility += int(count)
					points -= int(count)
					clear()
				elif fuzz.ratio(stat.lower(),"intelligence") >= 70:
					intelligence += int(count)
					points -= int(count)
					clear()
				elif fuzz.ratio(stat.lower(),"charisma") >= 70:
					charisma += int(count)
					points -= int(count)
					clear()
				elif fuzz.ratio(stat.lower(),"luck") >= 70:
					luck += int(count)
					points -= int(count)
					clear()
				else:
					print("What was that?")
					time.sleep(2)
					clear()
					continue
		#Basically identical to the above information about fuzzywuzzy, numbers, etc.
		elif fuzz.ratio(option.lower(),"remove points") >= 70:
			print("How many points would you like to remove?")
			count = input("> ")
			if count.isdigit() == False:
				print("That is not a number of points.")
				time.sleep(2)
				clear()
				continue
			elif int(count) < 0:
				print("That is not a positive number of points.")
				time.sleep(2)
				clear()
				continue
			else:
				print("Which stat would you like to remove points from?")
				stat = input("> ")
				if fuzz.ratio(stat.lower(),"strength") >= 70:
					strength -= int(count)
					points += int(count)
					clear()
				elif fuzz.ratio(stat.lower(),"defense") >= 70:
					defense -= int(count)
					points += int(count)
					clear()
				elif fuzz.ratio(stat.lower(),"agility") >= 70:
					agility -= int(count)
					points += int(count)
					clear()
				elif fuzz.ratio(stat.lower(),"intelligence") >= 70:
					intelligence -= int(count)
					points += int(count)
					clear()
				elif fuzz.ratio(stat.lower(),"charisma") >= 70:
					charisma -= int(count)
					points += int(count)
					clear()
				elif fuzz.ratio(stat.lower(),"luck") >= 70:
					luck -= int(count)
					points += int(count)
					clear()
				else:
					print("What was that?")
					time.sleep(2)
					clear()
					continue
		#Checks if the user is trying to pull a fast one on us.
		elif fuzz.ratio(option.lower(),"continue") >= 70:
			if points < 0:
				print("Your points are below zero. Please rearrange them to be greater than or equal to zero.")
				time.sleep(2)
				continue
			else:
				print("Are you sure? (y or n)")
				option = input("> ")
				if option.lower() == "y":
					cprint("Excellent! Let's continue!", attrs=['underline'])
					time.sleep(2)
					break
				else:
					continue
	#</clusterfuck>
	maxHP = int(math.ceil(strength/2 + defense/2)+20)
	hp = maxHP
	maxMP = int(math.ceil(intelligence/2 + charisma/2)+10)
	mp = maxMP
	clear()
	cprint("Final Stats for " + name + ":", attrs=['underline'])
	cprint("\u001b[1mHP: " + str(maxHP), "green")
	cprint("\u001b[1mMP: " + str(maxMP), "cyan")
	cprint("STR: " + str(strength), "red")
	cprint("DEF: " + str(defense), "blue")
	cprint("AGI: " + str(agility), "yellow")
	cprint("INT: " + str(intelligence), "cyan")
	cprint("CHR: " + str(charisma), "green")
	cprint("LUK: " + str(luck), "magenta")
	time.sleep(2)
	global thePlayer
	thePlayer = Player(name,maxHP,hp,maxMP,mp,[],strength,defense,agility,intelligence,charisma,luck,jedboroughPlaza)
	cprint("Here is your description sheet.", attrs=['underline'])
	time.sleep(2)
	print("You read the description sheet.")
	time.sleep(2)
	print(thePlayer.describe())
	time.sleep(2)
	cprint("Now you are ready, " + thePlayer.name + ". Ready to join the war against {generic villain name}!", attrs=["underline"])
	time.sleep(5)
#Debug	cprint(thePlayer.whereami(), "magenta", attrs=['underline'])
	input("Press enter to continue")
	clear()
	main()

def main():
	"""
	#### Oh boy, here we go. The code you're reading right now is preceded by this formal apology.
	#### I, PiggyClone205, otherwise known by my steam name, Arizona Ranger, apologize for this.
	#### As I write this apology, I haven't even written the code below yet, but I know it will be bad.
	#### I will be violating several programming practices, will likely have ten thousand security holes, et cetera.
	#### I cannot make excuses, I just suck at programming. So, once more, I formally apologize for the mess that,
	#### at the moment, I am about to write.
	#### Good Yard, The Programmer.
	"""
	while True:
		thePlayer.location.describe()
		option = input("> ")
		print("")
		thePlayer.location.parse(option.lower())
		print("")
		time.sleep(1.5)
if __name__ == "__main__":
	clear()
	cprint("WARNING: This game is very memory intensive. Be sure your computer can handle it before you run it.", "red", attrs=["bold","blink","underline"])
	#time.sleep(5)
	input("Press enter to continue after reading the warning.")
	title_screen()