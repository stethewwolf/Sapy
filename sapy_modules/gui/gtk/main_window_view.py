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
from sapy_modules.gui.gtk.main_window_toolbar import Sapy_Main_Toolbar
from sapy_modules.gui.gtk.dialogs import Date_Picker


class Main_Window_View(Gtk.Window):
    def __init__(self, controller):
        Gtk.Window.__init__(self)
        self.show_all()
        self.connect("destroy", Gtk.main_quit)
        self.controller = controller
        self.controller.view = self

        # main window features
        self.tite = "Sapy"
        self.resize(400, 600)

        # first level box
        external_box = Gtk.VBox()
        self.add(external_box)


        # menu buttons
        external_box.pack_start(Sapy_Main_Toolbar(self), False, False, 10)

        # dates row
        box = Gtk.HBox()
        dates_grid = Gtk.Grid()
        box.set_center_widget(dates_grid)
        start_date_label = Gtk.Label("Start Date")

        end_date_label = Gtk.Label("End Date")

        end_date_button = Gtk.Button(self.controller.end_date.strftime('%d-%m-%Y'))
        start_date_button = Gtk.Button(self.controller.start_date.strftime('%d-%m-%Y'))

        start_date_button.connect("clicked",self.clicked_start_date_button)
        end_date_button.connect("clicked",self.clicked_end_date_button)

        dates_grid.add(start_date_label)
        dates_grid.attach_next_to(start_date_button,start_date_label, Gtk.PositionType.BOTTOM, 1,2)

        dates_grid.attach_next_to(end_date_label,start_date_label, Gtk.PositionType.RIGHT, 1,1)

        dates_grid.attach_next_to(end_date_button,end_date_label, Gtk.PositionType.BOTTOM, 2,2)

        external_box.pack_start(box, False, False, 10)

        # list name row
        self.list_label = Gtk.Label("List")
        external_box.pack_start(self.list_label,False,False,5)
       
        # lom pane
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.tree = Gtk.TreeView(self.controller.moms_store)
        self.tree.append_column (
            Gtk.TreeViewColumn("id",Gtk.CellRendererText(), text=0)
        )
        self.tree.append_column (
            Gtk.TreeViewColumn("cause",Gtk.CellRendererText(), text=1)
        )
        self.tree.append_column (
            Gtk.TreeViewColumn("value",Gtk.CellRendererText(), text=2)
        )
        self.tree.append_column (
            Gtk.TreeViewColumn("date",Gtk.CellRendererText(), text=3)
        )

        render_toggle = Gtk.CellRendererToggle()
        render_toggle.connect("toggled",self.toggle_checkbox_mom)
        self.tree.append_column(Gtk.TreeViewColumn("",render_toggle, active=4))

        scrolled_window.add(self.tree)
        external_box.pack_start(scrolled_window,True,True,10)

        # balance row
        grid = Gtk.Grid()

        balance_date_label = Gtk.Label("Balance Date")

        balance_valuelabel_label = Gtk.Label("Balance Value")

        balance_date_button = Gtk.Button(self.controller.date.strftime('%d-%m-%Y'))
        self.balance_value_label = Gtk.Label(self.controller.balance_value)

        balance_date_button.connect("clicked",self.clicked_balance_date_button)

        grid.add(balance_date_label)
        grid.attach_next_to(balance_date_button, balance_date_label, Gtk.PositionType.BOTTOM, 1,2)

        grid.attach_next_to(balance_valuelabel_label, balance_date_label, Gtk.PositionType.RIGHT, 1,1)

        grid.attach_next_to(self.balance_value_label, balance_valuelabel_label, Gtk.PositionType.BOTTOM, 2,2)

        external_box.pack_end(grid, False, True, 10)
 
    def toggle_checkbox_mom(self, widget, path):
        self.controller.moms_store[path][4] = not self.controller.moms_store[path][4]

    def clicked_start_date_button(self, widget):
        date_picker = Date_Picker(self)
        date_picker.set_date(self.controller.start_date)
        
        if date_picker.run() == Gtk.ResponseType.OK:
            self.controller.start_date = date_picker.get_date()
            widget.set_label(self.controller.start_date.strftime('%d-%m-%Y'))
            self.controller.rebuild_list()

        date_picker.destroy()

    def clicked_end_date_button(self, widget):
        date_picker = Date_Picker(self)
        date_picker.set_date(self.controller.end_date)
        
        if date_picker.run() == Gtk.ResponseType.OK:
            self.controller.end_date = date_picker.get_date()
            widget.set_label(self.controller.end_date.strftime('%d-%m-%Y'))
            self.controller.rebuild_list()

        date_picker.destroy()

    def clicked_balance_date_button(self, widget):
        date_picker = Date_Picker(self)
        date_picker.set_date(self.controller.end_date)
        
        if date_picker.run() == Gtk.ResponseType.OK:
            self.controller.date = date_picker.get_date()
            widget.set_label(self.controller.date.strftime('%d-%m-%Y'))
            self.controller.calc_balance()

        date_picker.destroy()

    def main(self):
        self.show_all()
        Gtk.main()