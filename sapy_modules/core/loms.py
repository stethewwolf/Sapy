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


from xml.dom.minidom import TypeInfo
from sapy_modules.utils import loggers as LoggerFactory
from sapy_modules.utils import config as SingleConfig
from sapy_modules.utils import constants as SapyConstants
from sapy_modules.utils import values as SapyValues
import sapy_modules.utils.db as db_iface
import datetime,csv
from sapy_modules.core.moms import Mom
import re

CREATE_TABLE_LOM= """
	CREATE TABLE "loms" (
       "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
       "name"	TEXT NOT NULL UNIQUE,
        "visible" INTEGER NOT NULL DEFAULT 0,
        "color" TEXT NOT NULL DEFAULT "red"
    ) """
CREATE_TABLE_MOM_IN_LOM = """
	CREATE TABLE "mom_in_lom" (
        "mom_id"	INTEGER NOT NULL,
        "lom_id"	INTEGER NOT NULL,
        PRIMARY KEY("lom_id","mom_id")
    ) """
INSERT_LOM = "insert into loms (name,visible,color) values (?,?,?)"
GET_LAST_LOM = "select id from loms order by id DESC ;"
LINK_MOM_TO_LOM ="insert into mom_in_lom (mom_id,lom_id) values ( ?, ?)"
DELETE_LOM = "delete from loms where id = ?"
GET_MOMS_0 = """
        SELECT * FROM (
            SELECT id,value,cause,date,lom_id
                FROM moms INNER join mom_in_lom on moms.id = mom_in_lom.mom_id
            )
        where lom_id = ?
        """
GET_MOMS_1 = """
        SELECT * FROM (
            SELECT id,value,cause,date,lom_id
                FROM moms INNER join mom_in_lom on moms.id = mom_in_lom.mom_id
            )
        where lom_id = ? and  date <= ?
        """
GET_MOMS_2 = """
        SELECT * FROM (
            SELECT id,value,cause,date,lom_id
                FROM moms INNER join mom_in_lom on moms.id = mom_in_lom.mom_id
            )
        where lom_id = ? and date >= ?
        """
GET_MOMS_3 = """
        SELECT * FROM (
            SELECT id,value,cause,date,lom_id
                FROM moms INNER join mom_in_lom on moms.id = mom_in_lom.mom_id
            )
        where lom_id = ? and date >= ? and date <= ?
        """
GET_MOM = "SELECT * from moms where moms.id = ? ;"
GET_LOM_BY_NAME = 'select * from loms where `name` == ? '
GET_LOM_BY_ID = 'select * from loms where `id` == ? '
GET_ALL_LOMS = """SELECT * FROM loms"""
CREATE_DEFAULT_LOMS = """
    INSERT INTO "loms"
    ("id","name","visible","color") VALUES
    ({},'{}','{}','{}'),
    ({},'{}','{}','{}')
    ;""".format(
        SapyConstants.DB.OCCURRED_LIST_ID,
        SapyConstants.DB.OCCURRED_LIST_NAME,
        SapyConstants.DB.OCCURRED_LIST_VISIBLE,
        SapyConstants.DB.OCCURRED_LIST_COLOR,
        SapyConstants.DB.PLANNED_LIST_ID,
        SapyConstants.DB.PLANNED_LIST_NAME,
        SapyConstants.DB.PLANNED_LIST_VISIBLE,
        SapyConstants.DB.PLANNED_LIST_COLOR
        )

UPDATE_LOM_VISIBLE ="UPDATE loms SET `visible`=? WHERE id=?;"
UPDATE_LOM_NAME ="UPDATE loms SET `name`=? WHERE id=?;"
UPDATE_LOM_COLOR ="UPDATE loms SET `color`=? WHERE id=?;"
GET_LOM_VISIBLE ="SELECT visible FROM loms WHERE id=?;"
SET_TAB_VERSION = """INSERT INTO "app_meta" ("key","value") VALUES ("lom_tab_version",?)"""

TAB_VERSION = 1

def create_tables():
    cur = db_iface.get_cursor()
    cur.execute(CREATE_TABLE_LOM)
    cur.execute(CREATE_TABLE_MOM_IN_LOM)
    cur.execute(CREATE_DEFAULT_LOMS)
    cur.execute(SET_TAB_VERSION,(TAB_VERSION,))
    db_iface.commit()
    cur.close()

class Lom(object):  # list of movements
    def __init__(
        self,
        id=None,
        name="list of movements",
        visible=False,
        color="black"
        ):
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))
        self.name = name
        self.visible = visible
        self.color = color

        if id == None:
            cur = db_iface.get_cursor()
            cur.execute(INSERT_LOM,(name,visible,color))

            cur.execute(GET_LAST_LOM)
            self.id = cur.fetchone()[0]

            db_iface.commit()
            cur.close()
        else:
            self.id = id

    def add(self, mlist):
        cur = db_iface.get_cursor()
        for m in mlist:
            cur.execute(LINK_MOM_TO_LOM,(m.id, self.id, ))

        db_iface.commit()
        cur.close()

    def delete(self):
    	#TODO : before delete the lom delete all the moms linked
        cur = db_iface.get_cursor()
        cur.execute(DELETE_LOM,(self.id, ))
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

        _start_date = None
        _end_date = None

        if start_date is not None :
            if type(start_date) is datetime.datetime:
                _start_date = start_date.date()
            else :
                _start_date = start_date.strftime('%Y-%m-%d')

        if end_date is not None :
            if type(end_date) is datetime.datetime:
                _end_date = end_date.date()
            else :
                _end_date = end_date.strftime('%Y-%m-%d')


        if _start_date is None and _end_date is None:
            cur.execute(GET_MOMS_0, (self.id, ) )
        elif start_date is None and _end_date is not None:
            cur.execute(GET_MOMS_1, (self.id,_end_date) )
        elif start_date is not None and _end_date is None:
            cur.execute(GET_MOMS_2, (self.id, _start_date) )
        elif start_date is not None and end_date is not None:
            cur.execute(GET_MOMS_3, (self.id, _start_date, _end_date) )

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
        cur.execute(GET_MOM,( id, ))
        raw = cur.fetchone()
        raw_year = raw[3].split('-')[0]
        raw_month = raw[3].split('-')[1]
        raw_day = raw[3].split('-')[2]
        return Mom(id=raw[0], value=raw[1], cause=raw[2], year=raw_year, month=raw_month, day=raw_day)

    def csv_import(self,csv_file):
        mom_list = []
        with open(str(csv_file.get_path()),'r') as data_file:
            data = csv.DictReader(data_file, fieldnames=[
                'date',
                'cause',
                'value'
            ], delimiter=";",quoting=csv.QUOTE_NONE) # TODO : add configuration option for delimiter

            for raw_mom in data:
                # TODO : add configuration option for manage date formats
                raw_year  = raw_mom['date'].split('.')[2]
                raw_month = raw_mom['date'].split('.')[1]
                raw_day = raw_mom['date'].split('.')[0]

                mom = Mom(
                    cause= re.escape( raw_mom['cause']),
                    value= float(raw_mom['value'].replace(",",".")),
                    year=raw_year,
                    month=raw_month,
                    day=raw_day
                )

                mom_list.append( mom )

        self.add(mom_list)

    def balance(self, start_date=None, end_date=None):
        balance = 0

        for m in self.get_moms(start_date=start_date,end_date=end_date):
            balance += m.value

        return balance

    def balance_per_day(self, start_date=None, end_date=None):
        base_balance = self.balance(end_date=start_date)
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
            day_balance = base_balance

            for mom in self.get_moms(start_date=min_date,end_date=min_date):
                day_balance += mom.value

            dates.append(min_date)
            values.append(day_balance)

            min_date += time_delta
            base_balance = day_balance

        return (dates,values)

    def set_visible(self,value):
        self.visible = value
        cur = db_iface.get_cursor()
        if self.visible :
            cur.execute(UPDATE_LOM_VISIBLE,(1,self.id))
        else:
            cur.execute(UPDATE_LOM_VISIBLE,(0,self.id))
        db_iface.commit()

    def set_name(self,value):
        self.name = value
        cur = db_iface.get_cursor()
        cur.execute(UPDATE_LOM_NAME,(self.name,self.id))
        db_iface.commit()

    def set_color(self,value):
        self.color = value
        cur = db_iface.get_cursor()
        cur.execute(UPDATE_LOM_COLOR,(self.color,self.id))
        db_iface.commit()

def get_lom(name=None, id=None):
    cur = db_iface.get_cursor()
    if name:
        cur.execute(GET_LOM_BY_NAME,(name,))
    elif id:
        cur.execute(GET_LOM_BY_ID,(id,))
    res = cur.fetchone()
    cur.close()
    return Lom(res[0], res[1], res[2], res[3])

def get_loms():
    llist=[]
    cur = db_iface.get_cursor()
    cur.execute(GET_ALL_LOMS)
    for l in cur.fetchall():
        if l[2] == 1:
            llist.append(Lom(l[0], l[1], True, l[3]))
        else:
            llist.append(Lom(l[0], l[1], False, l[3]))
    cur.close()
    return  llist



