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
	else:
		# Installs
		installs(command)
		# Pip installs
		pip_installs(command)
		# Bash aliases
		file_edits(join(folder,"alias"),".bash_aliases","alias {0}=\"{1}\"\n")
		# Bashrc
		file_edits(join(folder,"bash"),".bashrc","{0} {1}\n")
		# Macros
		file_edits(join(folder,"macro"),".inputrc","{0}: \"{1}\"\n")
		print("SETUP COMPLETED")


def file_edits(command,dest,line_layout):
	try:
		with open(command,"r") as f:
			dest = join(expanduser("~"),dest)
			text = f.read()
			text = text.strip("\n")
			lines = text.split(";\n")
			try:
				with open(dest,"r") as r:
					text = r.read()
					start = text.find("\n## THIS SECTION GOVERNED BY SYSTEM_SETUP ##")
					end = text.find("## END OF SYSTEM_SETUP ##")
					if start != -1 and end != -1:
						beg = text[:start]
						fin = text[end+26:]
						text = beg+fin
			except FileNotFoundError:
				vprint("No existing file {} found\nCreating File...".format(dest))
				text = ""
			with open(dest,"w+") as w:
				w.write(text)
				w.write("\n## THIS SECTION GOVERNED BY SYSTEM_SETUP ##\n\n")
				for line in lines:
					try:
						if line[0] == "#":
							comment_end = line.find("\n")+1
							w.write("{}".format(line[:comment_end]))
							line = line[comment_end:]
						data = []
						split = line.find(":")
						data.append(line[:split])
						data.append(line[split+1:])
						to_write = line_layout.replace("{0}",data[0]).replace("{1}",data[1][:-1])
						w.write(to_write)
					except IndexError:
						pass
				w.write("\n## END OF SYSTEM_SETUP ##\n")
				vprint("Wrote to {}".format(dest))
	except FileNotFoundError:
		vprint("File {} not found...\nSkipping...".format(command))


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
	try:
		with open(join(config_path,join(command,"install")),"r") as f:
			text = f.read()
			text = text.strip("\n")
			lines = text.split("\n")
			for line in lines:
				os.system("{0} {1}".format(installer,line))
	except FileNotFoundError:
		vprint("No install file found\nSkipping...")


def pip_installs(command):
	try:
		with open(join(config_path,join(command,"pip")),"r") as f:
			text = f.read()
			text = text.strip("\n")
			lines = text.split("\n")
			for line in lines:
				os.system("pip3 install {}".format(line))
	except FileNotFoundError:
		vprint("No pip install file found...\nSkipping...")


def vprint(string):
	if verbose_logging:
		print(string)


config_path = join(dirname(dirname(dirname(abspath(__file__)))),"config")
verbose_logging = True


if __name__ == '__main__':
	assert(len(sys.argv)==2)
	run_setup(sys.argv[1])
