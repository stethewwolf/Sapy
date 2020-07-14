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
import sapy_modules.sapy.mom as moms
import sapy_modules.sapy.lom as loms
import matplotlib as mp
import datetime
from matplotlib.figure import Figure
from numpy import arange, pi, random, linspace
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas


class Graph_Page(Gtk.VBox):
    """docstring for Graph_Page"""
    def __init__(self, parent):
        super(Graph_Page, self).__init__()
        self.parent = parent
        self.controller = Graph_Page_Controller(self)

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

        self.pack_start(box, False, False, 10)


        self.controller.update_loms()
        
        self.fig = Figure(figsize=(5,5), dpi=100)
        
        #fig.legend()
        self.ax = self.fig.add_subplot(111)
        canvas = FigureCanvas(self.fig)
        canvas.set_size_request(400,400)
        self.pack_start(canvas, True, True, 10)

        self.controller.update_plot()

        



class Graph_Page_Controller(object):
    """docstring for Graph_Page_Controller"""
    def __init__(self, view):
        super(Graph_Page_Controller, self).__init__()
        self.view = view

        self.start_date = (datetime.datetime.today().date() - datetime.timedelta(days=15)) # start date
        self.end_date = (datetime.datetime.today().date() + datetime.timedelta(days=15))   # end date

        self.loms = loms.get_loms()

    def update_plot(self):
        self.view.ax.clear()        

        for lom in self.loms:
            graph_data = lom.balance_per_day(start_date=self.start_date,end_date=self.end_date)
            self.view.ax.scatter(mp.dates.date2num(graph_data[0]), graph_data[1], label=lom.name, marker="_")

        self.view.ax.set_xlim(self.start_date, self.end_date)
        

        self.view.ax.plot()

        self.view.fig.autofmt_xdate()

    def update_loms(self):
        self.loms = loms.get_loms()

    def clicked_start_date_button(self, widget):
        date_picker = Date_Picker(self.view.parent)
        date_picker.set_date(self.start_date)
        
        if date_picker.run() == Gtk.ResponseType.OK:
            self.start_date = date_picker.get_date()
            widget.set_label(self.start_date.strftime('%d-%m-%Y'))

        date_picker.destroy()
        self.update_plot()

    def clicked_end_date_button(self, widget):
        date_picker = Date_Picker(self.view.parent)
        date_picker.set_date(self.end_date)
        
        if date_picker.run() == Gtk.ResponseType.OK:
            self.end_date = date_picker.get_date()
            widget.set_label(self.end_date.strftime('%d-%m-%Y'))

        date_picker.destroy()
        self.update_plot()


                        