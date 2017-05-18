#!/usr/bin/python
#
#   File : arg_parse.py
#
# MIT License
#
# Copyright (c) 2017 Stefano Prina <stethewwolf@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
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

from lom import *
from mom import *
import json,os

_DEBUG_ = True

class Data_mgr ( object ) :
    if _DEBUG_ :
        print ("__ Data mgr __ : init")
    def __init__ ( self  , datafile ) :
        self.loms = list()
        self.datafile = datafile

    def new_lom ( self, name  ) :
        tmp = lom()
        tmp.name = name
        self.loms.append(tmp)

    def remove ( self ) :
        pass

    def from_jsonable ( self, raw ):
        for item in raw :
            tmp = lom ();
            tmp.fromJsonable(item)
            self.loms.append(tmp)

        if _DEBUG_ :
            print ( self.loms)

    def to_jsonable ( self ):
        tmp = []
        for lom in self.loms :
            tmp.append(lom.toJsonable())

        return tmp

    def list_loms(self):
        return [ l.name for l in self.loms ]

    def list_moms(self,lom):
        return [l for l in self.loms if l.name==lom ][0].movements
        #return  self.loms[lom].movements

    def load(self):
        if _DEBUG_ :
            print ("__ Data Mgr __: load_saved_data : \n" + os.path.abspath( self.datafile ))

        if os.path.isfile( os.path.abspath( self.datafile ) ) :
            datafile = open( os.path.abspath( self.datafile ), "r")
            rawdata = json.load( datafile )
            datafile.close()
            for tmp_data in rawdata :
                tmp_lom = lom()
                tmp_lom.fromJsonable( tmp_data )
                self.loms.append(tmp_lom)

        elif _DEBUG_ :
            print (" no file " +  os.path.abspath( self.datafile ))

        else :
            print ( "no file %s available", self.datafile )


    def dump(self):
        rawdata = []
        for tmp_lom in self.loms :
            rawdata.append( tmp_lom.to_jsonable())

        if os.path.isfile( os.path.abspath( self.datafile ) ) :
            datafile = open( os.path.abspath( self.datafile ), "w")
            json.dump(rawdata,datafile)
            datafile.close()
        pass