#!/usr/bin/python3
#
#   file : objectives.py
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
import sapy_modules.commands.setter.set_end as se
import sapy_modules.core.db as db_iface

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