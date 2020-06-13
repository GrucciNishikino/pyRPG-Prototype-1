import os
import subprocess
from termcolor import cprint

def clear():
	subprocess.call("clear" if os.name == "posix" else "cls", shell=True)

def getNumber(prompt = "Enter a number:"):
	try:
		return int(input(prompt + "\n> "))
	except:
		cprint("Invalid number!", "red")
		return getNumber(prompt)

# returns "n" if n is negative, and "+n" if n is positive
def prefixNumber(n):
	return ("+" if n > 0 else "") + str(n)