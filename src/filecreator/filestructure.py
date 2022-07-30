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

from os import path, getcwd, makedirs
from datetime import datetime


variables = {} # Global Variable for Storing Replacement Data


def FileStructureFactory(args,variables):
	f_struct_name = args.pop(0)
	f_structs = {
		"repo": Repo,
		"python": Python,
		"cpp": Cpp,
		".gitignore": GitIgnore,
		"readme": ReadMe,
		"makefile": Makefile
	}
	return f_structs[f_struct_name](args, variables)


def RepoFactory(args, variables):
	"""
	It's expected that the first arg is a "type" in repos
	"""
	repos = {
		"cpp": Repo_Cpp,
		"python": Repo_Python
	}
	return repos[args[0]](args,variables)


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

################################################################################
## GENERIC
class FileStructure:
	def __init__(self, args, variables):
		self.args = args
		self.header = ""
		self.body = ""
		self.path = getcwd()
		self.variables = variables
		self.variables["@mlc_start"] = ""
		self.variables["@mlc_end"] = ""
		self.ext = ""
		self.isFile = False
		self.children = []
		self.header_file = "default_header"
		self.body_file = ""
		self.header_type = "default"
		self.body_type = "default"

	def distr_setup(self):
		for child in self.children:
			child.setup()

	def createFile(self):
		self.load_header()
		self.load_body()
		if self.isFile and not path.exists(path.join(self.path,path.join(self.name,self.ext))):
			with open(path.join(self.path,self.name+self.ext),"w+") as f:
				text = self.header + self.body
				text = self.repl_var(text)
				f.write(text)
		for child in self.children:
			child.createFile()
			
	def repl_var(self, text):
		prev_text = ""
		while text is not prev_text:
			prev_text = text
			for key in self.variables.keys():
				text = text.replace(key,self.variables[key])
		return text

	def load_header(self):
		header_file = path.join(self.header_type,self.header_file)
		if self.header_file != "":
			if (path.exists(path.join(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))),path.join("file_structures",header_file)))):
				self.header = load_struct(header_file)

	def load_body(self):
		body_file = path.join(self.body_type,self.body_file)
		if self.body_file != "":
			if (path.exists(path.join(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))),path.join("file_structures",body_file)))):
				self.body = load_struct(body_file)

## END GENERIC
################################################################################

################################################################################
## REPOS
class Repo(FileStructure):
	def __init__(self, args, variables):
		super().__init__(args,variables)

	def setup(self):
		self.type = self.args[0]
		self.name = self.args[1]
		self.isFile = False
		supMakeDirs(path.join(self.path,self.name))
		supMakeDirs(path.join(path.join(self.path,self.name),"bin"))
		supMakeDirs(path.join(path.join(self.path,self.name),"data"))
		supMakeDirs(path.join(path.join(self.path,self.name),"src"))
		self.children.append(RepoFactory(self.args,variables))
		self.children.append(FileStructureFactory(["readme",self.name],variables))
		self.children.append(GitIgnore(self.args,self.variables))
		for child in self.children:
			child.path = path.join(self.path,self.name)
		super().distr_setup()

class Repo_Python(Repo):
	def __init__(self,args,variables):
		super().__init__(args,variables)
	
	def setup(self):
		self.children.append(FileStructureFactory([".gitignore","python"],variables))
		self.children[0].path = self.path
		python_child = Python_Funct_File(["main"],self.variables)
		python_child.path = path.join(self.path,"src")
		self.children.append(python_child)
		super().distr_setup()

class Repo_Cpp(Repo):
	def __init__(self,args,variables):
		super().__init__(args,variables)
	
	def setup(self):
		self.children.append(Cpp([],self.variables))
		self.children.append(Makefile(self.args,self.variables))
		for child in self.children:
			child.path = self.path
		super().distr_setup()

## END REPOS
################################################################################

################################################################################
## PYTHON
class Python(FileStructure):
	# Generic Python FileStructure, subclasses into classes, functs, main
	def __init__(self,args,variables):
		super().__init__(args,variables)
		self.variables["@mlc_start"] = "\"\"\""
		self.variables["@mlc_end"] = "\"\"\""
		self.ext = ".py"
		self.body_type = "python"
		self.subclasses = {
			"class": Python_Class_File,
			"main": Python_Funct_File,
			"func": Python_Funct_File
		}

	def setup(self):
		self.type = "main"
		self.name = "main"
		if len(self.args)>0:
			self.type = self.args[0]
		if len(self.args)>1:
			self.name = self.args[1]
		self.children.append(self.subclasses[self.type]([self.name],self.variables))
		super().distr_setup()

class Python_Class_File(Python):
	def __init__(self,args,variables):
		super().__init__(args,variables)
		self.isFile = True
		self.body_file = "python_class_body"

	def setup(self):
		assert len(self.args)==1,"Python Class Name Required"
		self.name = self.args[0]
		self.variables["@name"] = self.name
		super().distr_setup()

class Python_Funct_File(Python):
	def __init__(self,args,variables):
		super().__init__(args,variables)
		self.isFile = True
		self.body_file = "python_funct_body"

	def setup(self):
		assert len(self.args)==1,"Python Class Name Required"
		self.name = self.args[0]
		self.variables["@name"] = self.name
		super().distr_setup()

## END PYTHON
################################################################################

################################################################################
## START CPP	
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

## END CPP
###############################################################################	

###############################################################################	
## GITIGNORE
class GitIgnore(FileStructure):
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
		self.isFile = True
		super().distr_setup()

## END GITIGNORE
###############################################################################	

###############################################################################	
## README
class ReadMe(FileStructure):
	"""
	args: [title]
	"""
	def __init__(self, args, variables):
		super().__init__(args,variables)
		self.bodies = {
			"cpp": "readme_cpp_body",
			"python": "readme_python_body"
		}

	def setup(self):
		self.name = "README"
		self.ext = ".md"
		if len(self.args) != 0:
			self.variables["@name"] = self.args[0]
		self.header_type = "readme"
		self.body_type = "readme"
		self.header_file = "readme_header"
		self.isFile = True
		super().distr_setup()

## END README
###############################################################################	

###############################################################################	
## MAKEFILE
class Makefile(FileStructure):
	"""
	args: [type, title]
	"""
	def __init__(self, args, variables):
		super().__init__(args,variables)
		self.body_files = {
			"cpp": "makefile_cpp_body"
		}

	def setup(self):
		self.isFile = True
		self.ext = ""
		self.name = "Makefile"
		self.body_type = "makefile"
		self.header_file = ""
		self.body_file = self.body_files[self.args[0]]
		if len(self.args)>1:
			self.variables["@name"] = self.args[1]
		super().distr_setup()

## END MAKEFILE
###############################################################################	
