"""
Copyright (C) 2022 Max Marshall   

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see https://www.gnu.org/licenses/.

________________
|_File_History_|________________________________________________________________
|_Programmer______|_Date_______|_Comments_______________________________________
| Max Marshall    | 2022-07-30 | Created File, separated from filestructure
| Max Marshall    | 2022-11-23 | Added load_license(), apply_changes(), etc()
| Max Marshall    | 2022-11-25 | Added settings checker
| Max Marshall    | 2023-06-01 | Added support for comments in fc files
|
"""
import os
from os import makedirs, path
from datetime import datetime


#variables = {} # Global Variable for Storing Replacement Data
changes = {"true":True,"false":False,"v":"verbose","":True}


def apply_changes(args):
	variables ={}
	remove = []
	for arg in args:
		if arg[:2] == "--":
			if arg.find("=") != -1:
				split = arg.find("=")
				key = arg[2:split]
				value = arg[split+1:]
			else:
				key = arg[2:]
				value = ""
			key = convert_change(key)
			if key == "author":
				value = str.ljust(value,15)
			else:
				value = convert_change(value)
			variables["@{}".format(key)] = value
			remove.append(arg)
	for arg in remove:
		args.remove(arg)
	return args, variables


def convert_change(value):
	if value in changes:
		return changes[value]
	elif value.lower() in changes:
		return changes[value.lower()]
	elif value.isnumeric():
		return int(value)
	return value


def load_variables(variables):
	# cmdline args preferred over repo settings preferred over user settings
	settings_file = find_settings(variables)
	creator_file = path.join(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))),path.join("config","creator.conf"))
	if settings_file is not None:
		#print(settings_file)
		variables = sub_load_variables(variables,settings_file)
	variables = sub_load_variables(variables,creator_file)
	date = datetime.now()
	variables["@year"] = str(date.year)
	variables["@date"] = str(date.date())
	if not "@verbose" in variables:
		variables["@verbose"] = False
	load_license(variables)
	return variables


def sub_load_variables(variables,file):
	if path.exists(file):
		with open(file, "r") as f:
			text = f.read()
			while (text.find("#") > -1):
				first = text.find("#")
				last = text.find("\n",first)
				text = text[:first] + text[last+1:]
			var_data = text.strip(";\n").strip("\n").split(";\n")
			for var in var_data:
				split_loc = var.find(":")
				if not var[:split_loc] in variables:
					variables[var[:split_loc]] = var[split_loc+1:]
					if (var[:split_loc] == "@author"):
						variables[var[:split_loc]] = str.ljust(var[split_loc+1:],15)
	return variables


def load_struct(filename):
	struct_loc = path.join(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))),path.join("file_structures",filename))
	text = ""
	with open(struct_loc,"r") as f:
		text = f.read()
	return text


def load_license(variables):
	license_loc = path.join(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))),path.join("file_structures","licenses"))
	if variables["@license"] != "":
		license = variables["@license"]
		if path.exists(path.join(license_loc,license)):
			header = path.join(path.join(license_loc,license),"header")
			full_license = path.join(path.join(license_loc,license),"license")
			with open(header,"r") as f:
				variables["@lic_header"] = f.read()
			with open(full_license,"r") as g:
				variables["@lic_full"] = g.read()
			loaded = variables["@license"]
			if variables["@verbose"]:
				print("loaded {} license".format(loaded))


def supMakeDirs(folder):
	try:
		makedirs(folder)
	except FileExistsError:
		pass


def find_settings(variables):
	loc = os.getcwd()
	while loc != "/":
		if "@verbose" in variables and variables["@verbose"]:
			print(loc)
		if path.exists(path.join(loc,".fcsettings")):
			return path.join(loc,".fcsettings")
		loc = path.dirname(loc)
	return None


if __name__ == '__main__':
	pass
