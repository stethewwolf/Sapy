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
import calendar as clndr

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
        self.gui_builder.add_from_file("/home/stethewwolf/Progetti/GtkApplications/Sapy/sapy_modules/gui/gtk/glade/sapy.glade")
        self.gui_builder.connect_signals(self.signal_handler)

        notebook = self.gui_builder.get_object("sapyNotebooks")
        notebook.set_current_page(0)

        momOccurredView = self.gui_builder.get_object("movementsOccurredView")
        momOccurredView.append_column (
            Gtk.TreeViewColumn("id",Gtk.CellRendererText(), text=0)
        )
        momOccurredView.append_column (
            Gtk.TreeViewColumn("cause",Gtk.CellRendererText(), text=1)
        )
        momOccurredView.append_column (
            Gtk.TreeViewColumn("value",Gtk.CellRendererText(), text=2)
        )

        momPlannedView = self.gui_builder.get_object("movementsPlannedView")
        momPlannedView.append_column (
            Gtk.TreeViewColumn("id",Gtk.CellRendererText(), text=0)
        )
        momPlannedView.append_column (
            Gtk.TreeViewColumn("cause",Gtk.CellRendererText(), text=1)
        )
        momPlannedView.append_column (
            Gtk.TreeViewColumn("value",Gtk.CellRendererText(), text=2)
        )

        window = self.gui_builder.get_object("sapyWindow")
        window.show_all()

        self.signal_handler.start_date = datetime.today().date()
        self.signal_handler.gui_data.day = self.signal_handler.start_date.day
        self.signal_handler.gui_data.month = self.signal_handler.start_date.month
        self.signal_handler.gui_data.year = self.signal_handler.start_date.year
        calendar = self.gui_builder.get_object("sapyCalendar")
        calendar.select_day(self.signal_handler.start_date.day)
        calendar.select_month(self.signal_handler.start_date.month-1, self.signal_handler.start_date.year)
        self.signal_handler.end_date = self.signal_handler.start_date # + timedelta(days=1)
        #self.signal_handler.updateMomStoreContent(self.signal_handler.start_date.date(), self.signal_handler.end_date.date())
        self.signal_handler.updateMomStoreContent()

        Gtk.main()

class GuiData():
    def __init__(self):
        self.year = 1900
        self.month = 1
        self.day = 1
        self.month_name = "Gen"
        self.add_mom_flag = False
        self.mom = None
        self.start_date = datetime.today().date()
        self.end_date = datetime.today().date()

class Handler:
    def __init__(self, gui_data:GuiData, gui_builder):
        self.logger=LoggerFactory.getLogger(str( self.__class__ ))
        self.gui_data = gui_data
        self.gui_builder  = gui_builder

    def onDestroy(self, *args):
        Gtk.main_quit()

    def onCalendarTabSelected(self, button):
        notebook = self.gui_builder.get_object("sapyNotebooks")
        notebook.set_current_page(0)

    def onGraphTabSelected(self, button):
        notebook = self.gui_builder.get_object("sapyNotebooks")
        notebook.set_current_page(1)

    def onDaySelected(self, button):
        calendar = self.gui_builder.get_object("sapyCalendar")
        self.gui_data.start_date = datetime(calendar.get_date().year, calendar.get_date().month+1, calendar.get_date().day)
        self.gui_data.end_date = self.gui_data.start_date #+ timedelta(days=1)
        #self.updateMomStoreContent(start_date.date(), end_date.date())
        self.updateMomStoreContent()

    def onYearMonthViewSelected(self, spinButton):
        self.gui_data.year = int(spinButton.get_value())
        self.gui_data.start_date = datetime(self.gui_data.year, self.gui_data.month, 1)
        self.gui_data.end_date = datetime(self.gui_data.year, self.gui_data.month, clndr.monthrange(self.gui_data.year, self.gui_data.month)[1])
        #self.updateMomStoreContent(start_date, end_date)
        self.updateMomStoreContent()

    def onMonthSelected(self, button):
        month_name = button.get_label()
        self.gui_data.month = 0
        if month_name == "Gen":
            self.gui_data.month = 1
        elif month_name == "Feb":
            self.gui_data.month = 2
        elif month_name == "Mar":
            self.gui_data.month = 3
        elif month_name == "Apr":
            self.gui_data.month = 4
        elif month_name == "May":
            self.gui_data.month = 5
        elif month_name == "Jun":
            self.gui_data.month = 6
        elif month_name == "Jul":
            self.gui_data.month = 7
        elif month_name == "Aug":
            self.gui_data.month = 8
        elif month_name == "Sep":
            self.gui_data.month = 9
        elif month_name == "Oct":
            self.gui_data.month = 10
        elif month_name == "Nov":
            self.gui_data.month = 11
        elif month_name == "Dec":
            self.gui_data.month = 12

        if self.gui_data.month != 0:
            self.gui_data.start_date = datetime(self.gui_data.year, self.gui_data.month, 1)
            self.gui_data.end_date = datetime(self.gui_data.year, self.gui_data.month, clndr.monthrange(self.gui_data.year, self.gui_data.month)[1])
            self.updateMomStoreContent()

    def onAddPlannedSelected(self, button):
        mom_dialog = self.gui_builder.get_object("momDialog")
        mom_date = self.gui_builder.get_object("addMomDateEntry")
        calendar = self.gui_builder.get_object("sapyCalendar")
        mom_date.set_text( str(calendar.get_date().day) + " / " + str(calendar.get_date().month) + " / " + str(calendar.get_date().year))

        mom_dialog.run()
        mom_dialog.hide()

        if self.gui_data.add_mom_flag:
            mom_date = self.gui_builder.get_object("addMomDateEntry")
            mom_cause = self.gui_builder.get_object("addMomCauseEntry")
            mom_value = self.gui_builder.get_object("addMomValueEntry")

            date = datetime.strptime(mom_date.get_text(), '%d / %m / %Y')
            mom = Mom(
                value=float(mom_value.get_text().replace(",", ".")),
                cause=mom_cause.get_text(),
                year=date.year,
                month=date.month+1,
                day=date.day
                )

            planned_lom = loms.get_lom(name=SapyConstants.DB.PLANNED_LIST_NAME)
            planned_lom.add([mom])

            self.updateMomStoreContent()
        print("closing dialog add occurred mom")

    def onAddOccurredSelected(self, button):
        self.gui_data.add_mom_flag = False
        calendar = self.gui_builder.get_object("sapyCalendar")
        mom_dialog = self.gui_builder.get_object("momDialog")
        mom_date = self.gui_builder.get_object("addMomDateEntry")
        mom_date.set_text( str(calendar.get_date().day) + " / " + str(calendar.get_date().month) + " / " + str(calendar.get_date().year))

        mom_dialog.run()
        mom_dialog.hide()

        if self.gui_data.add_mom_flag:
            mom_date = self.gui_builder.get_object("addMomDateEntry")
            mom_cause = self.gui_builder.get_object("addMomCauseEntry")
            mom_value = self.gui_builder.get_object("addMomValueEntry")

            date = datetime.strptime(mom_date.get_text(), '%d / %m / %Y')
            mom = Mom(
                value=float(mom_value.get_text().replace(",", ".")),
                cause=mom_cause.get_text(),
                year=date.year,
                month=date.month+1,
                day=date.day
                )

            occurred_lom = loms.get_lom(name=SapyConstants.DB.OCCURRED_LIST_NAME)
            occurred_lom.add([mom])
            self.updateMomStoreContent()
        print("closing dialog add occurred mom")

    def onMomDialogApplayButton(self, widget):
        self.gui_data.add_mom_flag = True

        #TODO add here a chekc for the date value
        mom_dialog = self.gui_builder.get_object("momDialog")
        mom_dialog.hide()

    def onMomDialogCancelButton(self, button):
        mom_dialog = self.gui_builder.get_object("momDialog")
        mom_dialog.hide()

    def onPlannedMomSelected(self, column, path, user_data):
        momPlannedStore = self.gui_builder.get_object("movementsPlannedStore")
        planned_lom = loms.get_lom(name=SapyConstants.DB.PLANNED_LIST_NAME)
        planned_mom = planned_lom.get_mom(id=momPlannedStore[path][0])

        mom_date = self.gui_builder.get_object("editMomDateEntry")
        mom_date.set_text(                      \
            str(planned_mom.time.day) +  \
            " / " + str(planned_mom.time.month) + \
            " / " + str(planned_mom.time.year))

        mom_cause = self.gui_builder.get_object("editMomCauseEntry")
        mom_cause.set_text(planned_mom.cause)
        mom_value = self.gui_builder.get_object("editMomValueEntry")
        mom_value.set_text(str(planned_mom.value))

        mom_dialog = self.gui_builder.get_object("momEditDialog")

        self.gui_data.mom = planned_mom
        mom_dialog.run()
        self.updateMomStoreContent()

    def onOccurredMomSelected(self, column, path, user_data):
        momOccurredStore = self.gui_builder.get_object("movementsOccurredStore")
        occurred_lom = loms.get_lom(name=SapyConstants.DB.OCCURRED_LIST_NAME)
        occurred_mom = occurred_lom.get_mom(id=momOccurredStore[path][0])
        mom_date = self.gui_builder.get_object("editMomDateEntry")
        mom_date.set_text(                      \
            str(occurred_mom.time.day) +  \
            " / " + str(occurred_mom.time.month) + \
            " / " + str(occurred_mom.time.year))

        mom_cause = self.gui_builder.get_object("editMomCauseEntry")
        mom_cause.set_text(occurred_mom.cause)
        mom_value = self.gui_builder.get_object("editMomValueEntry")
        mom_value.set_text(str(occurred_mom.value))

        mom_dialog = self.gui_builder.get_object("momEditDialog")

        self.gui_data.mom = occurred_mom
        mom_dialog.run()
        self.updateMomStoreContent()

    def onDayViewSelected(self, button):
        notebook = self.gui_builder.get_object("dateTimeView")
        notebook.set_current_page(0)
        self.onDaySelected(None)

    def onMonthViewSelected(self, button):
        notebook = self.gui_builder.get_object("dateTimeView")
        notebook.set_current_page(1)
        calendar = self.gui_builder.get_object("sapyCalendar")
        year_selector = self.gui_builder.get_object("monthViewYearValue")
        self.gui_data.month = calendar.get_date().month
        self.gui_data.year = calendar.get_date().year
        year_selector.set_value(self.gui_data.year)

        if self.gui_data.month == 0:
            monthBtn = self.gui_builder.get_object("GenButton")
        elif self.gui_data.month == 1 :
            monthBtn = self.gui_builder.get_object("FebButton")
        elif self.gui_data.month == 2 :
            monthBtn = self.gui_builder.get_object("MarButton")
        elif self.gui_data.month == 3 :
            monthBtn = self.gui_builder.get_object("AprButton")
        elif self.gui_data.month == 4 :
            monthBtn = self.gui_builder.get_object("MayButton")
        elif self.gui_data.month == 5 :
            monthBtn = self.gui_builder.get_object("JunButton")
        elif self.gui_data.month == 6 :
            monthBtn = self.gui_builder.get_object("JulButton")
        elif self.gui_data.month == 7 :
            monthBtn = self.gui_builder.get_object("AugButton")
        elif self.gui_data.month == 8 :
            monthBtn = self.gui_builder.get_object("SepButton")
        elif self.gui_data.month == 9 :
            monthBtn = self.gui_builder.get_object("OctButton")
        elif self.gui_data.month == 10 :
            monthBtn = self.gui_builder.get_object("NovButton")
        elif self.gui_data.month == 11 :
            monthBtn = self.gui_builder.get_object("DecButton")
        else :
            monthBtn = None

        if monthBtn is not None:
            monthBtn.activate()
            #monthBtn.clicked()

    def onYearViewSelected(self, button):
        notebook = self.gui_builder.get_object("dateTimeView")
        notebook.set_current_page(2)

        year_selector = self.gui_builder.get_object("yearViewYearValue")
        year_selector.set_value(self.gui_data.year)
        self.gui_data.start_date = datetime(day=1, month=1, year = self.gui_data.year).date()
        self.gui_data.end_date = datetime(day=31, month=12, year = self.gui_data.year).date()
        self.updateMomStoreContent()

    def updateMomStoreContent(self):
        self.updateMomStoreContentInPeriod(self.gui_data.start_date, self.gui_data.end_date)

    def updateMomStoreContentInPeriod(self, start_date:datetime.date, end_date:datetime.date):
        momOccurredStore = self.gui_builder.get_object("movementsOccurredStore")
        momOccurredStore.clear()
        for mom in loms.get_lom(name=SapyConstants.DB.OCCURRED_LIST_NAME).get_moms(start_date,end_date):
            momOccurredStore.append([mom.id, mom.cause, mom.value])

        momPlannedStore = self.gui_builder.get_object("movementsPlannedStore")
        momPlannedStore.clear()
        for mom in loms.get_lom(name=SapyConstants.DB.PLANNED_LIST_NAME).get_moms(start_date,end_date):
            momPlannedStore.append([mom.id, mom.cause, mom.value])

    def onMomEditDialogApplayButton(self, button):
        mom_date = self.gui_builder.get_object("editMomDateEntry")
        mom_cause = self.gui_builder.get_object("editMomCauseEntry")
        mom_value = self.gui_builder.get_object("editMomValueEntry")
        date = datetime.strptime(mom_date.get_text(), '%d / %m / %Y')
        self.gui_data.mom.update(
                new_value=float(mom_value.get_text().replace(",", ".")),
                new_cause=mom_cause.get_text(),
                new_year=date.year,
                new_month=date.month,
                new_day=date.day
                )
        mom_dialog = self.gui_builder.get_object("momEditDialog")
        mom_dialog.hide()
        self.updateMomStoreContent()

    def onMomEditDialogDeleteButton(self, button):
        self.gui_data.mom.delete()

        mom_dialog = self.gui_builder.get_object("momEditDialog")
        mom_dialog.hide()
        self.updateMomStoreContent()
        pass

    def onMomEditDialogCancelButton(self, button):
        mom_dialog = self.gui_builder.get_object("momEditDialog")
        mom_dialog.hide()
        pass
