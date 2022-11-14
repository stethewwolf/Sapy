# Sapy
# Copyright (C) 2018 stefano prina <stethewwolf@posteo.net>
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

from calendar import calendar
from datetime import date, datetime, timedelta
from distutils.command.build import build
from signal import signal
from traceback import print_tb
from sapy_modules.core import loms
from sapy_modules.core.moms import Mom
from sapy_modules.core import profiles
from sapy_modules.utils import loggers as LoggerFactory
from sapy_modules.utils import config as SingleConfig
from sapy_modules.utils import constants as SapyConstants
from sapy_modules.utils import values as SapyValues
from sapy_modules.commands.command import Command
from sapy_modules.gui.gtk.gtk_handlers import GuiData
from sapy_modules.gui.gtk.gtk_handlers import Handler
import calendar as clndr
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
import matplotlib as mp
import os
from pathlib import Path
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class RunGui(Command):
    short_arg = SapyConstants.COMMANDS.RUN_GUI.SHORT_ARG
    long_arg = SapyConstants.COMMANDS.RUN_GUI.LONG_ARG
    cmd_help = SapyConstants.COMMANDS.RUN_GUI.HELP
    cmd_type = SapyConstants.COMMANDS.RUN_GUI.TYPE
    cmd_action = SapyConstants.COMMANDS.RUN_GUI.ACTION

    def __init__(self, param):
        super().__init__()
        self.logger=LoggerFactory.getLogger(str( self.__class__ ))
        self.gui_builder = Gtk.Builder()
        self.signal_handler = Handler(GuiData(), self.gui_builder)

    def run( self ):
        run_gui_file = Path(__file__)
        sapy_modules_folder = run_gui_file.parents[2]
        glade_file = os.path.join(sapy_modules_folder,'gui/gtk/sapy.glade')
        self.gui_builder.add_from_file(glade_file)
        self.gui_builder.connect_signals(self.signal_handler)

        notebook = self.gui_builder.get_object("sapyNotebooks")
        notebook.set_current_page(0)

        momOccurredView = self.gui_builder.get_object("movementsOccurredView")
        momOccurredView.append_column (
            Gtk.TreeViewColumn("id",Gtk.CellRendererText(), text=0)
        )
        occurred_date_column = Gtk.TreeViewColumn("date",Gtk.CellRendererText(), text=1)
        occurred_date_column.set_sort_column_id(1)
        momOccurredView.append_column (occurred_date_column)
        momOccurredView.append_column (
            Gtk.TreeViewColumn("value",Gtk.CellRendererText(), text=2)
        )
        momOccurredView.append_column (
            Gtk.TreeViewColumn("cause",Gtk.CellRendererText(), text=3)
        )

        momPlannedView = self.gui_builder.get_object("movementsPlannedView")
        momPlannedView.append_column (
            Gtk.TreeViewColumn("id",Gtk.CellRendererText(), text=0)
        )
        planned_date_column = Gtk.TreeViewColumn("date",Gtk.CellRendererText(), text=1)
        planned_date_column.set_sort_column_id(1)
        momPlannedView.append_column (planned_date_column)
        momPlannedView.append_column (
            Gtk.TreeViewColumn("value",Gtk.CellRendererText(), text=2)
        )
        momPlannedView.append_column (
            Gtk.TreeViewColumn("cause",Gtk.CellRendererText(), text=3)
        )

        window = self.gui_builder.get_object("sapyWindow")
        window.show_all()

        self.signal_handler.start_date = datetime.today().date()
        self.signal_handler.gui_data.day = self.signal_handler.start_date.day
        self.signal_handler.gui_data.month = self.signal_handler.start_date.month
        self.signal_handler.gui_data.year = self.signal_handler.start_date.year
        #calendar = self.gui_builder.get_object("sapyCalendar")
        #calendar.select_day(self.signal_handler.start_date.day)
        #calendar.select_month(self.signal_handler.start_date.month-1, self.signal_handler.start_date.year)
        self.signal_handler.end_date = self.signal_handler.start_date # + timedelta(days=1)
        #self.signal_handler.updateMomStoreContent(self.signal_handler.start_date.date(), self.signal_handler.end_date.date())

        self.signal_handler.gui_data.fig = Figure(figsize=(5,5), dpi=100)
        self.signal_handler.gui_data.ax = self.signal_handler.gui_data.fig.add_subplot(111)
        canvas = FigureCanvas(self.signal_handler.gui_data.fig)
        canvas.set_size_request(400,400)
        d_area = self.gui_builder.get_object("GraphTab")
        d_area.pack_start(canvas, True, True, 10)
        d_area.show_all()

        active_profile_label = self.gui_builder.get_object("ActiveProfileLabel")
        default_profile_id = profiles.get_default_profile_id()
        self.signal_handler.gui_data.active_profile = profiles.get_profile(id=default_profile_id)

        active_profile_label.set_text(self.signal_handler.gui_data.active_profile.name)

        profilesListView = self.gui_builder.get_object("profilesListView")
        profilesListView.append_column (
            Gtk.TreeViewColumn("id",Gtk.CellRendererText(), text=0)
        )
        profilesListView.append_column (
            Gtk.TreeViewColumn("name",Gtk.CellRendererText(), text=1)
        )

        self.signal_handler.updateProfilesPopUpMenu()

        self.signal_handler.updateMomStoreContent()

        calendar = self.gui_builder.get_object("sapyCalendar")
        calendar.select_day(self.signal_handler.start_date.day)
        calendar.select_month(self.signal_handler.start_date.month-1, self.signal_handler.start_date.year)

        Gtk.main()
