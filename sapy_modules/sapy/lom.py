# Sapy
# Copyright (C) 2018 stefano prina <stethewwolf@null.net> <stethewwolf@gmail.com>
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

        query0 = """
                SELECT * FROM (
                    SELECT id,value,cause,date,lom_id 
                        FROM moms INNER join mom_in_lom on moms.id = mom_in_lom.mom_id
                    )
                where lom_id = ? 
                """
        query1 = """
                SELECT * FROM (
                    SELECT id,value,cause,date,lom_id 
                        FROM moms INNER join mom_in_lom on moms.id = mom_in_lom.mom_id
                    )
                where lom_id = ? and  date <= ?
                """
        query2 = """
                SELECT * FROM (
                    SELECT id,value,cause,date,lom_id 
                        FROM moms INNER join mom_in_lom on moms.id = mom_in_lom.mom_id
                    )
                where lom_id = ? and date >= ? 
                """
        query3 = """
                SELECT * FROM (
                    SELECT id,value,cause,date,lom_id 
                        FROM moms INNER join mom_in_lom on moms.id = mom_in_lom.mom_id
                    )
                where lom_id = ? and date >= ? and date <= ?
                """
                
        if start_date is None and end_date is None:
            cur.execute(query0, (self.id, ) )
        elif start_date is None and end_date is not None:
            cur.execute(query1, (self.id,end_date.strftime('%Y-%m-%d') ) )
        elif start_date is not None and end_date is None:
            cur.execute(query2, (self.id,start_date.strftime('%Y-%m-%d') ) )
        elif start_date is not None and end_date is not None:
            cur.execute(query3, (self.id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d') ) )

        for raw in cur.fetchall():
            raw_year = raw[3].split('-')[0]
            raw_month = raw[3].split('-')[1]
            raw_day = raw[3].split('-')[2]
            mom = Mom(id=raw[0], value=raw[1], cause=raw[2], year=raw_year, month=raw_month, day=raw_day)
            mlist.append(mom)

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

        print("----------------------")
        for m in self.get_moms(start_date=start_date,end_date=end_date):
            balance += m.value
            print(str(m.value) + str(m.time))
            
        print("----------------------")
        print(balance)
        print("----------------------")
        
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




