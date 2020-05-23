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
#Me when I don't want to build the game data into the program: I turned my data into a pickle. So bloody funny. Also I have to write the code as code then I can reverse the process.
import pickle
#Also self-explanatory.
from fuzzywuzzy import fuzz, process
#Also also self-explanatory.
from termcolor import colored, cprint

wrapper = textwrap.TextWrapper(width=50)
screen_width = 100

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
	def whereami(self,location):
		retVal = location.internalName + " is the internal name, and " + location.title + " is the title."
		return retVal
#### Class for the various areas of the world. ####
"""
TODO: Navigation, Shops, and battles, IN THAT ORDER!
Children of the Room Class will vary from high encounters and low shops to low encounters and high shops, as well as a dungeon child class. 
Chests and whatnot will be children of the Event Class.
Battles will be a seperate class, but the specifics will be attributes of areas.
"""
class Room:
	def __init__(self,internalName,title,description,exits,encountersEnabled,encounterPool):
		self.internalName = internalName
		self.title = title
		self.description = description
		self.exits = exits
		self.encountersEnabled = encountersEnabled
		self.encounterPool = encounterPool
#### Children of Room Class inbound! ####
## A room in a city ##
class CityCell(Room):
	def __init__(self,internalName,title,description,exits,encountersEnabled,encounterPool):
		self.internalName = internalName
		self.title = title
		self.description = description
		self.exits = exits
		self.encountersEnabled = False
		self.encounterPool = None
### Generic outdoor parent class. ###
class Outdoors(Room):
	def __init__(self,internalName,title,description,exits,encountersEnabled,encounterPool):
		self.internalName = internalName
		self.title = title
		self.description = description
		self.exits = exits
		self.encountersEnabled = True
		self.encounterPool = encounterPool
## Different types of outdoor rooms. ##
class Swamp(Outdoors):
	def __init__(self,internalName,title,description,exits,encountersEnabled,encounterPool):
		self.internalName = internalName
		self.title = title
		self.description = description
		self.exits = exits
		self.encountersEnabled = True
		self.encounterPool = encounterPool
class Plains(Outdoors):
	def __init__(self,internalName,title,description,exits,encountersEnabled,encounterPool):
		self.internalName = internalName
		self.title = title
		self.description = description
		self.exits = exits
		self.encountersEnabled = True
		self.encounterPool = encounterPool
class Forest(Outdoors):
	def __init__(self,internalName,title,description,exits,encountersEnabled,encounterPool):
		self.internalName = internalName
		self.title = title
		self.description = description
		self.exits = exits
		self.encountersEnabled = True
		self.encounterPool = encounterPool
class Cave(Outdoors):
	def __init__(self,internalName,title,description,exits,encountersEnabled,encounterPool):
		self.internalName = internalName
		self.title = title
		self.description = description
		self.exits = exits
		self.encountersEnabled = True
		self.encounterPool = encounterPool
class Desert(Outdoors):
	def __init__(self,internalName,title,description,exits,encountersEnabled,encounterPool):
		self.internalName = internalName
		self.title = title
		self.description = description
		self.exits = exits
		self.encountersEnabled = True
		self.encounterPool = encounterPool
class Savanna(Outdoors):
	def __init__(self,internalName,title,description,exits,encountersEnabled,encounterPool):
		self.internalName = internalName
		self.title = title
		self.description = description
		self.exits = exits
		self.encountersEnabled = True
		self.encounterPool = encounterPool
class Snowlands(Outdoors):
	def __init__(self,internalName,title,description,exits,encountersEnabled,encounterPool):
		self.internalName = internalName
		self.title = title
		self.description = description
		self.exits = exits
		self.encountersEnabled = True
		self.encounterPool = encounterPool
class Jungle(Outdoors):
	def __init__(self,internalName,title,description,exits,encountersEnabled,encounterPool):
		self.internalName = internalName
		self.title = title
		self.description = description
		self.exits = exits
		self.encountersEnabled = True
		self.encounterPool = encounterPool
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
	try:
		os.system('cls')
	except:
		os.system('clear')
	cprint("############################", "red")
	cprint("#   Text RPG Prototype 1   #", "red")
	cprint("############################", "red")
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
	print("- Enjoy my game that I totally didn't copy code for! *wink*")
	input("#    Press any key to continue    #")
	title_screen()

#### Name and stat rolling, as well as map initialization. ####
def new_game():
	#### This will cause extremely long load times because python. Too bad! Loading an entire world takes time! ####
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
		if fuzz.ratio(option.lower(),"add points") >= 85:
			print("How many points would you like to add?")
			#Creates a variable for the number, which has to be used as a string, then converted to an int, then converted to a string again once the math is done. Fuck types.
			count = input("> ")
			#Checks to see if the user accidentally pressed return too soon or entered a non-whole number into the terminal.
			if count.isdigit() == False:
				print("That is not a number of points.")
				time.wait(2)
				continue
			elif int(count) < 0:
				print("That is not a positive number of points.")
				time.wait(2)
				continue
			#This will add the number provided as input to the stat chosen. See above for why I used fuzzy.
			else:
				print("Which stat would you like to add " + count + " points to?")
				stat = input("> ")
				if fuzz.ratio(stat.lower(),"strength") >= 85:
					strength += int(count)
					points -= int(count)
					try:
						os.system('cls')
					except:
						os.system('clear')
				elif fuzz.ratio(stat.lower(),"defense") >= 85:
					defense += int(count)
					points -= int(count)
					try:
						os.system('cls')
					except:
						os.system('clear')
				elif fuzz.ratio(stat.lower(),"agility") >= 85:
					agility += int(count)
					points -= int(count)
					try:
						os.system('cls')
					except:
						os.system('clear')
				elif fuzz.ratio(stat.lower(),"intelligence") >= 85:
					intelligence += int(count)
					points -= int(count)
					try:
						os.system('cls')
					except:
						os.system('clear')
				elif fuzz.ratio(stat.lower(),"charisma") >= 85:
					charisma += int(count)
					points -= int(count)
					try:
						os.system('cls')
					except:
						os.system('clear')
				elif fuzz.ratio(stat.lower(),"luck") >= 85:
					luck += int(count)
					points -= int(count)
					try:
						os.system('cls')
					except:
						os.system('clear')
				else:
					print("What was that?")
					try:
						os.system('cls')
					except:
						os.system('clear')
					continue
		#Basically identical to the above information about fuzzywuzzy, numbers, etc.
		elif fuzz.ratio(option.lower(),"remove points") >= 85:
			print("How many points would you like to remove?")
			count = input("> ")
			if count.isdigit() == False:
				print("That is not a number of points.")
				time.wait(2)
				continue
			elif int(count) < 0:
				print("That is not a positive number of points.")
				time.wait(2)
				continue
			else:
				print("Which stat would you like to remove points from?")
				stat = input("> ")
				if fuzz.ratio(stat.lower(),"strength") >= 85:
					strength -= int(count)
					points += int(count)
					try:
						os.system('cls')
					except:
						os.system('clear')
				elif fuzz.ratio(stat.lower(),"defense") >= 85:
					defense -= int(count)
					points += int(count)
					try:
						os.system('cls')
					except:
						os.system('clear')
				elif fuzz.ratio(stat.lower(),"agility") >= 85:
					agility -= int(count)
					points += int(count)
					try:
						os.system('cls')
					except:
						os.system('clear')
				elif fuzz.ratio(stat.lower(),"intelligence") >= 85:
					intelligence -= int(count)
					points += int(count)
					try:
						os.system('cls')
					except:
						os.system('clear')
				elif fuzz.ratio(stat.lower(),"charisma") >= 85:
					charisma -= int(count)
					points += int(count)
					try:
						os.system('cls')
					except:
						os.system('clear')
				elif fuzz.ratio(stat.lower(),"luck") >= 85:
					luck -= int(count)
					points += int(count)
					try:
						os.system('cls')
					except:
						os.system('clear')
				else:
					print("What was that?")
					try:
						os.system('cls')
					except:
						os.system('clear')
					continue
		#Checks if the user is trying to pull a fast one on us. Inelegant, but too bad!
		elif fuzz.ratio(option.lower(),"continue") >= 85:
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
	cprint("Final Stats:", attrs=['underline'])
	cprint("\u001b[1mHP: " + str(maxHP), "green")
	cprint("\u001b[1mMP: " + str(maxMP), "cyan")
	cprint("STR: " + str(strength), "red")
	cprint("DEF: " + str(defense), "blue")
	cprint("AGI: " + str(agility), "yellow")
	cprint("INT: " + str(intelligence), "cyan")
	cprint("CHR: " + str(charisma), "green")
	cprint("LUK: " + str(luck), "magenta")
	time.sleep(2)
	thePlayer = Player(name,maxHP,hp,maxMP,mp,[],strength,defense,agility,intelligence,charisma,luck,)
	cprint("Here is your description sheet.", attrs=['underline'])
	time.sleep(2)
	print("You read the description sheet.")
	time.sleep(2)
	print(thePlayer.describe())
	time.sleep(2)
	cprint("Now you are ready, " + thePlayer.name + ". Ready to join the war against {generic villain name}!", attrs=["underline"])
	time.sleep(5)
	thePlayer.whereAmI
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
		pass
if __name__ == "__main__":
	title_screen()