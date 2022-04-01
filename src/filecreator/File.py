"""
@author: jormungandr1105
@desc: A class to hold file data
@started: 03/31/22
"""

class File:

	def __init__(self,filename,fname):
		self.filesource = filename
		self.fname = fname
		self.desc = None
		self.body =  None

	def read(self):
		with open(self.filesource,"r") as f:
			text = f.read()
			beg_of_desc = text.find("=")+1
			end_of_desc = text.find("\n")+1
			self.desc = text[beg_of_desc:end_of_desc-1]
			self.body = text[end_of_desc:]

	def insert_wildcards(self,configs):
		for key in configs.keys():
			self.body = self.body.replace("{{"+"{}".format(key)+"}}",configs[key])

	def print(self): # Really just for testing purposes
		print(self.desc)
		print(self.body)
