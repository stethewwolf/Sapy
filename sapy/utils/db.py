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

import sqlite3

__conn = None


def open(db_file):
    global __conn
    
    if not __conn:
        __conn = sqlite3.connect(db_file)


def get_cursor():
    global __conn

    if not __conn:
        open()

    return __conn.cursor()


def commit():
    global __conn

    if __conn:
        __conn.commit()


def close():
    global __conn

    if __conn:
        __conn.close()
