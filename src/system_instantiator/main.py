"""
@author: Max Marshall
@desc: The main system setup script
@created: 04/02/2022
"""
import os
from os.path import *
import sys
import distro


def run_setup(command):
	folder = join(config_path,command)
	if not exists(folder):
		print("Setup not found.\nPossible Setups Include:")
		for line in os.listdir(config_path):
			if isdir(join(config_path,line)):
				print("- {}".format(line))


def bashrc_edits(command):
	pass


def alias_edits(command):
	pass


def installs(command):
	installer = ""
	dist = distro.id()
	print("DETECTED DISTRIBUTION:",dist)
	if dist == "ubuntu" or dist == "debian" or dist == "raspbian":
		installer = "sudo apt-get install"
	elif dist == "arch":
		installer == "sudo pacman -Su"
	if installer == "":
		print("UNKNOWN DISTRIBUTION: ABORTING INSTALLATION")
		return
	with open(join(config_path,join(command,"install"),"r")) as f:
		text = f.read()
		text = text.strip("\n")
		lines = text.split("\n")
		for line in lines:
			os.system("{0} {1}".format(installer,line))


def pip_installs(command):
	with open(join(config_path,join(command,"pip"),"r")) as f:
		text = f.read()
		text = text.strip("\n")
		lines = text.split("\n")
		for line in lines:
			os.system("pip3 install {}".format(line))



config_path = join(dirname(dirname(dirname(abspath(__file__)))),"config")



if __name__ == '__main__':
	assert(len(sys.argv)==2)
	run_setup(sys.argv[1])
