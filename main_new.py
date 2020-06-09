import sys
import os
import time
import random
import math
from fuzzywuzzy import fuzz, process
from termcolor import cprint
import jsonpickle

# Code imports
from player import Player
from menus import getMenus
from utils import *

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
	input()
	title_screen()



def main():
	title_screen()
	return

# Main menu functions
# If it returns True, it exits the menu, if it returns False, it returns to the menu

def load():
	print("Loading game file...")
	# TODO: Load game file here
	play()
	return True

def help():
	cprint("Select an option from the list...", "green")
	return False

def play():
	player = Player(input("What is your name?\n> "), 5, 5, 5, 5, 5, 5, 5, 5)
	print("So the adventure begins... %s" % (player.name))
	input()
	player = getMenus()["player_init"].prompt(player)
	return True


# call main
if __name__ == "__main__":
	main()