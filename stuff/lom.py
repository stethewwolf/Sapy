#!/usr/bin/python3
#
#   File : lom.py
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

from mom import Mom
import datetime


class Lom(object):  # list of movements
    def __init__(
        self,
        name="list of movements",
    ):
        self.__name = name
        self.__movements = []  # array ordered by date
        self.__lom_id = -1
        self.__last_mom_id = -1
        self.__visible = False

    def name(self, name=None):
        if name is not None and (not isinstance(name, str)):
            print ("type error")
            pass

        if not name :
            self.__name = name

        return self.__name

        
        
    def visible(self, visible=True):
        if visible is not None and (not isinstance(visible, bool)):
            print ("type error")
            pass

        if visible == None :
            return self.__visible
        else :
            self.__visible = visible

        return self.__visible

    def is_visible(self):
        return self.__visisble

    def lom_id(self, lom_id=None):
        if lom_id is not None and (not isinstance(lom_id, int)):
            print ("type error")
            return -1
        if lom_id:
            self.__lom_id = lom_id
        return self.__lom_id

    def insert(self, m):
        if m is not None and (not isinstance(m, Mom)):
            print ("type error")
            return
        # manage ids
        self.__last_mom_id += 1
        m.mom_id(self.__last_mom_id)
        # insert mom in the list
        self.__movements.append(m)
        self.__movements.sort(key=lambda x: x.time(), reverse=False)

    def remove(self, m):
        if not isinstance(m, Mom):
            print ("error")
            pass
        try:
            self.__movements.remove(m)
        except:
            # TODO: add exception class
            print("impossible delete " + m.to_string())

    def to_dict(self):
        return {
            'name': self.__name,
            'movements': [ mom.to_dict() for mom in self.__movements ],
            'lom_id': self.__lom_id,
            'last_mom_id': self._last_mom_id,
            'visible': self.__visible,
        }

    def from_dict(self, source):
        if source is not None and (not isinstance(source, dict)):
            print ("type error i want dict")
            return

        self.__name = source['name']
        self.__lom_id = source['lom_id']
        self.__last_mom_id = source['last_mom_id']
        self.__visible = source['visible']
        self.__movements = [ Mom(mom_dict) for mom_dict in source['movements'] ]


        # TODO: enable sort by date
        #self.Movements.sort(key=lambda x: x.date, reverse=False)


    def get_mom_in_period(self, start_date, time_delta):
        if not isinstance(start_date, datetime.date):
            print("type error")
            return
        if not isinstance(time_delta, datetime.timedelta):
            print("type error")
            return
        return [m for m in self.Movements if ((m.date >= start_date) and (m.date <= start_date+time_delta))]

    def get_mom_by_id(self, mom_id):
        if not isinstance(mom_id, int):
            print ("type error")
            return
        return [m for m in self.Movements if m.mom_id() == mom_id]

    def balance_per_day(self, start_date, end_date):
        if not isinstance(start_date, datetime.date):
            print("type error")
            return
        if not isinstance(end_date, datetime.date):
            print("type error")
            return
        if not isinstance(base_balance, float):
            print ("type error")
            return
        
        balance = 0

        for m in self.Movements:
            if m.date() < end_date:
                if m.date() >= start_date:
                    balance += m.direction()*m.price()

        return balance


# RUNS TESTS
if __name__ == "__main__":
    print ("testing loms")
    # TODO: write some tests
    # create 2 lom
    lom1 = Lom("lom1")
    # import 2 lom from json
    json_lom2 = {
        'visible': False,
        'name': 'lom2',
        'last_mom_id': -1,
        'lom_id': 2,
        'movements': []
    }
    json_lom3 = {
        'visible': False,
        'name': 'lom2',
        'last_mom_id': -1,
        'lom_id': 3,
        'movements': []
    }

    lom2 = Lom()
    lom3 = Lom()

    # implict test of from_json() method
    lom2.from_dict(json_lom2)
    lom3.from_dict(json_lom3)

    if lom2.lom_id() != json_lom2['lom_id']:
        print("failed method lom_id()")
        print (lom2.lom_id())
        print (json_lom2['lom_id'])
    else:
        print("method lom_id() ok")

    lom1.insert(
        Mom(
            price=float(10),
            direction=-1,
            mom_id=1,
            cause="test mom A",
            agent="agent mom A",
            payee="payee mom A",
            time=datetime.datetime.now()
        )
    )



