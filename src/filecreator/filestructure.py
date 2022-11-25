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
| Max Marshall    | 2022-11-23 | Modified to allow multiple body/headers
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
		if self.isFile and not path.exists(path.join(self.path,self.name+self.ext)):
			if self.variables["@verbose"]:
				print(path.join(self.path,self.name+self.ext))
			with open(path.join(self.path,self.name+self.ext),"w+") as f:
				text = self.header + self.body
				if self.replace:
					text = self.repl_var(text)
				f.write(text)
		else:
			if self.isFile:
				if self.variables["@verbose"]:
					print("{} already exists".format(path.join(self.path,self.name+self.ext)))
		for child in self.children:
			child.createFile()
			
	def repl_var(self, text):
		prev_text = ""
		while text is not prev_text:
			prev_text = text
			for key in self.variables.keys():
				if key.find("mlc") != -1:
					continue
				if type(self.variables[key]) != str:
					continue
				text = text.replace(key,self.variables[key])
		text = self.repl_comments(text)
		return text

	def repl_comments(self,text):
		if "@mlc_start" in self.variables:
			if self.variables["@mlc_start"] == "#EVERYLINE":
				for _ in range(text.count("@mlc_start")):
					start_idx = text.find("@mlc_start")
					end_idx = text.find("@mlc_end")+8
					repl_text = text[start_idx:end_idx]
					repl_text = repl_text.replace("@mlc_start\n","#").replace("@mlc_end","\n")
					repl_text = repl_text.replace("\n","\n#")
					repl_text = repl_text.replace("#\n","")
					text = text[:start_idx] + repl_text[:-1] + text[end_idx:]
			else:
				text = text.replace("@mlc_start",self.variables["@mlc_start"])
				text = text.replace("@mlc_end",self.variables["@mlc_end"])
		return text

	def load_header(self):
		if self.header_file != "":
			self.header = ""
			if type(self.header_file) == str:
				header_file = path.join(self.header_type,self.header_file)
				if (path.exists(path.join(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))),path.join("file_structures",header_file)))):
					self.header += load_struct(header_file)
			else:
				assert len(self.header_type) == len(self.header_file), "HEADER_TYPE and HEADER_FILE LENGTHS DO NOT MATCH"
				for i in range(len(self.header_file)):
					header_file = path.join(self.header_type[i],self.header_file[i])
					if (path.exists(path.join(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))),path.join("file_structures",header_file)))):
						self.header += load_struct(header_file)

	def load_body(self):
		if self.body_file != "":
			self.body = ""
			if type(self.body_file) == str:
				body_file = path.join(self.body_type,self.body_file)
				if (path.exists(path.join(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))),path.join("file_structures",body_file)))):
					self.body = load_struct(body_file)
			else:
				assert len(self.body_type) == len(self.body_file), "BODY_TYPE and BODY_FILE LENGTHS DO NOT MATCH"
				for i in range(len(self.body_file)):
					body_file = path.join(self.body_type[i],self.body_file[i])
					if (path.exists(path.join(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))),path.join("file_structures",body_file)))):
						self.body += load_struct(body_file)


class File(FileStructure):
	def __init__(self, args, variables):
		super().__init__(args, variables)
		self.isFile = True
		self.name = "file"
		if len(self.args)>0:
			self.name = self.args[0]
		self.ext = ""
		self.header = ""
		self.body = ""
		self.header_file = ""
		self.body_file = ""
		self.replace = True

	def setup(self):
		pass

