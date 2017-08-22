#!/bin/environment python
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
        self.Name = name
        self.Movements = []  # array ordered by date
        self.Balance = 0
        self.Pos_sum = 0
        self.Neg_sum = 0
        self.Lom_id = 1
        self.Last_mom_id = -1
        self.Visible = False

    def visible(self, visible=True):
        if not isinstance(visible, bool):
            print ("type error")
            pass

        if id:
            self.Visible = visible
        return self.Visible

    def lom_id(self, lom_id=None):
        if lom_id is not None and (not isinstance(lom_id, int)):
            print ("type error")
            return -1
        if lom_id:
            self.Lom_id = lom_id
        return self.Lom_id

    def get_num_omoms(self): # defined for debug purpose
        return len(self.Movements)

    def insert(self, m):
        if m is not None and (not isinstance(m, Mom)):
            print "type error"
            return

        # manage ids
        self.Last_mom_id += 1
        m.mom_id(self.Last_mom_id)

        # insert mom in the list
        self.Movements.append(m)
        self.Movements.sort(key=lambda x: x.time, reverse=False)
        self.Balance = self.Balance + m.direction()*m.price()
        if m.direction() >= 0:
            self.Pos_sum += m.price()
        else:
            self.Neg_sum += m.price()

    def remove(self, m):
        if not isinstance(m, Mom):
            print "error"
            pass
        try:
            self.Movements.remove(m)
            self.Balance -= m.direction()*m.price()
            if m.direction() >= 0:
                self.Pos_sum -= m.price()
            else:
                self.Neg_sum -= m.price()
        except:
            # TODO: add exception class
            print("impossible delete " + m.to_string())

    def to_json(self):
        lom_json = {
            'name': self.Name,
            'movements': [],
            'balance': self.Balance,
            'pos_sum': self.Pos_sum,
            'neg_sum': self.Neg_sum,
            'lom_id': self.Lom_id,
            'last_mom_id': self.Last_mom_id,
            'visible': self.Visible,
        }

        for mom in self.Movements:
            jmom = mom.to_json()
            lom_json['movements'].append(jmom)

        return lom_json

    def from_json(self, json):
        if json is not None and (not isinstance(json, dict)):
            print ("type error i want dict")
            return
        self.Name = json['name']
        self.Lom_id = json['lom_id']
        self.Last_mom_id = json['last_mom_id']
        self.Visible = json['visible']

        tmp_pos_sum = 0
        tmp_neg_sum = 0

        for jmom in json['movements']:
            new_mom = Mom()
            new_mom.from_json(jmom)

            if new_mom.direction() >= 0:
                tmp_pos_sum += new_mom.price()
            else:
                tmp_neg_sum += new_mom.price()

            self.Movements.append(new_mom)

        self.Movements.sort(key=lambda x: x.date, reverse=False)

        if tmp_pos_sum != json['pos_sum']:
            print("something went wrong whit pos_sum, using fresh calculated one")
            self.Pos_sum = tmp_pos_sum
        else:
            self.Pos_sum = json['neg_sum']

        if tmp_neg_sum != json['neg_sum']:
            print("something went wrong whit neg_sum, using fresh calculated one")
            self.Neg_sum = tmp_neg_sum
        else:
            self.Neg_sum = json['neg_sum']

    def find_on_date(self, date):
        if not isinstance(date, datetime.date):
            print ("type error")
            return
        return [m for m in self.Movements if m.date == date]

    def get_in_period(self, start_date, time_delta):
        if not isinstance(start_date, datetime.date):
            print("type error")
            return
        if not isinstance(time_delta, datetime.timedelta):
            print("type error")
            return
        return [m for m in self.Movements if ((m.date >= start_date) and (m.date <= start_date+time_delta))]

    def get_by_id(self, mom_id):
        if not isinstance(mom_id, int):
            print ("type error")
            return
        return [m for m in self.Movements if m.Mom_id == mom_id]

    def balance_at_day(self, start_date, end_date, base_balance=0):
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
        if base_balance != 0:
            balance = base_balance

        for m in self.Movements:
            if m.date() < end_date:
                if m.date() >= start_date:
                    # print m.direction*m.price
                    balance += m.direction()*m.price()

        return balance

    def balance_per_day(self, start_date, end_date, base_balance=0):
        if not isinstance(start_date, datetime.date):
            print("type error")
            return
        if not isinstance(end_date, datetime.date):
            print("type error")
            return
        if not isinstance(base_balance, float):
            print ("type error")
            return
        pass

# RUNS TESTS
if __name__ == "__main__":
    print ("testing loms")
    # TODO: write some tests
    # create 2 lom
    lom1 = Lom("lom1")
    # import 2 lom from json
    json_lom2 = {
        'visible': False,
        'neg_sum': 0,
        'name': 'lom2',
        'last_mom_id': -1,
        'pos_sum': 0,
        'lom_id': 2,
        'balance': 0,
        'movements': []
    }
    json_lom3 = {
        'visible': False,
        'neg_sum': 0,
        'name': 'lom2',
        'last_mom_id': -1,
        'pos_sum': 0,
        'lom_id': 3,
        'balance': 0,
        'movements': []
    }

    lom2 = Lom()
    lom3 = Lom()

    # implict test of from_json() method
    lom2.from_json(json_lom2)
    lom3.from_json(json_lom3)

    if lom2.lom_id() != json_lom2['lom_id']:
        print("failed method lom_id()")
        print lom2.lom_id()
        print json_lom2['lom_id']
    else:
        print("method lom_id() ok")

    # testing get_num_omoms
    nomom = lom1.get_num_omoms()
    if(nomom != 0):
        print("failed method get_num_omoms")
    else:
        print("ok method get_num_omoms")

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

    if ( lom1.get_num_omoms() == 1):
        print("ok method insert")
    else:
        print("failed method insert")


