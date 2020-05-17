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
#

import gi, datetime
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sapy_modules.sapy import moms

class Add_Mom_Dialog_View(Gtk.MessageDialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "add new mom", parent, 0,
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
                2, 1
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
                2, 1
                )
        
        date_label = Gtk.Label("Date")
        self.date_entry = Gtk.Entry()
        self.date_entry.set_placeholder_text("dd/mm/yyyy")

        grid.attach_next_to(
                date_label, 
                cause_label, 
                Gtk.PositionType.BOTTOM, 
                1, 1
                )

        grid.attach_next_to( 
                self.date_entry,
                date_label, 
                Gtk.PositionType.RIGHT, 
                2, 1
                )
 
        box.add(grid)
        self.show_all()

    def get_mom(self):
        raw_cause =  self.cause_entry.get_text()
        raw_value = float(self.value_button.get_value())

        if len(self.date_entry.get_text().split("/")) == 3:
            raw_year = self.date_entry.get_text().split("/")[2]
            raw_month = self.date_entry.get_text().split("/")[1]
            raw_day = self.date_entry.get_text().split("/")[0]
            new_mom = moms.Mom(cause=raw_cause, value=raw_value, year=raw_year, month=raw_month, day=raw_day)
        else:
            new_mom = moms.Mom(cause=raw_cause, value=raw_value)
        
        return new_mom


class Add_Mom_Dialog_Controller(object):
    def __init__(self):
        #TODO: only one lom is selected per time, when you selcet one, other
        #       are deselected
        pass 
