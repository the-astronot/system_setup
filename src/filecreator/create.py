"""
@author: jormungandr1105
@desc: This file creates 
@started: 03/31/22
"""
import sys
import os


def create(args):
	ftype, fname = determine_filetype(args)
	ftype = os.path.join(filetype_path,ftype)
	print(ftype)
	#f = open()

def determine_filetype(args):
	return args[0], args[1]


filetype_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),"file_structures")

if __name__ == '__main__':
	create(sys.argv[1:])