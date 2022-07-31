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
| Max Marshall    | 2022-07-30 | Moved SubClasses into other files
|
|
"""
from os import path, getcwd
from utils import *


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


class File(FileStructure):
	def __init__(self, args, variables):
		super().__init__(args, variables)
		self.isFile = True
