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
from filestructure import File

class GitIgnore(File):
	"""
	args: [type]
	"""
	body_types = {
		"python": "gitignore_python_body",
		"cpp": "gitignore_cpp_body"
	}

	def __init__(self,args,variables):
		super().__init__(args,variables)

	def setup(self):
		self.name = ".gitignore"
		self.header_type = "gitignore"
		self.header_file = "gitignore_header"
		self.body_type = "gitignore"
		self.body_file = self.body_types[self.args[0]]
		super().distr_setup()
