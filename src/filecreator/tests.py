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
| Max Marshall    | 2023-05-31 | Created File
| Max Marshall    | 2023-06-01 | Added support for Python,Bash,Cpp Tests
| Max Marshall    | 2023-06-26 | Added outline for more tests
|
"""
import unittest
import os
import main


################################################################################
## TEST HELPERS ################################################################
def check_file(filename):
	return os.path.exists(filename)

def read_file(filename):
	f = open(filename,"r")
	text = f.read()
	f.close()
	return text

def pass_test(filename,text="",delete=True):
	if check_file(filename):
		file_text = read_file(filename)
		if file_text.find(text) != -1:
			if delete:
				os.remove(filename)
			return True
		if delete:
			os.remove(filename)
	return False


################################################################################
## TESTS #######################################################################
class TestGenericMethods(unittest.TestCase):
	def setUp(self):
		self.delete = delete_files
		self.cpp_error = "Error recreating the .cpp file"
		self.h_error = "Error recreating the .h file"


class TestPythonMethods(TestGenericMethods):
	def test_main(self):
		return
	
	def test_class(self):
		return
	
	def test_function(self):
		return


class TestBashMethods(TestGenericMethods):
	def test_main(self):
		filename = "test"
		string = ""
		error = "Failed to Reproduce Test Case -- Main"
		main.ProcessArgs("bash {}".format(filename).split(" "))
		self.assertTrue(pass_test("{}.sh".format(filename),string,self.delete),error)
	
	def test_setup(self):
		filename = "setup"
		string = ""
		main.ProcessArgs("bash {}".format(filename).split(" "))
		self.assertTrue(pass_test("{}.sh".format(filename),string,self.delete))
	
	def test_run(self):
		filename = "run"
		string = ""
		main.ProcessArgs("bash {}".format(filename).split(" "))
		self.assertTrue(pass_test("{}.sh".format(filename),string,self.delete))


class TestCppMethods(TestGenericMethods):
	def test_class(self):
		filename = "test"
		cpp_string = ""
		h_string = ""
		main.ProcessArgs("cpp class {}".format(filename).split(" "))
		self.assertTrue(pass_test("src/{}.cpp".format(filename),cpp_string,self.delete),self.cpp_error)
		self.assertTrue(pass_test("include/{}.h".format(filename),h_string,self.delete),self.h_error)
	

class TestCMethods(TestGenericMethods):
	def test_main(self):
		return
	
	def test_func(self):
		return
	

class TestLicenseMethods(TestGenericMethods):
	def test(self):
		return


class TestRepoMethods(TestGenericMethods):
	def test_python(self):
		return

	def test_cpp(self):
		return

	def test_c(self):
		return


################################################################################
## GLOBALS #####################################################################
test_loc = "{}/test_files/".format(os.path.dirname(__file__))
delete_files = True


if __name__ == '__main__':
    # Add arg to not delete files, if I feel like it
    os.chdir(test_loc)
    unittest.main()
