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

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sapy_modules.gui.gtk.dialogs import Date_Picker
from sapy_modules.gui.gtk.widgets import Lom_Page_Toolbar
import sapy_modules.core.moms as moms
import datetime


class Lom_Page(Gtk.VBox):
    def __init__(self, parent, lom, update_plot_callback):
        Gtk.VBox.__init__(self)

        self.controller = Lom_Page_Controller(self, lom, update_plot_callback)
        self.gtkWindow = parent

        # dates row
        box = Gtk.HBox()
        dates_grid = Gtk.Grid()
        box.set_center_widget(dates_grid)
        start_date_label = Gtk.Label("Start Date")

        end_date_label = Gtk.Label("End Date")

        end_date_button = Gtk.Button(self.controller.end_date.strftime('%d-%m-%Y'))
        start_date_button = Gtk.Button(self.controller.start_date.strftime('%d-%m-%Y'))

        start_date_button.connect("clicked",self.controller.clicked_start_date_button)
        end_date_button.connect("clicked",self.controller.clicked_end_date_button)

        dates_grid.add(start_date_label)
        dates_grid.attach_next_to(start_date_button,start_date_label, Gtk.PositionType.BOTTOM, 1,2)

        dates_grid.attach_next_to(end_date_label,start_date_label, Gtk.PositionType.RIGHT, 1,1)

        dates_grid.attach_next_to(end_date_button,end_date_label, Gtk.PositionType.BOTTOM, 2,2)

        self.pack_start(box, False, False, 10)

        # lom pane
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.tree = Gtk.TreeView(self.controller.moms_store)

        render_toggle = Gtk.CellRendererToggle()
        render_toggle.connect("toggled",self.toggle_checkbox_mom)
        self.tree.append_column(Gtk.TreeViewColumn("sel",render_toggle, active=0))

        self.tree.append_column (
            Gtk.TreeViewColumn("id",Gtk.CellRendererText(), text=1)
        )

        self.tree.append_column (
            Gtk.TreeViewColumn("date",Gtk.CellRendererText(), text=2)
        )

        self.tree.append_column (
            Gtk.TreeViewColumn("value",Gtk.CellRendererText(), text=3)
        )

        self.tree.append_column (
            Gtk.TreeViewColumn("cause",Gtk.CellRendererText(), text=4)
        )

        scrolled_window.add(self.tree)
        self.pack_start(scrolled_window,True,True,10)

        self.pack_start(Lom_Page_Toolbar(self),False,False,10)

        # balance row
        grid = Gtk.Grid()

        balance_date_label = Gtk.Label("Balance Date")

        balance_valuelabel_label = Gtk.Label("Balance Value")

        balance_date_button = Gtk.Button(self.controller.balance_date.strftime('%d-%m-%Y'))
        self.balance_value_label = Gtk.Label(self.controller.balance_value)

        balance_date_button.connect("clicked",self.controller.clicked_balance_date_button)

        grid.add(balance_date_label)
        grid.attach_next_to(balance_date_button, balance_date_label, Gtk.PositionType.BOTTOM, 1,2)

        grid.attach_next_to(balance_valuelabel_label, \
                            balance_date_label, Gtk.PositionType.RIGHT, 1,1)

        grid.attach_next_to(self.balance_value_label, \
                            balance_valuelabel_label, Gtk.PositionType.BOTTOM, 2,2)

        self.pack_end(grid, False, True, 10)


        self.controller.calc_balance()
        self.controller.update_lom_list()

    def toggle_checkbox_mom(self, widget, path):
        self.controller.moms_store[path][0] = not \
                self.controller.moms_store[path][0]


class Lom_Page_Controller(object):
    """docstring for Lom_Page_Controller"""
    def __init__(self, view, lom, update_plot_callback):
        self.view = view
        self.lom = lom
        self.update_plot = update_plot_callback

        self.start_date = (datetime.datetime.today().date() - datetime.timedelta(days=15)) # start date
        self.end_date = (datetime.datetime.today().date() + datetime.timedelta(days=15))   # end date
        self.balance_date = datetime.datetime.today().date()

        self.balance_value = 0

        self.moms_store = Gtk.ListStore(bool, int, str, float, str) # id cause, value, date

    def clicked_start_date_button(self, widget):
        date_picker = Date_Picker(self.view.gtkWindow)
        date_picker.set_date(self.start_date)
        if date_picker.run() == Gtk.ResponseType.OK:
            self.start_date = date_picker.get_date()
            widget.set_label(self.start_date.strftime('%d-%m-%Y'))

        date_picker.destroy()
        self.update_lom_list()

    def clicked_end_date_button(self, widget):
        date_picker = Date_Picker(self.view.gtkWindow)
        date_picker.set_date(self.end_date)

        if date_picker.run() == Gtk.ResponseType.OK:
            self.end_date = date_picker.get_date()
            widget.set_label(self.end_date.strftime('%d-%m-%Y'))

        date_picker.destroy()
        self.update_lom_list()

    def clicked_balance_date_button(self, widget):
        date_picker = Date_Picker(self.view.gtkWindow)
        date_picker.set_date(self.balance_date)

        if date_picker.run() == Gtk.ResponseType.OK:
            self.balance_date = date_picker.get_date()
            widget.set_label(self.balance_date.strftime('%d-%m-%Y'))
            self.calc_balance()

        date_picker.destroy()

    def calc_balance(self):
        self.balance_value = self.lom.balance(end_date=self.balance_date)

        self.view.balance_value_label.set_label(str(round(self.balance_value,2)))

    def update_lom_list(self):
        moms_list = self.lom.get_moms(start_date=self.start_date, end_date=self.end_date)

        self.moms_store.clear()

        moms_list.sort(key=moms.date_key)
        if len(moms_list) != 0:
            for mom in moms_list:
                self.moms_store.append([False, mom.id, mom.time.strftime('%d-%m-%Y'), mom.value, mom.cause])

        # todo : trigger update plot
        self.update_plot()



    def add_mom(self, mom):
        self.lom.add([mom])
        self.update_lom_list()

    def del_mom(self):
        for mom_row in self.moms_store:
            if mom_row[0]:
                del_mom = self.lom.get_mom(mom_row[1])

                if del_mom:
                    del_mom.delete()

        self.update_lom_list()

    def has_mom_selected(self):
        for mom_row in self.moms_store:
            if mom_row[0]:
                mom_selected = self.lom.get_mom(mom_row[1])
                return True

        return False
