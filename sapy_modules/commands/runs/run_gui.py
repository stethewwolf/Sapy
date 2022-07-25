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

from calendar import calendar
from datetime import date, datetime, timedelta
from distutils.command.build import build
from signal import signal
from traceback import print_tb
from sapy_modules.core import loms
from sapy_modules.core.moms import Mom
from sapy_modules.gui.gtk.dialogs import add_mom_dialog
from sapy_modules.utils import loggers as LoggerFactory
from sapy_modules.utils import config as SingleConfig
from sapy_modules.utils import constants as SapyConstants
from sapy_modules.utils import values as SapyValues
from sapy_modules.commands.command import Command
from sapy_modules.gui.gtk import Main_Window_View

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

global builder
global add_mom_flag 
global signal_handler

class RunGui(Command):
    short_arg = SapyConstants.COMMANDS.RUN_GUI.SHORT_ARG
    long_arg = SapyConstants.COMMANDS.RUN_GUI.LONG_ARG
    cmd_help = SapyConstants.COMMANDS.RUN_GUI.HELP
    cmd_type = SapyConstants.COMMANDS.RUN_GUI.TYPE
    cmd_action = SapyConstants.COMMANDS.RUN_GUI.ACTION

    def __init__(self, param):
        super().__init__()
        self.logger=LoggerFactory.getLogger(str( self.__class__ ))
        global builder
        global signal_handler
        global add_mom_flag
        add_mom_flag = False
        builder = Gtk.Builder()
        signal_handler = Handler()

    def run( self ):
        global builder
        global signal_handler
        builder.add_from_file("/home/stethewwolf/Projects/GitHub/stethewwolf/Sapy/sapy_modules/gui/gtk/glade/sapy.glade")
        builder.connect_signals(signal_handler)

        notebook = builder.get_object("sapyNotebooks")
        notebook.set_current_page(0)

        start_date = datetime.today()
        calendar = builder.get_object("sapyCalendar")
        calendar.select_day(start_date.day)
        calendar.select_month(start_date.month-1, start_date.year)
        end_date = start_date # + timedelta(days=1)

        momOccurredView = builder.get_object("movementsOccurredView")
        momOccurredView.append_column (
            Gtk.TreeViewColumn("id",Gtk.CellRendererText(), text=0)
        )
        momOccurredView.append_column (
            Gtk.TreeViewColumn("cause",Gtk.CellRendererText(), text=1)
        )
        momOccurredView.append_column (
            Gtk.TreeViewColumn("value",Gtk.CellRendererText(), text=2)
        )
        #renderToggleOccurred = Gtk.CellRendererToggle()
        #renderToggleOccurred.connect("toggled",signal_handler.onToggleCheckboxMom)
        #momOccurredView.append_column(Gtk.TreeViewColumn("sel",renderToggleOccurred, active=2))

        momOccurredStore = builder.get_object("movementsOccurredStore")
        for mom in loms.get_lom(name=SapyConstants.DB.OCCURRED_LIST_NAME).get_moms(start_date,end_date):
            momOccurredStore.append([mom.id, mom.cause, mom.value, False])

        momPlannedView = builder.get_object("movementsPlannedView")
        momPlannedView.append_column (
            Gtk.TreeViewColumn("id",Gtk.CellRendererText(), text=0)
        )
        momPlannedView.append_column (
            Gtk.TreeViewColumn("cause",Gtk.CellRendererText(), text=1)
        )
        momPlannedView.append_column (
            Gtk.TreeViewColumn("value",Gtk.CellRendererText(), text=2)
        )
        #renderTogglePlanned = Gtk.CellRendererToggle()
        #renderTogglePlanned.connect("toggled",signal_handler.onToggleCheckboxMom)
        #momPlannedView.append_column(Gtk.TreeViewColumn("sel",renderTogglePlanned, active=2))

        momPlannedStore = builder.get_object("movementsPlannedStore")
        for mom in loms.get_lom(name=SapyConstants.DB.PLANNED_LIST_NAME).get_moms(start_date,end_date):
            momPlannedStore.append([mom.id, mom.cause, mom.value, False])

        window = builder.get_object("sapyWindow")
        window.show_all()

        Gtk.main()

class Handler:

    def onDestroy(self, *args):
        global builder
        Gtk.main_quit()

    def onCalendarTabSelected(self, button):
        global builder
        notebook = builder.get_object("sapyNotebooks")
        notebook.set_current_page(0)

    def onGraphTabSelected(self, button):
        global builder
        notebook = builder.get_object("sapyNotebooks")
        notebook.set_current_page(1)

    def onDaySelected(self, button):
        global builder
        calendar = builder.get_object("sapyCalendar")
        start_date = datetime(calendar.get_date().year, calendar.get_date().month+1, calendar.get_date().day)
        end_date = start_date #+ timedelta(days=1)

        momOccurredStore = builder.get_object("movementsOccurredStore")
        momOccurredStore.clear()
        for mom in loms.get_lom(name=SapyConstants.DB.OCCURRED_LIST_NAME).get_moms(start_date,end_date):
            momOccurredStore.append([mom.id, mom.cause, mom.value ])

        momPlannedStore = builder.get_object("movementsPlannedStore")
        momPlannedStore.clear()
        for mom in loms.get_lom(name=SapyConstants.DB.PLANNED_LIST_NAME).get_moms(start_date,end_date):
            momPlannedStore.append([mom.id, mom.cause, mom.value ])

    def onAddPlannedSelected(self, button):
        global builder
        global add_mom_flag
        add_mom_flag = False
        mom_dialog = builder.get_object("momDialog")
        mom_date = builder.get_object("addMomDateEntry")
        mom_date.set_text( str(calendar.get_date().day) + " / " + str(calendar.get_date().month) + " / " + str(calendar.get_date().year))

        mom_dialog.run()
        mom_dialog.hide()

        if add_mom_flag:
            mom_date = builder.get_object("addMomDateEntry")
            mom_cause = builder.get_object("addMomCauseEntry")
            mom_value = builder.get_object("addMomValueEntry")

            date = datetime.strptime(mom_date.get_text(), '%d / %m / %Y')
            mom = Mom(
                value=float(mom_value.get_text()),
                cause=mom_cause.get_text(),
                year=date.year,
                month=date.month+1,
                day=date.day
                )

            planned_lom = loms.get_lom(name=SapyConstants.DB.PLANNED_LIST_NAME)
            planned_lom.add([mom])

            self.onDaySelected(None)

    def onAddOccurredSelected(self, button):
        global builder
        global add_mom_flag
        add_mom_dialog = False
        calendar = builder.get_object("sapyCalendar")
        mom_dialog = builder.get_object("momDialog")
        mom_date = builder.get_object("addMomDateEntry")
        mom_date.set_text( str(calendar.get_date().day) + " / " + str(calendar.get_date().month) + " / " + str(calendar.get_date().year))

        mom_dialog.run()
        mom_dialog.hide()

        if add_mom_flag:
            mom_date = builder.get_object("addMomDateEntry")
            mom_cause = builder.get_object("addMomCauseEntry")
            mom_value = builder.get_object("addMomValueEntry")

            date = datetime.strptime(mom_date.get_text(), '%d / %m / %Y')
            mom = Mom(
                value=float(mom_value.get_text()),
                cause=mom_cause.get_text(),
                year=date.year,
                month=date.month+1,
                day=date.day
                )

            occurred_lom = loms.get_lom(name=SapyConstants.DB.OCCURRED_LIST_NAME)
            occurred_lom.add([mom])
            self.onDaySelected(None)

    def onMomDialogApplayButton(self, widget):
        global builder
        global add_mom_flag
        add_mom_flag = True

        #TODO add here a chekc for the date value
        mom_dialog = builder.get_object("momDialog")
        mom_dialog.hide()

    def onMomDialogCancelButton(self, button):
        global builder
        mom_dialog = builder.get_object("momDialog")
        mom_dialog.hide()

    def onPlannedMomSelected(self, column, path, user_data):
        global builder
        momPlannedStore = builder.get_object("movementsPlannedStore")
        planned_lom = loms.get_lom(name=SapyConstants.DB.PLANNED_LIST_NAME)
        planned_mom = planned_lom.get_mom(id=momPlannedStore[path][0])

        mom_date = builder.get_object("addMomDateEntry")
        mom_date.set_text(                      \
            str(planned_mom.time.day) +  \
            " / " + str(planned_mom.time.month) + \
            " / " + str(planned_mom.time.year))

        mom_cause = builder.get_object("addMomCauseEntry")
        mom_cause.set_text(planned_mom.cause)
        mom_value = builder.get_object("addMomValueEntry")
        mom_value.set_text(str(planned_mom.value))

        mom_dialog = builder.get_object("momDialog")

        mom_dialog.run()
        mom_dialog.hide()

        date = datetime.strptime(mom_date.get_text(), '%d / %m / %Y')
        planned_mom.update(
                new_value=float(mom_value.get_text()),
                new_cause=mom_cause.get_text(),
                new_year=date.year,
                new_month=date.month,
                new_day=date.day
                )
        self.onDaySelected(None)

    def onOccurredMomSelected(self, column, path, user_data):
        global builder
        momOccurredStore = builder.get_object("movementsOccurredStore")
        occurred_lom = loms.get_lom(name=SapyConstants.DB.OCCURRED_LIST_NAME)
        occurred_mom = occurred_lom.get_mom(id=momOccurredStore[path][0])
        mom_date = builder.get_object("addMomDateEntry")
        mom_date.set_text(                      \
            str(occurred_mom.time.day) +  \
            " / " + str(occurred_mom.time.month) + \
            " / " + str(occurred_mom.time.year))

        mom_cause = builder.get_object("addMomCauseEntry")
        mom_cause.set_text(occurred_mom.cause)
        mom_value = builder.get_object("addMomValueEntry")
        mom_value.set_text(str(occurred_mom.value))

        mom_dialog = builder.get_object("momDialog")

        mom_dialog.run()
        mom_dialog.hide()

        date = datetime.strptime(mom_date.get_text(), '%d / %m / %Y')
        occurred_mom.update(
                new_value=float(mom_value.get_text()),
                new_cause=mom_cause.get_text(),
                new_year=date.year,
                new_month=date.month,
                new_day=date.day
                )
        self.onDaySelected(None)

    #def onToggleChecksoxMom(self, widget, stuff):
    #    pass
