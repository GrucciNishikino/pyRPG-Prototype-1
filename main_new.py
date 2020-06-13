import sys
import os
import time
import random
import math
from fuzzywuzzy import fuzz, process
from termcolor import cprint
import jsonpickle

# *.py file imports
import player
from menus import getMenus
from rooms import Room, getRooms
from utils import clear

# title screen

def title_screen():
	options = { 
		"Play": lambda: play(),
		"Load": lambda: load(),
		"Help": lambda: help(),
		"Quit": lambda: sys.exit()
	}
	clear()
	header = "# Text RPG Prototype 1 #"
	cprint(header, "green")
	for o in options:
		pad = " " * (int(len(header) / 2) - len(o))
		print("%s%s%s" % (pad, ("> %s <" % (o)), pad))
	opt = input("> ")
	retry = True
	for o in options:
		if fuzz.ratio(opt.lower(), o.lower()) >= 75:
			if options[o]():
				return
			else:
				break
	cprint("Invalid option!", "red")
	time.sleep(1)
	title_screen()
	return



def main():
	clear()
	title_screen()
	return

# Main menu functions
# If it returns True, it exits the menu, if it returns False, it returns to the menu

def load():
	print("Loading game file...")
	# TODO: Load game file here
	play()
	return True

# This is the best help message i could think of dont bully me
def help():
	cprint("Select an option from the list!", "green")
	return False

# Start the game
def play():
	thePlayer = player.Player(input("What is your name?\n> "), 5, 5, 5, 5, 5, 5, 5, 5)
	print("So the adventure begins... %s\nAgainst the evil {generic_villan_name}!" % (thePlayer.name))
	time.sleep(1)
	thePlayer = getMenus()["player_init"].prompt(thePlayer)

	"""
	NONE -> Nothing special is happening
	"""
	gameState = "NONE"

	# Define all rooms
	map = [
		[getRooms()["main_room"],  getRooms()["debug_room"]],
		[getRooms()["debug_room"], getRooms()["debug_room"]]
	]
	mapSize = (len(map[0]), len(map))
	while gameState != "END":
		r: Room = map[thePlayer.coords[0]][thePlayer.coords[1]]
		if str(r.name).lower() == "debug room":
			r.description = str(r.description).replace("%NAME%", thePlayer.name)
		map[thePlayer.coords[0]][thePlayer.coords[1]] = r
		t = r.getMenu().prompt((thePlayer, map, gameState))
		thePlayer = t[0]
		gameState = t[1]

	return True


# call main because you kinda have to
if __name__ == "__main__":
	main()