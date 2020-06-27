# Sapy
# Copyright (C) 2018 stefano prina <stefano-prina@outlook.it> <stethewwolf@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime, copy
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
        year=datetime.datetime.today().date().year,
        month=datetime.datetime.today().date().month,
        day=datetime.datetime.today().date().day
        ):
        self.value = float(value)
        self.cause = cause  # description of money movement
        self.time = datetime.date(int(year),int(month),int(day))

        if id == None:
            cur = db_iface.get_cursor()
            cur.execute( "insert into moms (value,cause,date) values ( ?, ?, ?)", (self.value,self.cause,self.time, ))

            cur.execute("select id from moms order by id DESC ;")
            self.id = cur.fetchone()[0]
    
            db_iface.commit()
            cur.close()
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
                self.time = datetime.date(
                    year=int(source['time']['year']),
                    month=int(source['time']['month']),
                    day=int(source['time']['day'])
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

    def update(
            self,
            new_value= None,
            new_cause= None,
            new_year = None,
            new_month= None,
            new_day  = None
        ):
        cur = db_iface.get_cursor()

        if new_value:
            cur.execute("UPDATE moms SET value=? WHERE id=?;", (new_value, self.id, ))
        
        if new_cause:
            cur.execute("UPDATE moms SET cause=? WHERE id=?;", (new_cause, self.id, ))
        
        if new_year and new_month and new_day:
            new_time = datetime.date(year=new_year, month=new_month, day=new_day)
            cur.execute("UPDATE moms SET date=? WHERE id=?;", (new_time, self.id, ))

        db_iface.commit()
        cur.close()
