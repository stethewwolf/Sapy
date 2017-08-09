#!/bin/environment python
#
#   File : mom.py
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

import datetime


class Mom(object):  # movement of money
    import datetime

    def __init__(
        self,
        price=0,
        direction=1,
        mom_id=-1,
        cause="not specified",
        agent="not specified",
        payee="not specified",
        time=datetime.datetime.now()
    ):
        # type: (int, int, int, str, str, str, date, time) -> Mom
        self.Price = price
        self.Direction = direction
        self.Mom_id = mom_id
        self.Cause = cause  # description of money movement
        self.Agent = agent  # specify who move money
        self.Payee = payee  # specify who received money
        self.Time = time

    def time(self, time=None):
        if time is not None and (not isinstance(time, datetime.datetime)):
            print ("type error")
            return

        if time:
            self.Time = time
        return self.Time

    def price(self, price=None):
        if price is not None and (not isinstance(price, float)):
            print ("type error")
            return
        if price:
            if price >= 0:
                self.Price = price
                self.Direction=1
            else:
                self.Price = -1 * price
                self.Direction=-1

        return self.Price

    def direction(self, direction=None):
        if direction is not None and (not isinstance(direction, int)):
            print ("type error")
            return

        if direction:
            self.Direction = direction
        return self.Direction

    def cause(self, cause=None):
        if cause is not None and (not isinstance(cause, None)):
            print ("type error")
            return
        if cause:
            self.Cause = cause
        return self.Cause

    def agent(self, agent=None):
        if agent is not None and (not isinstance(agent,str)):
            print ("type error")
            return
        if agent:
            self.Agent = agent
        return self.Agent

    def payee(self, payee=None):
        if payee is not None and (not isinstance(payee, str)):
            print ("type error")
            return
        if payee:
            self.Payee = payee
        return self.Payee

    def mom_id(self, mom_id=None):
        if mom_id is not None and (not isinstance(mom_id, int)):
            print ("type error")
            return
        if mom_id:
            self.Mom_id = mom_id
        return self.Mom_id

    def to_string(self, separator=" "):
        result = ""
        result += str(self.Direction)+separator
        result += str(self.Price)+separator
        result += self.Cause+separator
        result += self.Agent+separator
        result += self.Payee+separator
        result += self.Date.isoformat()
        return result

    def to_json(self):
        tmp_data = {
            'price': self.Price,
            'direction': self.Direction,
            'cause': self.Cause,
            'agent': self.Agent,
            'payee': self.Payee,
            'time': {
                'year': self.Time.year,
                'month': self.Time.month,
                'day':  self.Time.day,
                'hours': self.Time.hour,
                'minutes':self.Time.minute
            },
            'mom_id': self.Mom_id
        }
        return tmp_data

    def from_json(self, jstring):
        if not jstring:
            # TODO: check if jstring is realy a str
            print ("type error : jstring must be a string")
            return
        self.Price = jstring['price']
        self.Direction = jstring['direction']
        self.Mom_id = jstring['mom_id']
        self.Cause = jstring['cause']
        self.Agent = jstring['agent']
        self.Payee = jstring['payee']
        self.Time = datetime.datetime(jstring['time']['year'], jstring['time']['month'], jstring['time']['day'],jstring['time']['hours'], jstring['time']['minutes'])
        pass

    def compare(self, lom):
        pass

# RUNS TESTS
if __name__ == "__main__":
    print ("testing mom")

    # mom1
    mom1_price = 59
    mom1_direction = 1
    mom1_id = 15
    mom1_cause = "test mom1"
    mom1_agent = "test mom1"
    mom1_payee = "test mom1"
    mom1_time = datetime.datetime.now()

    mom1 = Mom(
        price=mom1_price,
        direction=mom1_direction,
        mom_id=mom1_id,
        cause=mom1_cause,
        agent=mom1_agent,
        payee=mom1_payee,
        time=mom1_time
    )
    print mom1.to_json()

    if mom1.price() != mom1_price:
        print(" prices : do not match ")
    else:
        print(" prices : ok ")

    if mom1.direction() != mom1_direction:
        print(" directions : do not match ")
    else:
        print(" directions : ok ")

    if mom1.cause() != mom1_cause:
        print(" causes : do not match ")
    else:
        print(" causes : ok ")

    if mom1.agent() != mom1_agent:
        print(" agents : do not match ")
    else:
        print(" agents : ok ")

    if mom1.payee() != mom1_payee:
        print(" payees : do not match ")
    else:
        print(" payees : ok ")

    if mom1.time() != mom1_time:
        print(" time : do not match ")
    else:
        print(" time : ok ")

    # test import/export from json
    mom2 = Mom()

    mom2_json = {
        'direction': -1,
        'price': 34,
        'agent': 'test mom2',
        'payee': 'test mom2',
        'time': {
            'year': 2017,
            'month': 4,
            'day': 17,
            'hours': 16,
            'minutes': 45
        },
        'cause': 'test mom2',
        'mom_id': 2
    }

    print "pre"
    mom2.from_json(mom2_json)

    print "post"
    if mom2.to_json() == mom2_json:
        print ("conversion from/to json working")
    else:
        print ("conversion from/to json do not work")
        print mom2_json
        print mom2.to_json()
