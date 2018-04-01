#!/usr/bin/python3
#
#   File : json_handler
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

import csv, pathlib, datetime

class CsvHandler(object):
    def __init__(self):
        self.__url = ''
        self.__delimiter = ','
        self.__types = ["mom","lom"]
        self.__type = "mom"
        self.__lom_dict = {
            'name' : 'lom',
            'movements' : [],
            'lom_id' : -1,
            'last_mom_id' : 0,
            'visible' : False
        }
        self.__mom_dict = {
            'price': 0, 
            'cause': 'not specified', 
            'year': 2017, 
            'month': 12, 
            'day': 26, 
        }
    
    def set_type(self, data_type):
        if data_type not in self.__types:
            return
        
        self.__type = data_type

    def set_delimiter(self, delimiter):
        self.__delimiter = delimiter
        
    def set_url(self, url):
        if url is not pathlib.Path:
            url = pathlib.Path(url)

        # check the file exists, if not create it
        if not url.is_file():
            with open(url, 'w') as data_file:
                if self.__type == "mom":
                    writer = csv.DictWriter(data_file, fieldnames=self.__mom_dict.keys())
                    writer.writeheader()
                elif self.__type == "lom":
                    writer = csv.DictWriter(data_file, fieldnames=self.__lom_dict.keys())
                    writer.writeheader()
            data_file.close()
            
        # now save url
        self.__url = url
   
    def get_loms_list(self):
        self.__type == 'lom'
        loms_list = []
        with open(self.__url, 'r') as data_file:
            data = csv.DictReader(data_file, fieldnames=self.__lom_dict.keys())
        
        for lom in data:
            loms_list.append(
                {
                    'name' : lom['name'],
                    'lom_id' : lom['lom_id']
                    }
                )

        data_file.close()
        return loms_list

    def get_full_lom(self, lom_id):
        lom = {}
        with open(self.__url, 'r') as data_file:
            data = csv.DictReader(data_file, fieldnames=self.__lom_dict.keys())
        
        for lom in data:
            if lom['lom_id'] == lom_id :
                break

        data_file.close()
        return lom

    def get_lom(self, lom_id, start_date, end_date):
        return self.get_full_lom(lom_id)

    def get_moms(self, lom_id, start_date, end_date):
        self.__type == 'mom'
        mom_list = list()

        with open(self.__url, 'r') as data_file:
            #data = csv.DictReader(data_file, fieldnames=self.__mom_dict.keys())
            #data = csv.DictReader(data_file)
            data = csv.DictReader(data_file, fieldnames=[
                "cause",
                "price",
                "day",
                "month",
                "year"
            ])
            for mom in data:
                date = datetime.date(
                    int(mom['year']),
                    int(mom['month']),
                    int(mom['day'])
                    )

                if date >= start_date or date <= end_date:
                    mom_list.append({
                        'cause' : mom['cause'],
                        'price' : mom['price'],
                        'time' : {
                            'year' : mom['year'],
                            'month' : mom['month'],
                            'day' : mom['day']
                        }
                    })

        return mom_list

    def new_lom(self, lom_dict):
        pass
        
    def new_mom(self, lom_id, mom_dict):
        pass

    def remove_lom(self, lom_id):
        pass

    def remove_mom(self, lom_id, mom_id):
        pass

    def update_lom(self):
        pass

    def update_mom(self):
        pass        

