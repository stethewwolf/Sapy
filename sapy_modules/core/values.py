#
# Author : stefano prina 
#
# MIT License
# 
# Copyright (c) 2017 Stefano Prina <stethewwolf@gmail.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without sestriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
#     The above copyright notice and this permission notice shall be included in all
#     copies or substantial portions of the Software.
# 
#     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#     IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#     FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#     AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#     LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#     OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#     SOFTWARE.

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
