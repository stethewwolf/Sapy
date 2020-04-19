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

from sapy_modules.sapy.mom import Mom
import sapy_modules.core.db as db_iface
import sapy_modules.commands.setter.set_end as se
from sapy_modules.core import LoggerFactory
import datetime,csv

class Lom(object):  # list of movements
    def __init__(
        self,
        id=None,
        name="list of movements"
        ):
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))
        self.name = name
        self.visible = False

        if id == None:
            cur = db_iface.get_cursor()
            cur.execute( "insert into loms (name) values ( ?)", (name, ))

            cur.execute("select id from loms order by id DESC ;")
            self.id = cur.fetchone()[0]
    
            db_iface.commit()
            cur.close()
        else:
            self.id = id

    def add(self, mlist):
        cur = db_iface.get_cursor()
        for m in mlist:
            cur.execute( "insert into mom_in_lom (mom_id,lom_id) values ( ?, ?)", (m.id, self.id, ) )

        db_iface.commit()
        cur.close()

    def delete(self):
        cur = db_iface.get_cursor()
        cur.execute( "delete from loms where id = ?", (self.id, ))
        db_iface.commit()
        cur.close()
        self.name = None
        self.id    = None

    def get_moms(
            self, 
            start_date=datetime.datetime.today().date(), 
            end_date=datetime.datetime.today().date()
            ):
        mlist = []
        cur = db_iface.get_cursor()

        cur.execute( "SELECT * from moms where moms.id in (select mom_id from mom_in_lom where lom_id = ? );", (self.id, ) )

        for raw in cur.fetchall():
            raw_year = raw[3].split('-')[0]
            raw_month = raw[3].split('-')[1]
            raw_day = raw[3].split('-')[2]
            m = Mom(id=raw[0], value=raw[1], cause=raw[2], year=raw_year, month=raw_month, day=raw_day)
            md = datetime.date(year = m.time.year, month = m.time.month, day = m.time.day)
            sd = datetime.date(year = start_date.year, month = start_date.month, day = start_date.day)
            ed = datetime.date(year = end_date.year, month = end_date.month, day = end_date.day)
            
            if sd and ed :
                if md >= sd and md <= ed:
                    mlist.append( m )
            elif sd is None and ed :
                if md <= ed:
                    mlist.append( m )
            elif start_date and end_date is None :
                if md >= sd :
                    mlist.append( m )
            else:
                mlist.append( m )
                
        cur.close()
        return mlist

    def get_mom(self,id):
        cur = db_iface.get_cursor()
        cur.execute( "SELECT * from moms where moms.id = ? ;", ( id, ) )
        raw = cur.fetchone()
        raw_year = raw[3].split('-')[0]
        raw_month = raw[3].split('-')[1]
        raw_day = raw[3].split('-')[2]
        return Mom(id=raw[0], value=raw[1], cause=raw[2], year=raw_year, month=raw_month, day=raw_day)
 
    def csv_import(self,csv_file):
        mom_list = []
        #m_dialect = csv.Dialect()
        #m_dialect.delimiter=";"
        with open(str(csv_file.get_path()),'r') as data_file:
            data = csv.DictReader(data_file, fieldnames=[
                'cause',
                'value',
                'day',
                'month',
                'year'
            ])
            #data = csv.DictReader(data_file, fieldnames=[
            #    'cause',
            #    'value',
            #    'date'
            #], dialect=m_dialect)

            for raw_mom in data:
                #print(raw_mom)
                #raw_year  = raw_mom['date'].split('.')[2]
                #raw_month = raw_mom['date'].split('.')[1]
                #raw_day = raw_mom['date'].split('.')[0]

                #mom_list.append( Mom(
                #    cause= raw_mom['cause'],
                #    value= raw_mom['value'],
                #    year=raw_year,
                #    month=raw_month,
                #    day=raw_day
                #) 
 
                mom_list.append( 
                    Mom(
                        cause= raw_mom['cause'],
                        value= raw_mom['value'],
                        year=raw_mom['year'],
                        month=raw_mom['month'],
                        day=raw_mom['day']
                    ) 
                )

        self.add(mom_list)


    def balance(self, start_date=None, end_date=None):
        balance = 0
        for m in self.get_moms(start_date=start_date,end_date=end_date):
            balance += m.value
        
        return balance

    def balance_per_day(self, start_date=None, end_date=None):
        moms = self.get_moms(start_date=start_date,end_date=end_date)

        dates = []
        values = []

        min_date = datetime.date(datetime.MAXYEAR,1,1)
        max_date = datetime.date(datetime.MINYEAR,12,31)

        for mom in moms:
            if mom.time < min_date:
                min_date = mom.time
            
            if mom.time > max_date:
                max_date = mom.time
        
        time_delta = datetime.timedelta(days=1)

        while min_date <= max_date:
            day_balance = 0

            for mom in self.get_moms(start_date=min_date,end_date=min_date):
                day_balance += mom.value

            dates.append(min_date)
            values.append(day_balance)

            min_date += time_delta

        return (dates,values)

def get_lom(name=None, id=None):
    cur = db_iface.get_cursor()
    if name:
        cur.execute('select * from loms where `name` == ? ', (name, ))
    elif id:
        cur.execute('select * from loms where `id` == ? ', (id, ))
    res = cur.fetchone()
    cur.close()
    return Lom(res[0], res[1])

def get_loms():
    llist=[]
    cur = db_iface.get_cursor()
    cur.execute('select * from loms ')
    for l in cur.fetchall():
        llist.append(Lom(l[0], l[1]))
    cur.close()
    return  llist




