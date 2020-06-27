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
import sapy_modules.sapy.mom as moms
import sapy_modules.sapy.lom as loms

import matplotlib as mp
from matplotlib.figure import Figure
from numpy import arange, pi, random, linspace
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

class Plot_Graph_Dialog_View(Gtk.MessageDialog):
    def __init__(self, parent):
        Gtk.MessageDialog.__init__(
                self,
                parent,
                0,
                Gtk.MessageType.INFO,
                Gtk.ButtonsType.OK,
                "Graph",
               )

        self.set_default_size(150, 100)
        self.parent = parent
        box = self.get_content_area()

        fig = Figure(figsize=(5,5), dpi=100)
        ax = fig.add_subplot(111)

        sd = self.parent.controller.start_date
        ed = self.parent.controller.end_date

        for lom in loms.get_loms():
            graph_data = lom.balance_per_day(start_date=sd,end_date=ed)
            ax.scatter(mp.dates.date2num(graph_data[0]), graph_data[1], label=lom.name, marker="_")

        ax.set_xlim(sd,ed)

        fig.autofmt_xdate()
        fig.legend()
        ax.plot()

        canvas = FigureCanvas(fig)
        canvas.set_size_request(400,400)

        box.add(canvas) 
        self.show_all()

class Plot_Graph_Dialog_Controller(object):
    def __init__(self):
        #TODO: only one lom is selected per time, when you selcet one, other
        #       are deselected
        pass 
