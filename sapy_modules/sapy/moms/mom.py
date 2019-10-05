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
import sapy_modules.sapy.moms.mom_bridge as mb 
import sapy_modules.core.db as db_iface

class Mom(object):  # movement of money
    """
    Class Movemet of Money, this is the base
    """
    import datetime

    def __init__(
        self,
        id = None,
        value=0,
        cause="not specified",
        time=datetime.datetime.today().date()
    ):
        self.value = float(value)
        self.cause = cause  # description of money movement
        self.time = time

        if id == None:
            self.id = mb.add_mom(value,cause,time)
        else:
            self.id = id

    def to_string(self, separator=" "):
        return str(self.value)+separator \
            + self.cause+separator \
            + self.time.isoformat()

    def to_dict(self):
        return {
            'value': self.value,
            'cause': self.cause,
            'time': {
                'year': self.time.year,
                'month': self.time.month,
                'day':  self.time.day,
            },
            'id': self.id
        }

    def from_dict(self, source=None):
        if source is not None and (not isinstance(source, dict)):
            print ("type error : source must be a dict")
            return

        if 'value' in source:
            self.value = float(source['value'])

        if 'mom_id' in source:
            self.id = source['id']

        if 'cause' in source:
            self.cause = source['cause']

        if 'time' in source:
            if 'year' in source['time']         \
                and 'month' in source['time']   \
                and 'day' in source['time'] :     
                self.time = datetime.datetime(
                    int(source['time']['year']),
                    int(source['time']['month']),
                    int(source['time']['day']),
                )
            elif 'year' in source['time']       \
                and 'month' in source['time']   \
                and 'day' in source['time']:
                self.time = datetime.datetime(
                    int(source['time']['year']),
                    int(source['time']['month']),
                    int(source['time']['day']),
                )

    def compare(self, mom):
        if not (isinstance(mom, Mom)):
            print ("type error")
            return None

        return dict(
            delta   = self.value - mom.value,
            mom_id  = [ self.id == mom.id ],
            cause   = [ self.cause == mom.cause ],
            time    = self.time - mom.time
        )

    def copy(self):
        return  copy.deepcopy(self)

    def delete(self):
        cur = db_iface.get_cursor()
        cur.execute( "delete from moms where id = ?", (self.id, ))
        cur.execute( "delete from mom_in_lom where mom_id = ?", (self.id, ))
        db_iface.commit()
        cur.close()
        self.value = None
        self.cause = None
        self.time  = None
        self.id    = None
 