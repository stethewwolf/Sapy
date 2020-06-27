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

import gi, datetime
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Date_Picker(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "pick a date", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(150, 100)

        box = self.get_content_area()

        self.calendar = Gtk.Calendar()

        box.add(self.calendar)

        self.show_all()

    def get_date(self):
        raw_date = self.calendar.get_date()
        picked_date = datetime.date(year=raw_date.year, month=raw_date.month+1, day=raw_date.day)
        return picked_date
 
    def set_date(self,date):
        self.calendar.select_month(month=date.month-1, year=date.year)
        self.calendar.select_day(day=date.day)