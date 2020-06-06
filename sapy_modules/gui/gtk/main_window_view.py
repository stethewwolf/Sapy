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


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sapy_modules.gui.gtk.main_window_toolbar import Sapy_Main_Toolbar


class Main_Window_View(Gtk.Window):
    def __init__(self, controller):
        Gtk.Window.__init__(self)
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        self.controller = controller
        self.controller.view = self

        # main window features
        self.tite = "Sapy"
        self.resize(400, 600)

        # main container
        self.main_listbox = Gtk.ListBox()

        # menu button row
        row = Gtk.ListBoxRow()

        row.add(Sapy_Main_Toolbar(self))

        self.main_listbox.add(row)

        # calendar row
        row = Gtk.ListBoxRow()
        self.list_label = Gtk.Label("List")

        #self.calendar = Gtk.Calendar()
        #self.connect("button-press-event",self.controller.rebuild_list)
        #self.connect("month-changed",self.controller.rebuild_list)
        #self.connect("day-changed",self.controller.rebuild_list)
        row.add(self.list_label)



        self.main_listbox.add(row)

        # lom panes row
        row = Gtk.ListBoxRow()
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

        row.add(self.tree)

        self.main_listbox.add(row)

        self.add(self.main_listbox)

    def toggle_checkbox_mom(self, widget, path):
        self.controller.moms_store[path][4] = not self.controller.moms_store[path][4]

    def main(self):
        self.show_all()
        Gtk.main()
    
