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

        self.date = datetime.datetime.today().date()
        self.start_date = (self.date - datetime.timedelta(days=15)) # start date
        self.end_date = (self.date + datetime.timedelta(days=15))   # end date
        self.balance_value = 0

        self.moms_store = Gtk.ListStore(int, str, float, str, bool) # id cause, value, date
        self.view = Main_Window_View(self)
        self.set_list(self.lom_list[0].name)
        self.calc_balance()

    def set_list(self, lom_name):
        self.lom = loms.get_lom(name=lom_name)

        self.view.list_label.set_label(lom_name)

        moms = self.lom.get_moms(start_date=self.start_date, end_date=self.end_date)

        self.moms_store.clear()

        if len(moms) == 0:
            self.moms_store.append([-1, "-", 0, "-", False])
        else :
            for mom in self.lom.get_moms(start_date=self.start_date, end_date=self.end_date):
                self.moms_store.append([mom.id, mom.cause, mom.value, mom.time.strftime('%d-%m-%Y'), False])
        
        self.calc_balance()

    def rebuild_list(self, widget=None, event=None):

        moms = self.lom.get_moms(start_date=self.start_date, end_date=self.end_date)

        self.moms_store.clear()

        if len(moms) == 0:
            self.moms_store.append([-1, "-", 0, "-", False])
        else :
            for mom in self.lom.get_moms(start_date=self.start_date, end_date=self.end_date):
                self.moms_store.append([mom.id, mom.cause, mom.value, mom.time.strftime('%d-%m-%Y'), False])

    def calc_balance(self):
        self.balance_value = self.lom.balance(end_date=self.date)

        self.view.balance_value_label.set_label(str(self.balance_value))
        print(self.balance_value)

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
