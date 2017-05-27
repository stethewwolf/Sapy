#!/usr/bin/python
#
#   File : data_mgr.py
#   Author : stefano prina
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

import json
import os

from lom import Lom

_DEBUG_ = True


class DataMgr(object):
    if _DEBUG_:
        print ("__ Data mgr __ : init")

    def __init__(self, datafile):
        self.Lom_list = list()
        self.Datafile = datafile

    def new_lom(self, name):
        tmp = Lom()
        tmp.name = name
        self.Lom_list.append(tmp)

    def remove(self):
        # TODO : write function
        pass

    def from_json(self, raw):
        for item in raw:
            tmp = Lom()
            tmp.from_json(item)
            self.Lom_list.append(tmp)
        if _DEBUG_:
            print (self.Lom_list)

    def to_json(self):
        tmp = []
        for lom in self.Lom_list:
            tmp.append(lom.to_json())
        return tmp

    def list_lom(self):
        return [l.name for l in self.Lom_list]

    def list_moms(self, lom):
        return [l for l in self.Lom_list if l.Name == lom][0].movements
        # return  self.Lom_list[lom].movements

    def load(self):
        if _DEBUG_:
            print ("__ Data Mgr __: load_saved_data : \n" + str(os.path.abspath(self.Datafile)))

        if os.path.isfile(os.path.abspath(self.Datafile)):
            datafile = open(os.path.abspath(self.Datafile), "r")
            rawdata = json.load(datafile)
            datafile.close()
            for tmp_data in rawdata:
                tmp_lom = Lom()
                tmp_lom.from_json(tmp_data)
                self.Lom_list.append(tmp_lom)

        elif _DEBUG_:
            print (" no file " + str(os.path.abspath(self.Datafile)))

        else:
            print ("no file %s available", self.Datafile)

    def dump(self):
        rawdata = []
        for tmp_lom in self.Lom_list:
            rawdata.append(tmp_lom.to_json())

        if os.path.isfile(os.path.abspath(self.Datafile)):
            datafile = open(os.path.abspath(self.Datafile), "w")
            json.dump(rawdata, datafile)
            datafile.close()
        pass
