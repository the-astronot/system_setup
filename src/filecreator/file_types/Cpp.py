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
| Max Marshall    | 2022-07-30 | Created file, separated from file_structure
|
|
|
"""
from os import path
from filestructure import FileStructure
from utils import *


class Cpp(FileStructure):
	def __init__(self, args, variables):
		super().__init__(args, variables)
		self.variables["@mlc_start"] = "/*"
		self.variables["@mlc_end"] = "*/"
		self.body_type = "cpp"
		self.subfiles = {
			"": Cpp_Main_File,
			"class": Cpp_Class_File
		}
		self.subheaders = {
			"": Cpp_Main_Header,
			"class": Cpp_Class_Header
		}
		
	def setup(self):
		if path.basename(self.path) == "src" or path.basename(self.path) == "includes":
			supMakeDirs(path.join(self.path,path.join("..","src")))
			supMakeDirs(path.join(self.path,path.join("..","include")))
			file_path = path.join(self.path,path.join("..","src"))
			header_path = path.join(self.path,path.join("..","include"))
		else:
			supMakeDirs(path.join(self.path,"src"))
			supMakeDirs(path.join(self.path,"include"))
			file_path = path.join(self.path,"src")
			header_path = path.join(self.path,"include")
		if len(self.args) == 0:
			self.args.append("")
		self.type = self.args.pop(0)
		file = self.subfiles[self.type](self.args,self.variables)
		file.path = file_path
		header = self.subheaders[self.type](self.args,self.variables)
		header.path = header_path
		self.children.append(file)
		self.children.append(header)
		super().distr_setup()

class Cpp_Generic_File(Cpp):
	# Template
	def __init__(self,args,variables):
		super().__init__(args,variables)
		self.isFile = True
		self.ext = ".cpp"
	
	def setup(self):
		pass

class Cpp_Generic_Header(Cpp):
	#Template
	def __init__(self,args,variables):
		super().__init__(args,variables)
		self.isFile = True
		self.ext = ".h"

	def setup(self):
		pass

class Cpp_Class_File(Cpp_Generic_File):
	def __init__(self,args,variables):
		super().__init__(args,variables)
		self.body_file = "cpp_class_file"
		self.name = self.args[0]
		self.variables["@name"] = self.name

class Cpp_Class_Header(Cpp_Generic_Header):
	def __init__(self,args,variables):
		super().__init__(args,variables)
		self.body_file = "cpp_class_header"
		self.name = self.args[0]
		self.variables["@name"] = self.name
		
class Cpp_Main_File(Cpp_Generic_File):
	def __init__(self,args,variables):
		super().__init__(args,variables)
		self.body_file = "cpp_main_file"
		self.name = "main"

class Cpp_Main_Header(Cpp_Generic_Header):
	def __init__(self,args,variables):
		super().__init__(args,variables)
		self.body_file = "cpp_main_header"
		self.name = "main"

class Cpp_Funct_File(Cpp_Generic_File):
	def __init__(self,args,variables):
		super().__init__(args,variables)
		self.body_file = "cpp_funct_file"
		self.name = self.args[0]
		self.variables["@name"] = self.name

class Cpp_Funct_Header(Cpp_Generic_Header):
	def __init__(self,args,variables):
		super().__init__(args,variables)
		self.body_file = "cpp_funct_header"
		self.name = self.args[0]
		self.variables["@name"] = self.name
