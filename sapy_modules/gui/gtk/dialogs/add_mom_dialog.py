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
from sapy_modules.sapy import moms
from sapy_modules.gui.gtk.dialogs.date_picker import Date_Picker
from calendar import monthrange

class Add_Mom_Dialog_View(Gtk.MessageDialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "add new movement", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(150, 100)

        box = self.get_content_area()
        grid = Gtk.Grid()
        
        # value field
        value_label = Gtk.Label("value")
        value_adjustment = Gtk.Adjustment(0, -99999, 99999, 0.1, 1, 0)
        self.value_button = Gtk.SpinButton()
        self.value_button.set_adjustment(value_adjustment)
        self.value_button.set_digits(2)
        self.value_button.set_numeric(True)

        grid.add(value_label)
        grid.attach_next_to( 
                self.value_button,
                value_label, 
                Gtk.PositionType.RIGHT, 
                1, 1
                )

        cause_label = Gtk.Label("Cause")
        self.cause_entry = Gtk.Entry()
        self.cause_entry.set_placeholder_text("cause")

        grid.attach_next_to(
                cause_label, 
                value_label, 
                Gtk.PositionType.BOTTOM, 
                1, 1
                )

        grid.attach_next_to( 
                self.cause_entry,
                cause_label, 
                Gtk.PositionType.RIGHT, 
                1, 1
                )
        

        #Date selection
        date = datetime.datetime.today().date()

        date_label = Gtk.Label("Date")

        grid.attach_next_to(
                date_label, 
                cause_label, 
                Gtk.PositionType.BOTTOM, 
                1, 1
                )

        year_label = Gtk.Label("Year")
        year_adjustment = Gtk.Adjustment(date.year, 1900, 2100, 1, 1, 0)
        self.year_spin = Gtk.SpinButton()
        self.year_spin.configure(year_adjustment,1,0)
        self.year_spin.connect("value-changed",self.update_day_adj)

        grid.attach_next_to(
                year_label,
                date_label, 
                Gtk.PositionType.BOTTOM, 
                1, 1
                )
        grid.attach_next_to(
                self.year_spin,
                year_label,
                Gtk.PositionType.RIGHT, 
                1, 1
                )

        month_label = Gtk.Label("Month")
        month_adjustment = Gtk.Adjustment(date.month, 1, 12, 1, 1, 0)
        self.month_spin = Gtk.SpinButton()
        self.month_spin.configure(month_adjustment,1,0)
        self.month_spin.connect("value-changed",self.update_day_adj)

        grid.attach_next_to(
                month_label,
                year_label,
                Gtk.PositionType.BOTTOM, 
                1, 1
                )
        grid.attach_next_to(
                self.month_spin,
                month_label,
                Gtk.PositionType.RIGHT, 
                1, 1
                )

        day_label = Gtk.Label("Day")
        day_adjustment = Gtk.Adjustment(date.day, 1, monthrange(date.year,date.month)[1], 1, 1, 0)
        self.day_spin = Gtk.SpinButton()
        self.day_spin.configure(day_adjustment,1,0)

        grid.attach_next_to(
                day_label,
                month_label,
                Gtk.PositionType.BOTTOM, 
                1, 1
                )
        grid.attach_next_to(
                self.day_spin,
                day_label,
                Gtk.PositionType.RIGHT, 
                1, 1
                )

        box.add(grid)
        self.show_all()

    def get_mom(self):
        raw_cause =  self.cause_entry.get_text()
        raw_value = float(self.value_button.get_value())

        return moms.Mom(cause=raw_cause, value=raw_value, year=self.year_spin.get_value_as_int(), month=self.month_spin.get_value_as_int(), day=self.day_spin.get_value_as_int())
    
    def update_day_adj(self, widget):
        year = self.year_spin.get_value_as_int()
        month = self.month_spin.get_value_as_int()
        max_days = monthrange(year,month)[1]

        if self.day_spin.get_value_as_int() > max_days:
            self.day_spin.set_value(max_days)
        
        day_adjustment = Gtk.Adjustment(self.day_spin.get_value_as_int(), 1, max_days, 1, 1, 0)
        self.day_spin.configure(day_adjustment,1,0)

class Add_Mom_Dialog_Controller(object):
    def __init__(self):
        pass 
