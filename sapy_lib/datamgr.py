#!/usr/bin/python3
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
import datetime
import copy,csv

from sapy_lib.lom import Lom
from sapy_lib.mom import Mom

_DEBUG_ = True


class DataMgr(object):
    if _DEBUG_:
        print ("__ Data mgr __ : init")

    def __init__(self, path2file):
        self.__lom_list = list()
        self.__last_lom_id = -1
        self.__path_data_file = path2file

        if not self.__path_data_file : 
            print ("file2path could not be empty")
            return

        if not os.path.isfile(self.__path_data_file) :
            print ("file2path file must exist")
            return

        datafile = open(os.path.abspath(self.__path_data_file), "r")
        for lom_dict in json.load(datafile):
            lom_tmp = Lom()
            lom_tmp.from_dict(lom_dict)
            self.__lom_list.append(lom_tmp)

        datafile.close()
        # sort by date
        self.__lom_list = sorted(self.__lom_list, key=lambda lom: lom.lom_id())
        # set the last lom id
        if self.__lom_list :
            self.__last_lom_id =  self.__lom_list[-1].lom_id()
 

    def from_csv(self, file_path, lom):
        if os.path.isfile(os.path.abspath(file_path)):
            datafile = open(os.path.abspath(file_path), "r")
            reader = csv.reader(datafile)
            for row in reader :
                mom = Mom()
                mom.time(
                        datetime.date(
                            int(row[0].split("/")[2]),
                            int(row[0].split("/")[1]),
                            int(row[0].split("/")[0])
                            )
                        )
                mom.cause(row[1])
                mom.price(float(row[2].replace(",","")))
                lom.insert(mom)

    def from_file(self, file_path = None):
        if os.path.isfile(os.path.abspath(file_path)):
            datafile = open(os.path.abspath(file_path), "r")
            self.__lom_list = [ Lom(tmp_lom) for tmp_lom in json.load(datafile) ]
            datafile.close()
       # sort by date
            self.__lom_list = sorted(self.__lom_list, key=lambda lom: lom.lom_id())
        # set the last lom id
            self.__last_lom_id =  self.__lom_list[-1].lom_id()
 

        elif _DEBUG_:
            print (" no file " + str(os.path.abspath(self.Datafile)))

        else:
            print ("no file %s available", self.Datafile)

    def to_file(self, file_path = None):
        rawdata = [ tmp_lom.to_dict() for tmp_lom in self.__lom_list ]

        if file_path is not None and (not isinstance(file_path, str)):
            print ("type error")
            return
        
        if file_path == None :
            datafile = open(os.path.abspath(self.__path_data_file), "w")
            # TODO: enable dump indention
            json.dump(rawdata, datafile)
            datafile.close()
            return

        if os.path.isfile(os.path.isfile(from_file)):
            datafile = open(os.path.abspath(from_file), "w")
            # TODO: enable dump indention
            json.dump(rawdata, datafile)
            datafile.close()

    def new_lom(self, name = None):
        if name is not None and (not isinstance(name, str)):
            print ("type error")
            return

        if name :
            tmp_lom = Lom(name)
        else :
            tmp_lom = Lom()
        
        self.__last_lom_id += 1
        tmp_lom.lom_id(self.__last_lom_id)
        self.__lom_list.append(tmp_lom)
        
        return tmp_lom

    def insert_lom(self, lom):
        if  (not isinstance(lom, Lom)):
            print ("type error")
            return

        self.__last_lom_id += 1
        lom.lom_id(self.__last_lom_id)
        self.__lom_list.append(lom)
        
        return self.__last_lom_id


    def remove_lom(self,lom):
        if (not isinstance(lom, Lom)):
            print ("type error")
            return

        self.Lom_list.remove(lom)
        # TODO:manage grabbage ?
        pass

    def add_mom(self, lom, mom):
        if (not isinstance(lom, Lom)):
            print ("type error")
            return
        
        if (not isinstance(mom, dict)):
            print ("type error")
            return
        tmp_mom = Mom()
        tmp_mom.from_dict(mom)
        [l for l in self.__lom_list if l.name() == lom.name()][0].insert(mom)
      
    def remove_mom(self, lom, mom):
        if (not isinstance(lom, Lom)):
            print ("type error")
            return
        
        if (not isinstance(mom, Mom)):
            print ("type error")
            return

        [l for l in self.__lom_list if l.name() == lom.name()][0].remove(mom)
      
    def get_loms(self):
        return self.__lom_list


    def get_graph_data(self, start_date, end_date):
        graph_data = list()
        for lom in self.__lom_list:
            if lom.is_visible():
                graph_data.append(lom.balance_per_day(start_date, end_date))

        return graph_data



