import time
from termcolor import cprint

from menu import Menu
import utils

def getMenus() -> list:
	return {
		"player_init": Menu({
			"Add Points": lambda arg: player_init_addPoints(arg),
			"Continue": lambda arg: player_init_continue(arg),
			"Show Stats": lambda arg: player_init_showStats(arg)
		})
	}

# player_init menu

def player_init_showStats(arg) -> (object, bool):
	arg.showStats()
	input("Press enter to exit...")
	return (arg, False)

def player_init_continue(arg) -> (object, bool):
	cprint("Good luck, fellow adverturer!", "green")
	time.sleep(1)
	return (arg, True)

def player_init_addPoints(player) -> (object, bool):
	utils.clear()
	player.showStats()
	print("You have: %d points left" % (player.points));
	count = getNumber("How many points do you want to add? (Enter 0 to exit)")
	if count > player.points or count < 0:
		cprint("You dont have enough points or you entered an invalid number!", "red")
		player_init_addPoints(player)
	m = Menu({
		"Strength": lambda arg: pi_add_stat((arg, count, "strength")),
		"Defense": lambda arg: pi_add_stat((arg, count, "defense")),
		"Agility": lambda arg: pi_add_stat((arg, count, "agility")),
		"Intelligence": lambda arg: pi_add_stat((arg, count, "intelligence")),
		"Charisma": lambda arg: pi_add_stat((player, count, "charisma")),
		"Luck": lambda arg: pi_add_stat((player, count, "luck")),
		"Cancel": lambda arg: (arg, True)
	}, titleColor="blue")
	m.title = "Add %d points to player" % (count);
	if count != 0:
		player = m.prompt(player)
	else:
		cprint("Exiting!", "yellow")
		time.sleep(1)
	return (player, False)

# add_points submenu

def pi_add_stat(tuple) -> (object, bool):
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
