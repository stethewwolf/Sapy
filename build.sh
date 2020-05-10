#!/bin/sh
# Sapy
# Copyright (C) 2018 stefano prina <stethewwolf@null.net>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# This script adds a menu item, icons for the current
# user. If possible, it will use the xdg-utils - or fall back to just creating
# and copying a desktop file to the user's dir.
# If called with the "-u" option, it will undo the changes.

## CONFIGURATION
CC=pyinstaller
CC_OPT=-F
TARGET=sapy
VERSION=`grep -rn "VERSION"  sapy_modules/core/constants.py  | head -n 1 | cut -d "=" -f 2 | tr -d \' | tr -d ' ' | tr -d '\"'`

## FUNCTIONS
my_clean () {
	rm -rvf ./build
}

dist_clean ()  {
	my_clean
	rm -rvf ./dist
	rm -rvf ./env
}

my_build () {
	my_makenv
	$CC $CC_OPT $TARGET
}

my_install () {
	my_build
	install -v ./dist/sapy $1
	deactivate
}

print_usage () {
	echo "Usage :"
	echo "$0 clean"
	echo "$0 distclean"
	echo "$0 build"
	echo "$0 install target_path"
	echo "$0 makenv"
	echo "$0 help"
}

my_package () {
	my_build
	tar -cf ./dist/sapy_$VERSION.tar -C ./dist/sapy
	tar -f ./dist/sapy_$VERSION.tar -r README.md
	tar -f ./dist/sapy_$VERSION.tar -r LICENSE
	gzip ./dist/sapy_$VERSION.tar
	deactivate
}

my_makenv() {
	if [ ! -f env/bin/activate ]; then
		virtualenv -p python3 env
		source env/bin/activate
		pip install -r requirements.txt
	else
		source env/bin/activate
	fi
}

#==========================================#

case "$1" in
	"clean" ) my_clean ;;
	"distclean" ) dist_clean ;;
	"build" ) my_build ;;
	"install" ) my_install $2 ;;
	"package" ) my_package ;;
	"makenv" ) my_makenv ;;
	* ) print_usage ;;
esac