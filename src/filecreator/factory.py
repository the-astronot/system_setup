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
from utils import *
# Import Modules
from file_types.Cpp import *
from file_types.Repo import *
from file_types.Python import *
from file_types.Makefile import *
from file_types.Readme import *
from file_types.Gitignore import *
from file_types.Bash import *
from file_types.Copy import *


def FileStructureFactory(args,variables):
	f_struct_name = args.pop(0)
	f_structs = {
		"repo": Repo,
		"python": Python,
		"cpp": Cpp,
		".gitignore": GitIgnore,
		"readme": ReadMe,
		"makefile": Makefile,
		"bash": Bash,
		"copy": Copy
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

