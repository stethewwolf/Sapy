#!/usr/bin/python3
#
#   file : mom.py
#   author : stefano prina <stethewwolf@gmail.com>
#
# mit license
#
# copyright (c) 2017 stefano prina <stethewwolf@gmail.com>
#
# permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "software"), to deal
# in the software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the software, and to permit persons to whom the software is
# furnished to do so, subject to the following conditions:
#
#     the above copyright notice and this permission notice shall be included in all
#     copies or substantial portions of the software.
#
#     the software is provided "as is", without warranty of any kind, express or
#     implied, including but not limited to the warranties of merchantability,
#     fitness for a particular purpose and noninfringement. in no event shall the
#     authors or copyright holders be liable for any claim, damages or other
#     liability, whether in an action of contract, tort or otherwise, arising from,
#     out of or in connection with the software or the use or other dealings in the
#     software.

import datetime, copy

class Mom(object):  # movement of money
    """
    Class Movemet of Money, this is the base
    """
    import datetime

    def __init__(
        self,
        value=0,
        mom_id=-1,
        cause="not specified",
        time=datetime.datetime.now()
    ):
        # type: (int, int, int, str, str, str, date, time) -> Mom
        self.__value = float(value)
        self.__mom_id = mom_id
        self.__cause = cause  # description of money movement
        self.__time = time

    def time(self, time=None):
        """ time function return the value, if time paramenter is passed it setted"""
        if time is not None and (not isinstance(time, datetime.datetime)):
            print ("type error")
            return

        if time:
            self.__time = time
        return self.__time

    def value(self, value=None):
        if value is not None and (not isinstance(value, float)):
            print ("type error")
            return
        if value:
            self.__value = value

        return self.__value

    def cause(self, cause=None):
        if cause is not None and (not isinstance(cause, str)):
            print ("type error")
            return
        if cause:
            self.__cause = cause
        return self.__cause

    def mom_id(self, mom_id=None):
        if mom_id is not None and (not isinstance(mom_id, int)):
            print ("type error")
            return
        if mom_id:
            self.__mom_id = mom_id
        return self.__mom_id

    def to_string(self, separator=" "):
        return str(self.__value)+separator \
            + self.__cause+separator \
            + self.__time.isoformat()

    def to_dict(self):
        return {
            'value': self.__value,
            'cause': self.__cause,
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

        if 'value' in source:
            self.__value = float(source['value'])

        if 'mom_id' in source:
            self.__mom_id = source['mom_id']

        if 'cause' in source:
            self.__cause = source['cause']

        if 'time' in source:
            if 'year' in source['time']         \
                and 'month' in source['time']   \
                and 'day' in source['time']     \
                and 'hours' in source['time']   \
                and 'minutes' in source['time']:
                self.__time = datetime.datetime(
                    int(source['time']['year']),
                    int(source['time']['month']),
                    int(source['time']['day']),
                    int(source['time']['hours']),
                    int(source['time']['minutes'])
                )
            elif 'year' in source['time']       \
                and 'month' in source['time']   \
                and 'day' in source['time']:
                self.__time = datetime.datetime(
                    int(source['time']['year']),
                    int(source['time']['month']),
                    int(source['time']['day']),
                )

    def compare(self, mom):
        if not (isinstance(mom, Mom)):
            print ("type error")
            return None
        return dict(
            price=self.__direction*self.__price - mom.__direction * mom.__price,
            mom_id=[self.__mom_id == mom.__mom_id],
            cause=[self.__cause == mom.__cause],
            time=self.__time-mom.__time
        )

    def copy(self):
        return  copy.deepcopy(self)

