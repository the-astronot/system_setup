"""
	Copyright (C) 2022  Max Marshall   

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
| Max Marshall    | 2022-11-25 | Created File
|
|
|
"""
from filestructure import File

class Settings(File):
	def __init__(self, args, variables):
		super().__init__(args,variables)
		self.name = ".fcsettings"
		self.ext = ""
		self.replace = False
		self.temp_vars = ["@author","@date","@email","@mlc_start","@mlc_end","@name"]

	def setup(self):
		self.body = ""
		for variable in self.variables:
			if (str(self.variables[variable]).count("\n") < 1):
				if variable not in self.temp_vars:
					line = "{}:{};\n".format(variable,self.variables[variable])
					self.body += line


if __name__ == '__main__':
	test = Settings()
