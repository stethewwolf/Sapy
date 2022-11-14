 # Sapy
# Copyright (C) 2018 stefano prina  <stethewwolf@posteo.net>
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

from sapy_modules.core.moms import Mom
from sapy_modules.utils import constants as SapyConstants
from sapy_modules.core import loms
import sapy_modules.utils.db as db_iface
import datetime

CREATE_TABLE_PROFILES= """
	CREATE TABLE "profiles" (
       "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
       "name"	TEXT NOT NULL,
        "color" TEXT NOT NULL DEFAULT "blue"
    ) """

CREATE_TABLE_MOM_IN_PROFILE = """
	CREATE TABLE "mom_in_profile" (
        "mom_id"	INTEGER NOT NULL,
        "profile_id"	INTEGER NOT NULL,
        PRIMARY KEY("mom_id","profile_id")
    ) """

INSERT_PROFILE = "insert into profiles (name,color) values (?,?)"
GET_ALL_PROFILES = """SELECT * FROM profiles"""
GET_PROFILE_IDS = "select id from profiles order by id DESC ;"
GET_PROFILE_BY_ID = "SELECT * from profiles where id = ? ;"
GET_PROFILE_BY_NAME = 'select * from profiles where `name` == ? '
LINK_MOM_TO_PROFILE = "insert into mom_in_profile (mom_id,profile_id) values ( ?, ?)"
GET_MOM_IDS_IN_PROFILE = "select mom_id from mom_in_profile where `profile_id` == ?"
DELETE_PROFILE = "delete from profiles where id = ?"
UPDATE_PROFILE_NAME ="UPDATE profiles SET `name`=? WHERE id=?;"
UPDATE_PROFILE_COLOR ="UPDATE profiles SET `color`=? WHERE id=?;"
SET_TAB_VERSION = """INSERT INTO "app_meta" ("key","value") VALUES ("profile_tab_version",?)"""
CREATE_DEFAULT_PROFILE = """
    INSERT INTO "profiles"
    ("id","name","color") VALUES (1,"Default","blue");
    """
UPDATE_DEFAULT_PROFILE_ID ="""UPDATE app_meta SET value=? WHERE key='default_profile_id'"""
SET_DEFAULT_PROFILE_ID = """INSERT INTO "app_meta" ("key","value") VALUES ('default_profile_id',?) """
GET_DEFAULT_PROFILE_ID = """SELECT value from "app_meta" where `key` == 'default_profile_id' """

TAB_VERSION = 1

def create_tables():
    cur = db_iface.get_cursor()
    cur.execute(CREATE_TABLE_PROFILES)
    cur.execute(CREATE_TABLE_MOM_IN_PROFILE)
    cur.execute(CREATE_DEFAULT_PROFILE)
    cur.execute(SET_TAB_VERSION,(TAB_VERSION,))
    cur.execute(SET_DEFAULT_PROFILE_ID,(1,))
    db_iface.commit()
    cur.close()

def get_profile(name=None, id=None):
    cur = db_iface.get_cursor()
    if name:
        cur.execute(GET_PROFILE_BY_NAME,(name,))
    elif id:
        cur.execute(GET_PROFILE_BY_ID,(id,))
    res = cur.fetchone()
    cur.close()
    return Profile(res[0], res[1], res[2])

def get_profiles():
    llist=[]
    cur = db_iface.get_cursor()
    cur.execute(GET_ALL_PROFILES)
    for l in cur.fetchall():
            llist.append(Profile(l[0], l[1], l[2]))
    cur.close()
    return  llist

def get_default_profile_id():
    cur = db_iface.get_cursor()
    cur.execute(GET_DEFAULT_PROFILE_ID)
    res = cur.fetchone()
    cur.close()
    return res[0]

def set_default_profile_id(profile_id=None):
    if profile_id is not None:
        cur = db_iface.get_cursor()
        cur.execute(UPDATE_DEFAULT_PROFILE_ID,(profile_id,))
        db_iface.commit()
        cur.close()


class Profile(object):  # list of movements
    def __init__(
        self,
        id=None,
        name="profile",
        color="blue"
        ):
        if id == None:
            self.name = name
            self.color = color

            cur = db_iface.get_cursor()
            cur.execute(INSERT_PROFILE,(name,color))

            cur.execute(GET_PROFILE_IDS)
            self.id = cur.fetchone()[0]

            db_iface.commit()
            cur.close()
        else:
            self.id = id
            cur = db_iface.get_cursor()
            cur.execute(GET_PROFILE_BY_ID, (self.id,))
            raw_line = cur.fetchone()
            self.name =  raw_line[1]
            self.color = raw_line[2]
            cur.close()
        self.planned_lom = loms.get_lom(name=SapyConstants.DB.PLANNED_LIST_NAME)
        self.occurred_lom = loms.get_lom(name=SapyConstants.DB.OCCURRED_LIST_NAME)

    def update_name(self, name:str="profile"):
        self.name = name
        cur = db_iface.get_cursor()
        cur.execute(UPDATE_PROFILE_NAME,(name,self.id))
        db_iface.commit()
        cur.close()

    def update_color(self, color:str="green"):
        self.color = color
        cur = db_iface.get_cursor()
        cur.execute(UPDATE_PROFILE_COLOR,(color,self.id))
        db_iface.commit()
        cur.close()

    def remove_profile(self):
        for mom in self.get_moms():
            mom.delete()

        cur = db_iface.get_cursor()
        cur.execute(DELETE_PROFILE, (self.id, ))
        db_iface.commit()
        cur.close()
        self.name = None
        self.color = None
        self.id = None

    def get_moms(self):
        mom_ids = []
        cur = db_iface.get_cursor()
        cur.execute(GET_MOM_IDS_IN_PROFILE,(self.id, ))
        mom_ids = cur.fetchall()
        cur.close()
        return  [Mom(mom_id[0]) for mom_id in mom_ids]

    def get_planned_moms(self, start_date:datetime.date=None, end_date:datetime.date=None):
        return self.planned_lom.get_moms(start_date,end_date)

    def get_occurred_moms(self, start_date:datetime.date=None, end_date:datetime.date=None):
        return self.occurred_lom.get_moms(start_date,end_date)

    def add_planned_mom(self, mom_list:list):
        self.planned_lom.add(mom_list)
        cur = db_iface.get_cursor()
        for mom in mom_list:
            cur.execute(LINK_MOM_TO_PROFILE ,(mom.id,self.id))
        db_iface.commit()
        cur.close()

    def add_occurred_mom(self, mom_list:list):
        self.occurred_lom.add(mom_list)
        cur = db_iface.get_cursor()
        for mom in mom_list:
            cur.execute(LINK_MOM_TO_PROFILE ,(mom.id,self.id))
        db_iface.commit()
        cur.close()

    def get_planned_balance(self, start_date:datetime.date=None, end_date:datetime.date=None):
        return self.planned_lom.balance(start_date, end_date)

    def get_occurred_balance(self, start_date:datetime.date=None, end_date:datetime.date=None):
        return self.occurred_lom.balance(start_date, end_date)

    def get_planned_balance_per_day(self, start_date:datetime.date=None, end_date:datetime.date=None):
        return self.planned_lom.balance_per_day(start_date, end_date)

    def get_occurred_balance_per_day(self, start_date:datetime.date=None, end_date:datetime.date=None):
        return self.occurred_lom.balance_per_day(start_date, end_date)
