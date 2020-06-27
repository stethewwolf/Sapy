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
#

import sqlite3
from sapy_modules.core import SingleConfig

connession = None

def open():
    global  connession
    if not connession :
        connession = sqlite3.connect( SingleConfig.getConfig()['private']['data'] )
    pass

def get_cursor():
    global connession

    if not connession :
        open()

    return connession.cursor()

def commit():
    global connession

    if connession :
        connession.commit()

def close():
    global connession

    if connession :
        connession.close()

