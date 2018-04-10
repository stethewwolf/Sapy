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

import json, pathlib, datetime

class JsonHandler(object):
    def __init__(self):
        self.__url = ''
        pass
       
    def set_url(self, url):
        if url is not pathlib.Path:
            url = pathlib.Path(url)

        # check the file exists, if not create it
        if not url.is_file():
            with open(url, 'w') as data_file:
                data_file.write('[]')
            
        # now save url
        self.__url = url

    def set_type(self, data_type):
        pass

    def set_delimiter(self, delimiter):
        pass
 
    def get_loms_list(self):
        loms_list = []
        with open(self.__url, 'r') as data_file:
            data = json.load(data_file)
        data_file.close()
        
        for lom in data:
            loms_list.append(
                {
                    'name' : lom['name'],
                    'lom_id' : lom['lom_id'],
                    'visible' : lom['visible']
                    }
                )

        return loms_list

    def get_full_lom(self, lom_id):
        lom = None
        with open(self.__url, 'r') as data_file:
            data = json.load(data_file)
        
        for lom in data:
            if lom['lom_id'] == lom_id :
                break
        return lom

    def get_lom(self, lom_id, start_date, end_date):
        lom = self.get_full_lom(lom_id)
        if not lom:
            return None

        # check if date are correct type
        if not isinstance(start_date, datetime.date):
            return None
            
        if not isinstance(end_date, datetime.date):
            return None

        # now remove useless mom
        for mom in lom['movements']:
            date = datetime.date(
                mom['time']['year'],
                mom['time']['month'],
                mom['time']['day']
                )

            if date <= start_date.date() or date >= end_date.date():
                lom['movements'].remove(mom)
        return lom

    def get_moms(self, lom_id, start_date, end_date):
        lom = self.get_lom(lom_id, start_date, end_date)
        return lom['movements']

    def new_lom(self, lom_dict):
        with open(self.__url, 'r+') as data_file:
            data = json.load(data_file)

        data.append(lom_dict)

        with open(self.__url, 'w') as data_file:
            json.dump(data, data_file, indent=True)
    
    def new_mom(self, lom_id, mom_dict):
        lom = self.get_full_lom(lom_id)

        with open(self.__url, 'r+') as data_file:
            data = json.load(data_file)
        
        data.remove(lom)
        lom['movements'].append(mom_dict)
        data.append(lom)

        with open(self.__url, 'w') as data_file:
            data_file.truncate()
            json.dump(data, data_file, indent=True)
        
    def remove_lom(self, lom_id):
        lom = self.get_full_lom(lom_id)

        with open(self.__url, 'r+') as data_file:
            data = json.load(data_file)
        
        data.remove(lom)

        with open(self.__url, 'w') as data_file:
            json.dump(data, data_file, indent=True)
           
    def remove_mom(self, lom_id, mom_id):
        lom = self.get_full_lom(lom_id)
        self.remove_lom(lom_id)

        for mom in lom['movements']:
            if mom['mom_id'] == mom_id:
                lom['movements'].remove(mom)

        self.new_lom(lom)

    def update_lom(self, updated_lom):
        old_lom = self.get_full_lom(updated_lom['lom_id'])
        self.remove_lom(updated_lom['lom_id'])

        for field in old_lom:
            if field != "movements" and field != "lom_id":
                if old_lom[field] != updated_lom[field]:
                    old_lom[field] = updated_lom[field]
        self.new_lom(old_lom)

    def update_mom(self):
        pass        
