#!/bin/bash
ON_PATH=$(which system_setup)

if [[ -z "$ON_PATH" ]]; then
	PWD= pwd
	echo "export PATH=$PWD/bin:\$PATH" >> ~/.bashrc
fi