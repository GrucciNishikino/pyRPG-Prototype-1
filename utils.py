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