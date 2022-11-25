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
| Max Marshall    | 2022-11-24 | Modified subclasses
|
|
"""
from filestructure import File

class Python(File):
	# Generic Python FileStructure, subclasses into classes, functs, main
	def __init__(self,args,variables):
		super().__init__(args,variables)
		self.variables["@mlc_start"] = "\"\"\""
		self.variables["@mlc_end"] = "\"\"\""
		self.ext = ".py"
		self.body_type = "python"
		self.header_type = ["python","default"]
		self.header_file = ["python_header","default_header"]
		self.subclasses = {
			"class": Python_Class_File,
			"main": Python_Funct_File,
			"func": Python_Funct_File,
			"funct": Python_Funct_File,
			"function": Python_Funct_File
		}
		self.isFile = False

	def setup(self):
		self.type = "main"
		self.name = "main"
		if len(self.args)>0:
			self.type = self.args[0]
		if len(self.args)>1:
			self.name = self.args[1]
		if self.type in self.subclasses:
			python_file = self.subclasses[self.type]([self.name],self.variables)
		python_file.isFile = True
		python_file.path = self.path
		self.children.append(python_file)
		super().distr_setup()

class Python_Class_File(Python):
	def __init__(self,args,variables):
		super().__init__(args,variables)
		self.body_file = "python_class_body"
		self.isFile = True

	def setup(self):
		assert len(self.args)==1,"Python Class Name Required"
		self.name = self.args[0]
		self.variables["@name"] = self.name
		super().distr_setup()

class Python_Funct_File(Python):
	def __init__(self,args,variables):
		super().__init__(args,variables)
		self.body_file = "python_funct_body"
		self.isFile = True

	def setup(self):
		assert len(self.args)==1,"Python Class Name Required"
		self.name = self.args[0]
		self.variables["@name"] = self.name
		super().distr_setup()
