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
from sapy_modules.gui.gtk.widgets import Home_Page_Toolbar
import sapy_modules.core.moms as moms
import sapy_modules.core.loms as loms
import matplotlib as mp
import datetime
from matplotlib.figure import Figure
from numpy import arange, pi, random, linspace
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas


class Home_Page(Gtk.VBox):
    """docstring for Graph_Page"""
    def __init__(self, parent):
        super(Home_Page, self).__init__()
        self.gtkWindow = parent
        self.controller = Home_Page_Controller(self)

        self.set_border_width(10)
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

        self.pack_start(box,True,True,10)

        self.controller.update_loms()

        self.fig = Figure(figsize=(5,5), dpi=100)

        #fig.legend()
        self.ax = self.fig.add_subplot(111)
        canvas = FigureCanvas(self.fig)
        canvas.set_size_request(400,400)
        self.pack_start(canvas, True, True, 10)

        self.controller.update_plot()

        #list pane
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.tree = Gtk.TreeView(self.controller.lists_store)

        render_toggle = Gtk.CellRendererToggle()
        render_toggle.connect("toggled",self.controller.toggle_selected_list)
        self.tree.append_column(Gtk.TreeViewColumn("sel",render_toggle, \
                                                   active=0))

        self.tree.append_column (
            Gtk.TreeViewColumn("id",Gtk.CellRendererText(), text=1)
        )

        self.tree.append_column (
            Gtk.TreeViewColumn("name",Gtk.CellRendererText(), text=2)
        )

        render_toggle = Gtk.CellRendererToggle()
        render_toggle.connect("toggled",self.controller.toggle_visible_list)
        self.tree.append_column(Gtk.TreeViewColumn("visible",render_toggle,\
                                                   active=3))

        self.tree.append_column (
            Gtk.TreeViewColumn("color",Gtk.CellRendererText(), text=4)
        )

        scrolled_window.add(self.tree)

        self.pack_start(scrolled_window,True,True,10)

        button_box = Home_Page_Toolbar(self)
        self.pack_start(button_box,False,False,10)


class Home_Page_Controller(object):
    """docstring for Graph_Page_Controller"""
    def __init__(self, view):
        super(Home_Page_Controller, self).__init__()
        self.view = view
        self.lists_store = Gtk.ListStore(bool, int, str, bool, str) # name, is visible

        self.start_date = (datetime.datetime.today().date() - datetime.timedelta(days=15)) # start date
        self.end_date = (datetime.datetime.today().date() + datetime.timedelta(days=15))   # end date

    def update_plot(self):
        self.view.ax.clear()

        for lom in loms.get_loms():
            if lom.visible:
                graph_data = lom.balance_per_day(start_date=self.start_date,end_date=self.end_date)
                self.view.ax.scatter(mp.dates.date2num(graph_data[0]), graph_data[1], label=lom.name, marker="_", color=lom.color)

        self.view.ax.set_xlim(self.start_date, self.end_date)

        self.view.ax.plot()

        self.view.fig.autofmt_xdate()

    def update_loms(self):
        self.lists_store.clear()
        for lom in loms.get_loms():
            self.lists_store.append([False, lom.id, lom.name, lom.visible, lom.color])

    def clicked_start_date_button(self, widget):
        date_picker = Date_Picker(self.view.gtkWindow)
        date_picker.set_date(self.start_date)

        if date_picker.run() == Gtk.ResponseType.OK:
            self.start_date = date_picker.get_date()
            widget.set_label(self.start_date.strftime('%d-%m-%Y'))

        date_picker.destroy()
        self.update_plot()

    def clicked_end_date_button(self, widget):
        date_picker = Date_Picker(self.view.gtkWindow)
        date_picker.set_date(self.end_date)

        if date_picker.run() == Gtk.ResponseType.OK:
            self.end_date = date_picker.get_date()
            widget.set_label(self.end_date.strftime('%d-%m-%Y'))

        date_picker.destroy()
        self.update_plot()

    def toggle_visible_list(self, widget, path):
        self.lists_store[path][3] = not self.lists_store[path][3]
        lom = loms.get_lom(id=self.lists_store[path][1])

        lom.set_visible(self.lists_store[path][3])

        self.update_plot()

    def toggle_selected_list(self, widget, path):
       self.lists_store[path][0] = not self.lists_store[path][0]

    def add_lom_tab(self, lom):
        self.view.gtkWindow.controller.add_lom_page(lom)

    def del_lom(self):
        for lom_row in self.lists_store:
            if lom_row[0]:
                del_lom = loms.get_lom(id=lom_row[1])

                if del_lom:
                    self.view.gtkWindow.controller.remove_lom_page(del_lom.name)
                    del_lom.delete()

                self.lists_store.remove(lom_row.iter)

    def has_lom_selected(self):
        for lom_row in self.lists_store:
            if lom_row[0]:
                return True

        return False
