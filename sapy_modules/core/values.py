# Sapy
# Copyright (C) 2018 stefano prina <stefano-prina@outlook.it> <stethewwolf@gmail.com>
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

import configparser,os
import sapy_modules.core.constants as SapyConstants
import sapy_modules.sapy.lom as loms
from datetime import datetime

__store = {}

def init():
    global __store
    __store['end_date'] = datetime.today().date()
    __store['start_date'] = datetime.today().date()
    __store['date'] = datetime.today().date()
    __store['value'] = 0
    __store['frequency'] = SapyConstants.FREQUENCY.NONE
    __store['lom'] = ""
    #__store['lom'] = loms.get_loms()[0]
    __store['name'] = 'new name'

    # db values
    __store['db.create.objectives']="""CREATE TABLE "objectives" ( "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "description" TEXT, "duedate"	TEXT )"""
    __store['db.create.loms']= """   CREATE TABLE "loms" (
	                                    "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	                                    "name"	TEXT NOT NULL UNIQUE
                                    ) """

    __store['db.create.moms']="""   CREATE TABLE "moms" (
	                                    "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	                                    "value"	REAL NOT NULL,
	                                    "cause"	TEXT,
	                                    "date"	TEXT NOT NULL
                                    ) """ 
    __store['db.create.tags']=""" CREATE TABLE "tags" (
	                                "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	                                "name"	TEXT
                                )"""
    __store['db.create.tag_in_mom']=""" CREATE TABLE "tag_in_mom" (
	                                    "mom_id"	INTEGER NOT NULL,
	                                    "tag_id"	INTEGER NOT NULL,
	                                    PRIMARY KEY("mom_id","tag_id")
                                    )"""
    __store['db.create.mom_in_lom']="""   CREATE TABLE "mom_in_lom" (
	                                    "mom_id"	INTEGER NOT NULL,
	                                    "lom_id"	INTEGER NOT NULL,
	                                    PRIMARY KEY("lom_id","mom_id")
                                    ) """
    __store['db.populate.lom']=""" INSERT INTO "loms" ("id","name") VALUES (1,'real'),(2,'expected'); """
    

def get_value( key ):
    global __store
    return __store[key]

def set_value( key, value ):
    global __store
    __store[ key ] = value
