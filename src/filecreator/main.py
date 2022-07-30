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
| Max Marshall    | 2022-07-29 | Created File
|
|
|
"""

from filestructure import FileStructureFactory, variables, load_variables
from sys import argv


def ProcessArgs(args):
	load_variables()
	f_structs = FileStructureFactory(args,variables)
	f_structs.setup()
	f_structs.createFile()

if __name__ == '__main__':
	args = argv
	args.pop(0)
	ProcessArgs(args)
