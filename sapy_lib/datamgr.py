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

import copy, datetime
from sapy_lib.lom import Lom
from sapy_lib.mom import Mom
from sapy_lib.json_handler import JsonHandler
from sapy_lib.csv_handler import CsvHandler


class DataMgr(object):
    def __init__(self, path2file):
        self.__data_handler = JsonHandler()
        self.__data_handler.set_url(path2file)

        # update last_lom_id
        loms_list = self.__data_handler.get_loms_list()
        self.__last_lom_id = 0
        for lom in loms_list:
            if lom['lom_id'] > self.__last_lom_id:
                self.__last_lom_id = lom['lom_id']

    def new_lom(self, name = None):
        # chek name type
        if name is not None and (not isinstance(name, str)):
            return

        if name :
            lom = Lom(name)
        else :
            lom = Lom()
        
        self.__last_lom_id = self.__last_lom_id + 1
        lom.lom_id(self.__last_lom_id)
        self.__data_handler.new_lom(lom.to_dict())

        return lom

    def insert_lom(self, lom):
        # check data type
        if  (not isinstance(lom, Lom)):
            return -1

        self.__last_lom_id = self.__last_lom_id + 1
        lom.lom_id(self.__last_lom_id)
        self.__data_handler.new_lom(lom.to_dict())

        return self.__last_lom_id

    def remove_lom(self,lom):
        # check data type
        if (not isinstance(lom, Lom)):
            return
        
        self.__data_handler.remove_lom(lom.lom_id())

    def add_mom(self, lom, mom):
        # check data type
        if (not isinstance(lom, Lom)):
            return
        
        # check data type
        if (not isinstance(mom, dict)):
            return

        self.__data_handler.new_mom(lom.lom_id(), mom)
      
    def remove_mom(self, lom, mom):
        # check data type
        if (not isinstance(lom, Lom)):
            return
        
        # check data type
        if (not isinstance(mom, Mom)):
            return

        self.__data_handler.remove_mom(lom.lom_id(), mom.mom_id()) 
      
    def get_simple_loms(self):
        data = list()
        for dict_lom in self.__data_handler.get_loms_list():
            lom = Lom()
            lom.from_dict(dict_lom)
            data.append(lom)
        return data

    def get_lom(self, lom_id, start_date, end_date):
        lom_dict = self.__data_handler.get_lom(lom_id, start_date, end_date) 
        if lom_dict is None:
            return None
        lom = Lom()
        lom.from_dict(lom_dict)
        return lom

    def get_graph_data(self, start_date, end_date):
        #print("running graph data")
        graph_data = list()
        data = list()

        for dict_lom in self.__data_handler.get_loms_list():
            lom = Lom()
            lom.from_dict(self.__data_handler.get_full_lom(dict_lom['lom_id']))
            data.append(lom)

        for lom in data:
            if lom.is_visible():
                graph_data.append(lom.balance_per_day(start_date, end_date))

        #print(graph_data)
        return graph_data

    def from_csv(self, file_path, lom):
        csv_handler = CsvHandler()
        csv_handler.set_url(file_path)

        for mom_dict in csv_handler.get_moms(
            lom.lom_id(),
            datetime.date.min,
            datetime.date.max
            ):
            mom = Mom()
            mom.from_dict(mom_dict)
            lom.insert(mom)
            self.add_mom(lom, mom.to_dict())
    
    def update_lom(self, lom):
        self.__data_handler.update_lom(lom.to_dict())