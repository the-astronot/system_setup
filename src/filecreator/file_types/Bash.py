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
| Max Marshall    | 2022-11-23 | Added Subclasses Setup and Python
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
		self.isFile = False
		self.header_type = ["bash", "default"]
		self.header_file = ["bash_header", "default_header_narrow"]
		self.body_type = ""
		self.body_file = ""
		self.ext = ".sh"
		self.variables["@mlc_start"] = "#EVERYLINE"
		self.variables["@mlc_end"] = ""
		self.subclasses = {
			"setup": Setup,
			"base": Base,
			"run": PythonRun
		}

	def setup(self):
		self.type = "base"
		self.name = "run"
		if len(self.args)>0:
			if self.args[0] in self.subclasses:
				self.type = self.args[0]
			else:
				self.name = self.args[0]
		if len(self.args)>1:
			self.name = self.args[1]
		actual_bash = self.subclasses[self.type]([self.name],self.variables)
		actual_bash.path = self.path
		actual_bash.isFile = True
		self.children.append(actual_bash)
		super().distr_setup()


class Base(Bash):
	def __init__(self, args, variables):
		super().__init__(args, variables)
		self.name = self.args[0]

	def setup(self):
		self.variables["@name"] = self.name



class Setup(Bash):
	def __init__(self, args, variables):
		super().__init__(args, variables)
		self.name = "setup"
		self.body_type = "bash"
		self.body_file = "setup_body"

	def setup(self):
		self.variables["@name"] = self.name


class PythonRun(Bash):
	def __init__(self, args, variables):
		super().__init__(args,variables)
		self.name = "run"
		self.body_type = ["bash"]
		self.body_file = ["python_body"]

	def setup(self):
		self.variables["@name"] = self.name
