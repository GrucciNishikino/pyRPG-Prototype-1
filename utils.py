import os
import subprocess
from termcolor import cprint

import rooms

# Is there any other way to do this?
def clear():
	subprocess.call("clear" if os.name == "posix" else "cls", shell=True)
	pass

# Reads a number
def getNumber(prompt = "Enter a number:") -> int:
	try:
		return int(input(prompt + "\n> "))
	except:
		cprint("Invalid number!", "red")
		return getNumber(prompt)

# Returns "n" if n is negative, and "+n" if n is positive
def prefixNumber(n) -> str:
	return ("+" if n > 0 else "") + str(n)

# Combines dictionaries
def combine(d1, d2) -> dict:
	d1.update(d2)
	return d1

# getExitMenu option lambdas

def exit_up(arg) -> (object, bool):
	p = arg
	p.coords = (p.coords[0], p.coords[1] - 1)
	return (p, True)

def exit_down(arg) -> (object, bool):
	p = arg
	p.coords = (p.coords[0], p.coords[1] + 1)
	return (p, True)

def exit_left(arg) -> (object, bool):
	p = arg
	p.coords = (p.coords[0] - 1, p.coords[1])
	return (p, True)

def exit_right(arg) -> (object, bool):
	p = arg
	p.coords = (p.coords[0] + 1, p.coords[1])
	return (p, True)

# Gets an options dictionary (see menu.py) of valid exits for rooms
def getExitOptions(p, r, mapSize: (int, int)) -> dict:
	# Could have put this on one line but this looks waaay cleaner
	output = { "Cancel": lambda arg: (arg, True) }
	if r.exits[0] and p.coords[1] > 0:
		output = combine(output, { "Up": lambda arg: exit_up(arg) })
	if r.exits[1] and p.coords[1] < mapSize[1] - 1:
		output = combine(output, { "Down": lambda arg: exit_down(arg) })
	if r.exits[2] and p.coords[0] > 0:
		output = combine(output, { "Left": lambda arg: exit_left(arg) })
	if r.exits[3] and p.coords[0] < mapSize[0] - 1:
		output = combine(output, { "Right": lambda arg: exit_right(arg) })
	return output