#!/usr/bin/python3
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

from sapy_modules.sapy.moms.mom import Mom
import sapy_modules.core.db as db_iface
import datetime
import sapy_modules.commands.setter.set_end as se
from sapy_modules.core import LoggerFactory

class Lom(object):  # list of movements
    def __init__(
        self,
        name="list of movements",
        id = -1
        ):
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))
        self.name = name
        self.id = id
        self.visible = False

    def add(self, mlist):
        cur = db_iface.get_cursor()
        for m in mlist:
            cur.execute( "insert into mom_in_lom (mom_id,lom_id) values ( ?, ?)", (m.id, self.id, ) )

        db_iface.commit()
        cur.close()

    def remove(self, m):
        pass

    def get_moms(self, id=None, start_date=None, end_date=None ):
        mlist = []
        cur = db_iface.get_cursor()

        if id :
            cur.execute( "SELECT * from moms where moms.id = ? ;", ( id, ) )
        else:
            cur.execute( "SELECT * from moms where moms.id in (select mom_id from mom_in_lom where lom_id = ? );", (self.id, ) )

        for raw in cur.fetchall():
            m = Mom( id=raw[0], value=raw[1], cause=raw[2], time=se.parse_date( raw[3], self.logger ) )
            if start_date and end_date :
                if m.time >= start_date and m.time <= end_date:
                    mlist.append( m )
            else:
                mlist.append( m )
                
        cur.close()
        return mlist

    def balance(self, start_date=None, end_date=None):
        balance = 0
        for m in self.get_moms(start_date=start_date,end_date=end_date):
            balance += m.value
        
        return balance

def get_lom( name ):
    cur = db_iface.get_cursor()
    cur.execute("select * from loms where `name` == ? ", (name, ))
    res = cur.fetchone()
    cur.close()
    return Lom(res[1], res[0])




