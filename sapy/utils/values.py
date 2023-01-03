# Sapy
# Copyright (C) 2018 stefano prina <stethewwolf@posteo.net>
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
#

import configparser
import os
import sapy.core.loms as loms
from datetime import datetime

__store = {}


def init():
    global __store
    __store['end_date'] = datetime.today().date()
    __store['start_date'] = datetime.today().date()
    __store['date'] = datetime.today().date()
    __store['value'] = 0
    __store['frequency'] = None
    __store['lom'] = loms.get_loms()[0]
    __store['name'] = 'new name'

    # db values
    __store['db.create.app_meta'] = """
        CREATE TABLE "app_meta" (
            "id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "key"  TEXT NOT NULL UNIQUE,
            "value" TEXT NOT NULL
        ) """
    __store['db.populate.app_meta'] = """
        INSERT INTO "app_meta" ("key","value") VALUES ("app_version",?)
        """


def has_value(key):
    global __store
    return __store.has_key(key)


def get_value(key):
    global __store
    return __store[key]


def set_value(key, value):
    global __store
    __store[key] = value
