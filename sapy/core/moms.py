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
import  sapy.utils.db as db_iface

## Queries
CREATE_TABLE = """
    CREATE TABLE "moms" (
        "id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "value" REAL NOT NULL,
        "cause" TEXT,
        "date"  TEXT NOT NULL
    );"""
DELETE_MOM = "DELETE FROM moms WHERE id = ?;"
DELETE_MOM_IN_LOM_LINK = "DELETE FROM mom_in_lom WHERE mom_id = ?;"
DELETE_MOM_IN_PROFILE_LINK = "DELETE FROM mom_in_profile WHERE mom_id = ?;"
INSERT_MOM = "INSERT INTO moms (value,cause,date) VALUES ( ?, ?, ?);"
GET_LAST_MOM = "SELECT id FROM moms ORDER BY id DESC ;"
UPDATE_MOM_VALUE = "UPDATE moms SET value=? WHERE id=?;"
UPDATE_MOM_CAUSE = "UPDATE moms SET cause=? WHERE id=?;"
UPDATE_MOM_TIME = "UPDATE moms SET date=? WHERE id=?;"
SET_TAB_VERSION = """INSERT INTO "app_meta" ("key","value") VALUES ("mom_tab_version",?)"""

TAB_VERSION = 1

def create_tables():
    cur = db_iface.get_cursor()
    cur.execute(CREATE_TABLE)
    cur.execute(SET_TAB_VERSION,(TAB_VERSION,))
    db_iface.commit()
    cur.close()

class Mom(object):  # movement of money
    """
    Class Movemet of Money, this is the base
    """
    def __init__(
        self,
        id:int=None,
        value:float=0,
        cause:str="not specified",
        year:int=datetime.datetime.today().date().year,
        month:int=datetime.datetime.today().date().month,
        day:int=datetime.datetime.today().date().day
        ):
        self.value = float(value)
        self.cause = cause  # description of money movement
        self.time = datetime.date(int(year),int(month),int(day))

        if id == None:
            cur = db_iface.get_cursor()
            cur.execute(INSERT_MOM, (self.value,self.cause,self.time,))

            cur.execute(GET_LAST_MOM)
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
        cur.execute(DELETE_MOM, (self.id, ))
        cur.execute(DELETE_MOM_IN_LOM_LINK, (self.id, ))
        cur.execute(DELETE_MOM_IN_PROFILE_LINK, (self.id, ))
        db_iface.commit()
        cur.close()
        self.value = None
        self.cause = None
        self.time  = None
        self.id    = None
        self = None

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
            cur.execute(UPDATE_MOM_VALUE, (new_value, self.id, ))
            self.value = float( new_value )

        if new_cause:
            cur.execute(UPDATE_MOM_CAUSE, (new_cause, self.id, ))
            self.cause = new_cause

        if new_year and new_month and new_day:
            new_time = datetime.date(year=new_year, month=new_month, day=new_day)
            cur.execute(UPDATE_MOM_TIME, (new_time, self.id, ))
            self.time = datetime.date(int(new_year),int(new_month),int(new_day))

        db_iface.commit()
        cur.close()

def date_key(mom):
    return int('{}{}{}'.format(mom.time.year,mom.time.month,mom.time.day))

def delete_mom(mom_id):
    cur = db_iface.get_cursor()
    cur.execute(DELETE_MOM, (mom_id, ))
    cur.execute(DELETE_MOM_IN_LOM_LINK, (mom_id, ))
    cur.execute(DELETE_MOM_IN_PROFILE_LINK, (mom_id, ))
    db_iface.commit()
    cur.close()
 
