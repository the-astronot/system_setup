#!/bin/bash

# Global Variables
#declare -A CONFIGS
declare -A DIRS
NAMESIZE=16
LICENSENAME="none"
LICENSES=('gplv3' 'mit' 'none')
# End Global Variables

function initialize {
	# Set up folders to pull configs from
	REAL_FILE=$(realpath $0)
	DIRS[home]="${REAL_FILE%/new.sh}/../../file_structures"
	DIRS[bash]="${DIRS[home]}/bash"
	DIRS[c]="${DIRS[home]}/c"
	DIRS[cpp]="${DIRS[home]}/cpp"
	DIRS[generic]="${DIRS[home]}/generic"
	DIRS[gitignore]="${DIRS[home]}/gitignore"
	DIRS[license]="${DIRS[home]}/licenses"
	DIRS[makefile]="${DIRS[home]}/makefile"
	DIRS[python]="${DIRS[home]}/python"
	DIRS[readme]="${DIRS[home]}/readme"


	for folder in "${!DIRS[@]}"; do
		if [[ "$folder" != "home" ]]; then
			if [[ -e "${DIRS[$folder]}" && -d "${DIRS[$folder]}" ]]; then
				print "Folder: ${DIRS[$folder]#${DIRS[home]}/} loaded successfully"
			else
				echo "Folder: ${DIRS[$folder]#${DIRS[home]}/} not found" >&2
				E_FNF=1
			fi
		fi
	done
	if [[ $E_FNF ]]; then
		exit 1
	fi
	# Checking on user vars
	if [[ ! $author ]]; then
		export author="$USER"
	fi
	if [[ ! $author_email ]]; then
		export author_email=""
	fi
	export year=$(date +%Y)
	export todays_date=$(date +%Y-%m-%d)
	blank="                    "
	export auth_space="${blank:0:($NAMESIZE-${#author})}"
	USER_VALUES=("$author" "$author_email" "$year" "$todays_date")
	USER_KEYS=("author" "email" "year" "today")
}

function arg_parser() {
	for i in "$@"; do
		case $i in 
			python)
				export PYTHONFILE=1
				;;
			cpp)
				export CPPFILE=1
				;;
			bash)
				export BASHFILE=1
				;;
			c)
				export CFILE=1
				;;
			repo*)
				export REPOFILE=1
				;;
			readme)
				export READMEFILE=1
				;;
			make*)
				export MAKEFILE=1
				;;
			lic*)
				export LICENSEFILE=1
				;;
			class)
				export CLASSTYPE=1
				;;
			func*)
				export FUNCTIONTYPE=1
				;;
			--lic*)
				for (( j=1; j<${#i}; j++)); do
					case ${i:j:1} in
						=)
							set=0
							for k in "${LICENSES[@]}"; do
								str="${i:j+1}"
								if [[ "${k,,}" == "${str,,}" ]]; then
									export LICENSENAME=${str,,}
									set=1
								fi
							done
							if [[ "$set" -ne 1 ]]; then
								echo "License not recognized"
							fi
							;;
						*)
							;;
					esac
				done
				;;
			-*) # flags
				for (( j=1; j<${#i}; j++)); do
					case ${i:j:1} in
						v)
							VERBOSE=1
							;;
						o)
							OVERWRITE=1
							;;
						p)
							PLACE_FILES=1
							;;
						*)
							;;
					esac
				done
				;;
			*)
				export FILENAME="$i"
				;;
		esac
	done
}

function file_creator {
	if [[ -w . ]]; then
		if [[ $REPOFILE ]]; then # Make Repository
			FILENAME=${FILENAME%.*} # Remove extension
			if [[ $(dir_writer "$FILENAME" && cd "$FILENAME") ]]; then
				return
			fi
			cd "$FILENAME"
			dir_writer "bin"
			dir_writer "src"
			if [[ "$LICENSENAME" != "none" ]]; then
				file_writer "COPYING.txt" ""${DIRS[license]}"/$LICENSENAME/license"
			fi
			if [[ $PYTHONFILE ]]; then
				# Python Repo
				file_writer requirements.txt /dev/null
				(cd src && unset REPOFILE && file_creator)
			elif [[ $CPPFILE ]]; then
				dir_writer "include"
				(unset REPOFILE && unset MAKEFILE && PLACE_FILES=1 && FILENAME="main" && file_creator)
				(unset REPOFILE && MAKEFILE=1 && file_creator)
			elif [[ $CFILE ]]; then
				dir_writer "include"
				(unset REPOFILE && unset MAKEFILE && PLACE_FILES=1 && FILENAME="main" && file_creator)
				(unset REPOFILE && MAKEFILE=1 && file_creator)
			fi
			return
		elif [[ $MAKEFILE ]]; then
			if [[ $CPPFILE ]]; then
				file_writer "Makefile" "${DIRS[makefile]}/cpp"
			elif [[ $CFILE ]]; then
				file_writer "Makefile" "${DIRS[makefile]}/c"
			else
				file_writer "Makefile"
			fi
			return
		elif [[ $PYTHONFILE ]]; then
			FILENAME=${FILENAME%.*} # Remove extension
			if [[ $CLASSTYPE ]]; then
				file_writer "$FILENAME.py" "${DIRS[license]}/$LICENSENAME/#header" "${DIRS[python]}/header" "${DIRS[python]}/class"
			elif [[ $FUNCTIONTYPE ]]; then
				file_writer "$FILENAME.py" "${DIRS[license]}/$LICENSENAME/#header" "${DIRS[python]}/header" "${DIRS[python]}/func"
			else # main file
				file_writer "main.py" "${DIRS[license]}/$LICENSENAME/#header" "${DIRS[python]}/header" "${DIRS[python]}/func"
			fi
			return
		elif [[ $BASHFILE ]]; then
			FILENAME=${FILENAME%.*} # Remove extension
			if [[ "$FILENAME" == "setup" ]]; then
				file_writer "setup.sh" "${DIRS[bash]}/bash_header" "${DIRS[bash]}/setup_body"
			elif [[ "$FILENAME" == "pyrun" ]]; then
				file_writer "run.sh" "${DIRS[bash]}/bash_header" "${DIRS[bash]}/python_body"
			else
				file_writer "$FILENAME.sh" "${DIRS[bash]}/bash_header"
			fi
			return
		elif [[ $CFILE ]]; then
			FILENAME=${FILENAME%.*} # Remove extension
			export GUARD="${FILENAME^^}"
			file_writer "$FILENAME.c" "${DIRS[c]}/c_file"
			file_writer "$FILENAME.h" "${DIRS[license]}/$LICENSENAME/*header" "${DIRS[c]}/h_file"
			return
		elif [[ $CPPFILE ]]; then
			FILENAME=${FILENAME%.*} # Remove extension
			export GUARD="${FILENAME^^}"
			if [[ $CLASS ]]; then
				file_writer "$FILENAME.cpp" "${DIRS[cpp]}/class_file"
				file_writer "$FILENAME.h" "${DIRS[license]}/$LICENSENAME/*header" "${DIRS[cpp]}/class_h"
			elif [[ $FILENAME == "main" ]]; then
				file_writer "main.cpp" "${DIRS[cpp]}/main_file"
				file_writer "main.h" "${DIRS[license]}/$LICENSENAME/*header" "${DIRS[cpp]}/main_h"
			else
				file_writer "$FILENAME.cpp" "${DIRS[cpp]}/funct_file"
				file_writer "$FILENAME.h" "${DIRS[license]}/$LICENSENAME/*header" "${DIRS[cpp]}/funct_h"
			fi
			return
		elif [[ $READMEFILE ]]; then
			file_writer "README.md" "${DIRS[readme]}/header"
			return
		elif [[ $LICENSEFILE ]]; then # Make this better...
			FILENAME=${FILENAME%.*} # Remove extension
			if [[ "$FILENAME" == "none" ]]; then
				echo "" > /dev/null
			else
				file_writer "LICENSE" "${DIRS[license]}/$FILENAME/license"
			fi
			return
		else # Generic file
			if [[ $FILENAME ]]; then
				file_writer "$FILENAME"
			else 
				file_writer hello_world!.txt
			fi
			return
		fi
	else
		echo "Cannot create files, no writing permissions in folder $(pwd)" >&2
	fi
}

function source_config {
	# While true, back up dirs until find config file or reaches root
	CURR_DIR="$(pwd)"
	while [[ "$(pwd)" != "/" ]]; do
		#echo "$(pwd)"
		if [[ -e "$(pwd)/.fcsettings" ]]; then
			#echo "FOUND $(pwd)/.fcsettings"
			source "$(pwd)/.fcsettings"
			if [[ "$LICENSENAME" ]]; then
				export LICENSENAME=$LICENSENAME
			fi
			if [[ "$author_email" ]]; then
				export author_email=$author_email
			fi
			if [[ "$author" ]]; then
				export author=$author
			fi
			if [[ "$year" ]]; then
				export year=$year
			fi
			cd "$CURR_DIR"
			return
		fi
		cd ..
	done
	cd "$CURR_DIR"
	return
}

function file_writer {
	if [[ -w . ]]; then
		if [[ ! -e "$1" || "$OVERWRITE" ]]; then
			TEXT=""
			for (( i=2; i<$#+1; i++ )); do
				NEW_TEXT=$(envsubst < "${@:i:1}")
				TEXT="${TEXT}${NEW_TEXT}\n"
			done
			TEXT="${TEXT//'\REMOVE'/}"
			echo -e "$TEXT" > $1
		else
			echo "Cannot create file: $1, file already exists. Rerun with -o to overwrite" >&2
		fi
	else
		echo "Cannot create file: $1, no writing permissions." >&2
	fi
}

function dir_writer {
	if [[ ! -e "$1" ]]; then
		if [[ -w . ]]; then
			mkdir "$1"
		else
			echo "Cannot create folder: "$1", no writing permissions." >&2
		fi
	fi
}

function print {
	if [[ $VERBOSE ]]; then
		echo "$1"
	fi
}

## MAIN
source_config
arg_parser "$@"
initialize
file_creator
