#
#   File : add_mom_dialog.py
#   Author : stefano prina <stethewwolf@gmail.com>
#


import gi, datetime
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import sapy_modules.sapy.mom as moms


class add_mom_dialog_view(Gtk.MessageDialog):
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


class add_mom_dialog_controller(object):
    def __init__(self):
        #TODO: only one lom is selected per time, when you selcet one, other
        #       are deselected
        pass 
