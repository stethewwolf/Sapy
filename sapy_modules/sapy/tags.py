#!/usr/bin/python3
#
#   file : tags.py
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
import sapy_modules.core.db as db_iface


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