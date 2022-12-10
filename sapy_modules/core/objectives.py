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
from sapy_modules.commands.setters import set_end as se
import sapy_modules.utils.db as db_iface

CREATE_TABLE_OBJECTIVES = """
    CREATE TABLE "objectives" 
        ( "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
        "description" TEXT, 
        "duedate"	TEXT )
        """
SET_TAB_VERSION = """INSERT INTO "app_meta" ("key","value") VALUES ("obj_tab_version",?)"""

TAB_VERSION = 1

def create_tables():
    cur = db_iface.get_cursor()
    cur.execute(CREATE_TABLE_OBJECTIVES)
    cur.execute(SET_TAB_VERSION,(TAB_VERSION,))
    db_iface.commit()
    cur.close()

class Objective(object):  # movement of money
    """
    Class Objective, this is the base
    """

    def __init__(
        self,
        id = None,
        description='no description',
        duedate=datetime.datetime.today().date()
    ):
        self.description = description
        self.duedate = duedate

        if id == None:
            cur = db_iface.get_cursor()
            cur.execute( "insert into objectives (description,duedate) values ( ?, ?)", (description,duedate,))

            cur.execute("select id from objectives order by id DESC ;")
            self.id = cur.fetchone()[0]
    
            db_iface.commit()
            cur.close()
        else:
            self.id = id

    def to_dict(self):
        return {
            'description': self.description,
            'duedate': {
                'year': self.duedate.year,
                'month': self.duedate.month,
                'day':  self.duedate.day,
            },
            'id': self.id
        }

    def from_dict(self, source=None):
        if source is not None and (not isinstance(source, dict)):
            print ("type error : source must be a dict")
            return

        if 'id' in source:
            self.id = source['id']

        if 'description' in source:
            self.description = source['description']

        if 'duedate' in source:
            if 'year' in source['duedate']         \
                and 'month' in source['duedate']   \
                and 'day' in source['duedate'] :     
                self.time = datetime.datetime(
                    int(source['duedate']['year']),
                    int(source['duedate']['month']),
                    int(source['duedate']['day']),
                )

    def compare(self, obj):
        if not (isinstance(obj, Objective)):
            print ("type error")
            return None

        return dict(
            id  = [ self.id == obj.id ],
            cause   = [ self.description == obj.description ],
            time    = self.duedate - obj.duedate
        )

    def copy(self):
        return  copy.deepcopy(self)

    def delete(self):
        cur = db_iface.get_cursor()
        cur.execute( "delete from objectives where id = ?", (self.id, ))
        db_iface.commit()
        cur.close()
        self.description = None
        self.duedate  = None
        self.id    = None
 
def get_objs(logger):
    olist=[]

    cur = db_iface.get_cursor()
    cur.execute('select * from objectives')
    for l in cur.fetchall():
        olist.append(Objective(id=l[0], description=l[1], duedate=se.parse_date(l[2], logger)))
    cur.close()

    return olist

def get_obj(id,logger):
    cur = db_iface.get_cursor()
    cur.execute('select * from objectives where id = ?',(id,))
    l = cur.fetchone() 
    t = Objective(id=l[0], description=l[1], duedate=se.parse_date(l[2], logger))
    cur.close()
    return t
