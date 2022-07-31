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
| Max Marshall    | 2022-07-30 | Created File
|
|
|
"""
from filestructure import File

class Bash(File):
	"""
	args: [name]
	"""
	def __init__(self, args, variables):
		super().__init__(args, variables)

	def setup(self):
		self.name = self.args[0]
		self.header_file = ""
		self.body_type = "bash"
		self.body_file = "bash_body"
		self.ext = ".sh"
		super().distr_setup()
