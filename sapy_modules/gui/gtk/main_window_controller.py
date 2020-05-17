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

from sapy_modules.gui.gtk import Main_Window_View
from sapy_modules.sapy import loms
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import datetime


class Main_Window_Controller(object):

    def __init__(self):
        self.lom_list = loms.get_loms()
        self.lom = None
        self.view = None
        self.moms_store = Gtk.ListStore(int, str, float, str, bool) # id cause, value, date
        self.set_list(self.lom_list[0].name)
        self.view = Main_Window_View(self)

    def set_list(self, lom_name):
        self.lom = loms.get_lom(name=lom_name)

        if not self.view:
            date = datetime.datetime.today().date()
        else:
            raw_date = self.view.calendar.get_date()
            date = datetime.date(year = raw_date.year, month = raw_date.month+1, day = raw_date.day)

        sd = date - datetime.timedelta(days=15) # start date
        ed = date + datetime.timedelta(days=15) # end date

        moms = self.lom.get_moms(start_date=sd, end_date=ed)

        self.moms_store.clear()

        if len(moms) == 0:
            self.moms_store.append([-1, "-", 0, "-", False])
        else :
            for mom in self.lom.get_moms(start_date=sd, end_date=ed):
                self.moms_store.append([mom.id, mom.cause, mom.value, mom.time.strftime('%d-%m-%Y'), False])

        pass

    def rebuild_list(self, widget=None, event=None):
        print("list updated")
        if not self.view:
            date = datetime.datetime.today().date()
        else:
            raw_date = self.view.calendar.get_date()
            print(raw_date)
            date = datetime.date(year = raw_date.year, month = raw_date.month+1, day = raw_date.day)

        sd = date - datetime.timedelta(days=15) # start date
        ed = date + datetime.timedelta(days=15) # end date

        moms = self.lom.get_moms(start_date=sd, end_date=ed)

        self.moms_store.clear()

        if len(moms) == 0:
            self.moms_store.append([-1, "-", 0, "-", False])
        else :
            for mom in self.lom.get_moms(start_date=sd, end_date=ed):
                self.moms_store.append([mom.id, mom.cause, mom.value, mom.time.strftime('%d-%m-%Y'), False])

        pass


    def add_mom(self, mom):
        self.lom.add([mom])
        self.moms_store.append([mom.id, mom.cause, mom.value, mom.time.strftime('%d-%m-%Y'), False])

    def del_mom(self):
        for mom_row in self.moms_store:
            if mom_row[4]:
                del_mom = self.lom.get_mom(mom_row[0])

                if del_mom:
                    del_mom.delete()
            
                self.moms_store.remove(mom_row.iter)

    def run (self):
        self.view.main()
