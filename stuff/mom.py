#!/usr/bin/python3
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

import datetime, copy

class Mom(object):  # movement of money
    """
    Class Movemet of Money, this is the base
    """
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
        self.__price = float(price)
        self.__direction = direction
        self.__mom_id = mom_id
        self.__cause = cause  # description of money movement
        self.__agent = agent  # specify who move money
        self.__payee = payee  # specify who received money
        self.__time = time

    def time(self, time=None):
        """ time function return the value, if time paramenter is passed it setted"""
        if time is not None and (not isinstance(time, datetime.datetime)):
            print ("type error")
            return

        if time:
            self.__time = time
        return self.__time

    def price(self, price=None):
        if price is not None and (not isinstance(price, float)):
            print ("type error")
            return
        if price:
            if price >= 0:
                self.__direction = 1
            else:
                self.__direction = -1

            self.__price = self.__direction * price

        return self.__price

    def direction(self, direction=None):
        if direction is not None and (not isinstance(direction, int)):
            print ("type error")
            return

        if direction:
            self.__direction = direction
        return self.__direction

    def cause(self, cause=None):
        if cause is not None and (not isinstance(cause, str)):
            print ("type error")
            return
        if cause:
            self.__cause = cause
        return self.__cause

    def agent(self, agent=None):
        if agent is not None and (not isinstance(agent, str)):
            print ("type error")
            return
        if agent:
            self.__agent = agent
        return self.__agent

    def payee(self, payee=None):
        if payee is not None and (not isinstance(payee, str)):
            print ("type error")
            return
        if payee:
            self.__payee = payee
        return self.__payee

    def mom_id(self, mom_id=None):
        if mom_id is not None and (not isinstance(mom_id, int)):
            print ("type error")
            return
        if mom_id:
            self.__mom_id = mom_id
        return self.__mom_id

    def to_string(self, separator=" "):
        return str(self.__direction * self.__price)+separator \
            + self.__cause+separator \
            + self.__agent+separator \
            + self.__payee+separator \
            + self.__time.isoformat()

    def to_dict(self):
        return {
            'price': self.__price,
            'direction': self.__direction,
            'cause': self.__cause,
            'agent': self.__agent,
            'payee': self.__payee,
            'time': {
                'year': self.__time.year,
                'month': self.__time.month,
                'day':  self.__time.day,
                'hours': self.__time.hour,
                'minutes':self.__time.minute
            },
            'mom_id': self.__mom_id
        }

    def from_dict(self, source=None):
        if source is not None and (not isinstance(source, dict)):
            print ("type error : source must be a dict")
            return
        self.__price = float(source['price'])
        self.__direction = source['direction']
        self.__mom_id = source['mom_id']
        self.__cause = source['cause']
        self.__agent = source['agent']
        self.__payee = source['payee']
        self.__time = datetime.datetime(
            source['time']['year'],
            source['time']['month'],
            source['time']['day'],
            source['time']['hours'],
            source['time']['minutes']
        )

    def compare(self, mom):
        if not (isinstance(mom, Mom)):
            print ("type error")
            return None
        return dict(
            price=self.__direction*self.__price - mom.__direction * mom.__price,
            mom_id=[self.__mom_id == mom.__mom_id],
            cause=[self.__cause == mom.__cause],
            agent=[self.__agent== mom.__agent],
            payee=[self.__payee == mom.__payee],
            time=self.__time-mom.__time
        )

    def copy(self):
        return  copy.deepcopy(self)

# RUNS TESTS
# todo: improve test : they must be more readable
if __name__ == "__main__":

    print ("testing mom")
    # to check
    # time
    # price
    # direction
    # cause
    # agent
    # payee
    # mom id
    # to string
    # to json
    # compare
    # copy


    # mom1
    mom1_price = 59
    mom1_direction = 1
    mom1_id = 15
    mom1_cause = "test"
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
    print (mom1.to_dict())

    if mom1.price() != mom1_price:
        print (" prices : do not match ")
    else:
        print (" prices : ok ")

    if mom1.direction() != mom1_direction:
        print (" directions : do not match ")
    else:
        print (" directions : ok ")

    if mom1.cause() != mom1_cause:
        print (" causes : do not match ")
    else:
        print (" causes : ok ")

    if mom1.agent() != mom1_agent:
        print (" agents : do not match ")
    else:
        print (" agents : ok ")

    if mom1.payee() != mom1_payee:
        print (" payees : do not match ")
    else:
        print (" payees : ok ")

    if mom1.time() != mom1_time:
        print (" time : do not match ")
    else:
        print (" time : ok ")

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
        'cause': 'test',
        'mom_id': 2
    }

    print ("pre")
    mom2.from_dict(mom2_json)

    print ("post")
    if mom2.to_dict() == mom2_json:
        print ("conversion from/to json working")
    else:
        print ("conversion from/to json do not work")
        print (mom2_json)
        print (mom2.to_dict())

    # check comparison
    print (mom2.to_string("!"))
    print (mom1.to_string("|"))
    print (mom2.to_dict())
    print (mom1.to_dict())
    print (mom2.compare(mom1))
    print (mom1.compare(mom2))

    mom3 = mom1.copy()
    print (mom1.compare(mom3))
