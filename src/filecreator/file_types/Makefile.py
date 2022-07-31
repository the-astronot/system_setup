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
| Max Marshall    | 2022-07-30 | Created File, separated from file_structure
|
|
|
"""
from filestructure import File

class Makefile(File):
	"""
	args: [type, title]
	"""
	def __init__(self, args, variables):
		super().__init__(args,variables)
		self.body_files = {
			"cpp": "makefile_cpp_body"
		}

	def setup(self):
		self.ext = ""
		self.name = "Makefile"
		self.body_type = "makefile"
		self.header_file = ""
		self.body_file = self.body_files[self.args[0]]
		if len(self.args)>1:
			self.variables["@name"] = self.args[1]
		super().distr_setup()
