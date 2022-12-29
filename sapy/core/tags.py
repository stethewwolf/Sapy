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
CREATE_TAB_TAG = """
     CREATE TABLE "tags" (
     "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
     "name"	TEXT
    );"""
CREATE_TAB_TAG_IN_MOM ="""
    CREATE TABLE "tag_in_mom" (
        "mom_id"	INTEGER NOT NULL,
        "tag_id"	INTEGER NOT NULL,
        PRIMARY KEY("mom_id","tag_id")
        )"""

SET_TAB_VERSION = """INSERT INTO "app_meta" ("key","value") VALUES ("tag_tab_version",?)"""

TAB_VERSION = 1


def create_tables():
    cur = db_iface.get_cursor()
    cur.execute(CREATE_TAB_TAG)
    cur.execute(CREATE_TAB_TAG_IN_MOM)
    cur.execute(SET_TAB_VERSION,(TAB_VERSION,))
    db_iface.commit()
    cur.close()

class Tag(object):  # movement of money
    """
    Class Tag, this is the base
    """

    def __init__(
        self,
        id = None,
        name='noname',
    ):
        self.name = name

        if id == None:
            cur = db_iface.get_cursor()
            cur.execute( "insert into tags (name) values ( ? )", (name,))

            cur.execute("select id from tags order by id DESC ;")
            self.id = cur.fetchone()[0]
    
            db_iface.commit()
            cur.close()
        else:
            self.id = id

    def to_dict(self):
        return {
            'name': self.name,
            'id': self.id
        }

    def from_dict(self, source=None):
        if source is not None and (not isinstance(source, dict)):
            print ("type error : source must be a dict")
            return

        if 'id' in source:
            self.id = source['id']

        if 'name' in source:
            self.name = source['name']

    def compare(self, tag):
        if not (isinstance(tag, Tag)):
            print ("type error")
            return None

        return dict(
            id = [ self.id == tag.id ],
            name = [ self.name == tag.name ]
        )

    def copy(self):
        return  copy.deepcopy(self)

    def delete(self):
        cur = db_iface.get_cursor()
        cur.execute( "delete from tags where id = ?", (self.id, ))
        cur.execute( "delete from tag_in_mom where tag_id = ?", (self.id, ))
        db_iface.commit()
        cur.close()
        self.name  = None
        self.id    = None
 

def get_tags():
    tlist=[]

    cur = db_iface.get_cursor()
    cur.execute('select * from tags')
    for l in cur.fetchall():
        tlist.append(Tag(id=l[0], name=l[1]))
    cur.close()

    return tlist

def get_tag(id=None,name=None):
    cur = db_iface.get_cursor()
    if id :
        cur.execute('select * from tags where id = ?',(id,))
    elif name:
        cur.execute('select * from tags where name = ?',(name,))
    
    l = cur.fetchone() 
    t = Tag(id=l[0], name=l[1])

    cur.close()

    return t
