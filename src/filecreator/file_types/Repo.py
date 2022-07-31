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
import factory
from filestructure import FileStructure
from file_types.Python import Python_Funct_File
from file_types.Makefile import *
from file_types.Cpp import *
from file_types.Gitignore import *
from utils import *


class Repo(FileStructure): # Generic
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
		self.children.append(factory.RepoFactory(self.args,variables))
		self.children.append(factory.FileStructureFactory(["readme",self.name],variables))
		self.children.append(GitIgnore(self.args,self.variables))
		for child in self.children:
			child.path = path.join(self.path,self.name)
		super().distr_setup()


class Repo_Python(Repo): # Python
	def __init__(self,args,variables):
		super().__init__(args,variables)
	
	def setup(self):
		self.children.append(factory.FileStructureFactory([".gitignore","python"],self.variables))
		self.children[0].path = self.path
		python_child = Python_Funct_File(["main"],self.variables)
		python_child.path = path.join(self.path,"src")
		self.children.append(python_child)
		super().distr_setup()


class Repo_Cpp(Repo): # Cpp
	def __init__(self,args,variables):
		super().__init__(args,variables)
	
	def setup(self):
		self.children.append(Cpp([],self.variables))
		self.children.append(Makefile(self.args,self.variables))
		for child in self.children:
			child.path = self.path
		super().distr_setup()
