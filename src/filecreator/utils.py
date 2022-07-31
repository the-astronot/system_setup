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
|
|
|
"""
from os import makedirs, path
from datetime import datetime


variables = {} # Global Variable for Storing Replacement Data


def load_variables():
	global variables
	file = path.join(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))),path.join("config","creator.conf"))
	with open(file, "r") as f:
		text = f.read()
		var_data = text.strip(";\n").strip("\n").split(";\n")
		for var in var_data:
			split_loc = var.find(":")
			variables[var[:split_loc]] = var[split_loc+1:]
			if (var[:split_loc] == "@author"):
				variables[var[:split_loc]] = str.ljust(var[split_loc+1:],15)
	date = datetime.now()
	variables["@year"] = str(date.year)
	variables["@date"] = str(date.date())


def load_struct(filename):
	struct_loc = path.join(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))),path.join("file_structures",filename))
	text = ""
	with open(struct_loc,"r") as f:
		text = f.read()
	return text


def supMakeDirs(folder):
	try:
		makedirs(folder)
	except FileExistsError:
		pass


if __name__ == '__main__':
	pass
