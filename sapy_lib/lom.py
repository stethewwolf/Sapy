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

    def insert(self, m):
        # TODO: check m is mom type
        self.Movements.append(m)
        self.Movements.sort(key=lambda x: x.date, reverse=False)
        self.Balance = self.Balance + m.direction()*m.price()
        if m.direction() >= 0:
            self.Pos_sum += m.price()
        else:
            self.Neg_sum += m.price()

    def remove(self, m):
        # TODO: check m is mom type
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

    def to_jsonable(self):
        lom_jsonable = {
            'name': self.Name,
            'movements': [],
            'balance': self.Balance,
            'pos_sum': self.Pos_sum,
            'neg_sum': self.Neg_sum,
        }

        for mom in self.Movements:
            jmom = mom.to_jsonable()
            lom_jsonable['movements'].append(jmom)

        return lom_jsonable

    def from_jsonable(self, jsonable):
        self.Name = jsonable['name']

        tmp_pos_sum = 0
        tmp_neg_sum = 0

        for jmom in jsonable['movements']:
            new_mom = Mom()
            new_mom.from_jsonable(jmom)

            if new_mom.direction() >= 0:
                tmp_pos_sum += new_mom.price()
            else:
                tmp_neg_sum += new_mom.price()

            self.Movements.append(new_mom)

        self.Movements.sort(key=lambda x: x.date, reverse=False)

        if tmp_pos_sum != jsonable['pos_sum']:
            print("something went wrong whit pos_sum, using fresh calculated one")
            self.Pos_sum = tmp_pos_sum
        else:
            self.Pos_sum = jsonable['neg_sum']

        if tmp_neg_sum != jsonable['neg_sum']:
            print("something went wrong whit neg_sum, using fresh calculated one")
            self.Neg_sum = tmp_neg_sum
        else:
            self.Neg_sum = jsonable['neg_sum']

    def find_on_date(self, date):
        return [m for m in self.Movements if m.date == date]

    def get_in_period(self, start_date, time_delta):
        return [m for m in self.Movements if ((m.date >= start_date) and (m.date <= start_date+time_delta))]

    def balance_at_day(self, start_date, end_date, base_balance=0):
        balance = 0
        if base_balance != 0:
            balance = base_balance

        for m in self.Movements:
            if m.date() < end_date:
                if m.date() >= start_date:
                    # print m.direction*m.price
                    balance += m.direction()*m.price()

        return balance


# RUNS TESTS
if __name__ == "__main__":
    print ("testing loms")
