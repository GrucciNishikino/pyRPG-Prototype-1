from termcolor import cprint

from menu import Menu
from utils import *

def getMenus():
	return {
		"player_init": Menu({
			"add points": lambda arg: player_init_addPoints(arg),
			"continue": lambda arg: player_init_continue(arg)
		})
	}

# player_init menu

def player_init_continue(arg):
	cprint("Good luck, fellow adverturer!", "green")
	return (arg, True)

def player_init_addPoints(player):
	clear()
	player.showStats()
	print("You have: %d points left" % (player.points))
	count = getNumber("How many points do you want to add?")
	if count > player.points or count < 0:
		cprint("You dont have enough points!", "red")
		player_init_addPoints(player)
	m = Menu({
		"Strength": lambda arg: pi_add_stat((arg, count, "strength")),
		"Defense": lambda arg: pi_add_stat((arg, count, "defense")),
		"Agility": lambda arg: pi_add_stat((arg, count, "agility")),
		"Intelligence": lambda arg: pi_add_stat((arg, count, "intelligence")),
		"Charisma": lambda arg: pi_add_stat((player, count, "charisma")),
		"Luck": lambda arg: pi_add_stat((player, count, "luck"))
	}, title="Add points to player", titleColor="blue")
	if count != 0:
		player = m.prompt(player)
	else:
		cprint("Exiting!", "yellow")
	return (player, False)

# add_points submenu

def pi_add_stat(tuple):
	player = tuple[0]
	count = tuple[1]
	stat = tuple[2]
	if stat == "strength":
		player.strength = player.strength + count
	elif stat == "defense":
		player.defense = player.defense + count
	elif stat == "agility":
		player.agility = player.agility + count
	elif stat == "intelligence":
		player.intelligence = player.intelligence + count
	elif stat == "charisma":
		player.charisma = player.charisma + count
	elif stat == "luck":
		player.luck = player.luck + count
	player.points = player.points - count
	return (player, True)
