"""
@author: jormungandr1105
@desc: This file creates boilerplate for other files
@started: 03/31/22
"""
import sys
import os
import datetime
from File import File


def create(args):
	ftype, fname = determine_filetype(args)
	ftype = os.path.join(filetype_path,ftype)
	configs = config_filler(fname)
	file_data = File(ftype,fname)
	file_data.read()
	if file_data.desc == "file":
		create_file(file_data,current_path,configs)
	elif file_data.desc == "folder":
		create_folder(file_data,current_path,configs)


def create_file(file_data, path, configs):
	with open(os.path.join(path,file_data.fname),"w+") as file:
		file_data.insert_wildcards(configs)
		file.write(file_data.body)


def create_folder(file_data, path, configs):
	file_data.insert_wildcards(configs)
	commands = file_data.body.split("\n")
	for command in commands:
		if command[:6] == "folder":
			try:
				os.mkdir(os.path.join(path,command[7:]))
			except FileExistsError:
				pass
		else:
			args = command[5:].split(" ")
			if args[0] != "\"\"":
				args[-1] = os.path.join(args[0],args[-1])
			args = args[1:]
			ftype, fname = determine_filetype(args)
			sub_file_data = File(ftype,fname)
			sub_file_data.read()
			sub_configs = config_filler(fname.split("/")[-1])
			create_file(sub_file_data, path, sub_configs)


def determine_filetype(args):
	fname = args[-1]
	filesource = filetype_path
	for x in range(len(args)-1):
		test_filesource = os.path.join(filesource,args[x])
		if os.path.exists(test_filesource):
			filesource = test_filesource
		else:
			filesource = os.path.join(filesource,"{}.txt".format(args[x]))
			break
	if os.path.isdir(filesource) and os.path.exists(os.path.join(filesource,"any.txt")):
		filesource = os.path.join(filesource,"any.txt")
	elif os.path.exists(os.path.join(filesource,"{}.txt".format(args[-1]))):
		filesource = os.path.join(filesource,"{}.txt".format(args[-1]))
	elif os.path.isdir(filesource) and os.path.exists(filesource+".txt"):
		filesource = filesource+".txt"
	elif os.path.isdir(os.path.join(filesource,args[-1])):
		print("Not Specific Enough, Try Again")
		exit(1)
	#print(filesource, fname)
	return filesource, fname


def config_filler(fname):
	with open(config_file,"r") as conf:
		config_text = conf.read()
		config_text = config_text.strip(";\n")
		config_array = config_text.split(";\n")
		configs = {}
		for item in config_array:
			parts = item.split(":")
			if len(parts) == 2:
				configs[parts[0]] = parts[1]
	configs["@fname"] = fname
	for key in all_configs.keys():
		if configs.get(key) is None or configs.get(key) == "":
			configs[key] = all_configs[key]
	return configs


def generate_defaults():
	global all_configs
	curr_time = datetime.datetime.now()
	try:
		all_configs["@author"] = os.getlogin()
	except FileNotFoundError:
		all_configs["@author"] = input("Enter User: ")
	all_configs["@date"] = "{0:02d}/{1:02d}/{2}".format(curr_time.month,curr_time.day,curr_time.year)



config_file = "creator.conf"
filetype_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),"file_structures")
current_path = os.getcwd()
config_file = os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),"config"),config_file)
all_configs = {}



if __name__ == '__main__':
	generate_defaults()
	create(sys.argv[1:])
