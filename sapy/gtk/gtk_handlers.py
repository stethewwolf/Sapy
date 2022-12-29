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
from sapy.core import loms
from sapy.core.moms import Mom
import sapy.core.profiles as profiles
from sapy.utils import loggers as LoggerFactory
from sapy.utils import config as SingleConfig
from sapy.utils import values as SapyValues
from sapy.commands.command import Command
import calendar as clndr
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
import matplotlib as mp
import os
from pathlib import Path
from gi.repository import Gtk
import gi
gi.require_version('Gtk', '3.0')


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
        self.ax = None
        self.fig = None
        self.set_start_date_flag = True
        self.is_file_been_imported_flag = True
        self.active_profile = None


class Handler:
    def __init__(self, gui_data: GuiData, gui_builder):
        self.logger = LoggerFactory.getLogger(str(self.__class__))
        self.gui_data = gui_data
        self.gui_builder = gui_builder

    def onDestroy(self, *args):
        Gtk.main_quit()

    def onCalendarTabSelected(self, button):
        notebook = self.gui_builder.get_object("sapyNotebooks")
        notebook.set_current_page(0)

    def onGraphTabSelected(self, button):
        notebook = self.gui_builder.get_object("sapyNotebooks")
        notebook.set_current_page(1)
        self.updatePlot()

    def onDaySelected(self, button):
        calendar = self.gui_builder.get_object("sapyCalendar")
        self.gui_data.start_date = datetime(
            calendar.get_date().year,
            calendar.get_date().month+1,
            calendar.get_date().day)
        self.gui_data.end_date = self.gui_data.start_date
        self.updateMomStoreContent()
        self.updateTotalLabels()

    def onYearMonthViewSelected(self, spinButton):
        self.gui_data.year = int(spinButton.get_value())
        self.gui_data.start_date = datetime(
            self.gui_data.year, self.gui_data.month, 1)
        self.gui_data.end_date = datetime(
            self.gui_data.year,
            self.gui_data.month,
            clndr.monthrange(self.gui_data.year, self.gui_data.month)[1])
        self.updateMomStoreContent()
        self.updateTotalLabels()

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
            self.gui_data.start_date = datetime(
                self.gui_data.year, self.gui_data.month, 1)
            self.gui_data.end_date = datetime(
                self.gui_data.year,
                self.gui_data.month,
                clndr.monthrange(self.gui_data.year, self.gui_data.month)[1])
            self.updateMomStoreContent()
            self.updateTotalLabels()

    def onAddPlannedSelected(self, button):
        mom_dialog = self.gui_builder.get_object("momDialog")
        mom_date = self.gui_builder.get_object("addMomDateEntry")
        calendar = self.gui_builder.get_object("sapyCalendar")
        mom_date.set_text(
            str(calendar.get_date().day) + " / " +
            str(calendar.get_date().month+1) + " / " +
            str(calendar.get_date().year))

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
                month=date.month,
                day=date.day
                )

            self.gui_data.active_profile.add_planned_mom([mom])

            self.updateMomStoreContent()

    def onAddOccurredSelected(self, button):
        self.gui_data.add_mom_flag = False
        calendar = self.gui_builder.get_object("sapyCalendar")
        mom_dialog = self.gui_builder.get_object("momDialog")
        mom_date = self.gui_builder.get_object("addMomDateEntry")
        mom_date.set_text(
            str(calendar.get_date().day) + " / " +
            str(calendar.get_date().month+1) + " / " +
            str(calendar.get_date().year))

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
                month=date.month,
                day=date.day
                )

            self.gui_data.active_profile.add_occurred_mom([mom])
            self.updateMomStoreContent()

    def onMomDialogApplayButton(self, widget):
        self.gui_data.add_mom_flag = True

        # TODO add here a chekc for the date value
        mom_dialog = self.gui_builder.get_object("momDialog")
        mom_dialog.hide()

    def onMomDialogCancelButton(self, button):
        mom_dialog = self.gui_builder.get_object("momDialog")
        mom_dialog.hide()

    def onPlannedMomSelected(self, column, path, user_data):
        momPlannedStore = self.gui_builder.get_object("movementsPlannedStore")
        planned_lom = loms.get_lom(name=loms.PLANNED_LIST_NAME)
        planned_mom = planned_lom.get_mom(id=momPlannedStore[path][0])

        mom_date = self.gui_builder.get_object("editMomDateEntry")
        mom_date.set_text(
            str(planned_mom.time.day) +
            " / " + str(planned_mom.time.month) +
            " / " + str(planned_mom.time.year))

        mom_cause = self.gui_builder.get_object("editMomCauseEntry")
        mom_cause.set_text(planned_mom.cause)
        mom_value = self.gui_builder.get_object("editMomValueEntry")
        mom_value.set_text(str(planned_mom.value))

        mom_dialog = self.gui_builder.get_object("momEditDialog")

        self.gui_data.mom = planned_mom
        mom_dialog.run()
        self.updateMomStoreContent()
        self.updateTotalLabels()

    def onOccurredMomSelected(self, column, path, user_data):
        momOccurredStore = self.gui_builder.get_object(
            "movementsOccurredStore")
        occurred_lom = loms.get_lom(name=loms.OCCURRED_LIST_NAME)
        occurred_mom = occurred_lom.get_mom(id=momOccurredStore[path][0])
        mom_date = self.gui_builder.get_object("editMomDateEntry")
        mom_date.set_text(
            str(occurred_mom.time.day) +
            " / " + str(occurred_mom.time.month) +
            " / " + str(occurred_mom.time.year))

        mom_cause = self.gui_builder.get_object("editMomCauseEntry")
        mom_cause.set_text(occurred_mom.cause)
        mom_value = self.gui_builder.get_object("editMomValueEntry")
        mom_value.set_text(str(occurred_mom.value))

        mom_dialog = self.gui_builder.get_object("momEditDialog")

        self.gui_data.mom = occurred_mom
        mom_dialog.run()
        self.updateMomStoreContent()
        self.updateTotalLabels()

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
        elif self.gui_data.month == 1:
            monthBtn = self.gui_builder.get_object("FebButton")
        elif self.gui_data.month == 2:
            monthBtn = self.gui_builder.get_object("MarButton")
        elif self.gui_data.month == 3:
            monthBtn = self.gui_builder.get_object("AprButton")
        elif self.gui_data.month == 4:
            monthBtn = self.gui_builder.get_object("MayButton")
        elif self.gui_data.month == 5:
            monthBtn = self.gui_builder.get_object("JunButton")
        elif self.gui_data.month == 6:
            monthBtn = self.gui_builder.get_object("JulButton")
        elif self.gui_data.month == 7:
            monthBtn = self.gui_builder.get_object("AugButton")
        elif self.gui_data.month == 8:
            monthBtn = self.gui_builder.get_object("SepButton")
        elif self.gui_data.month == 9:
            monthBtn = self.gui_builder.get_object("OctButton")
        elif self.gui_data.month == 10:
            monthBtn = self.gui_builder.get_object("NovButton")
        elif self.gui_data.month == 11:
            monthBtn = self.gui_builder.get_object("DecButton")
        else:
            monthBtn = None

        if monthBtn is not None:
            monthBtn.activate()

    def onYearViewSelected(self, button):
        notebook = self.gui_builder.get_object("dateTimeView")
        notebook.set_current_page(2)
        year_selector = self.gui_builder.get_object("yearViewYearValue")
        year_selector.set_value(self.gui_data.year)
        self.gui_data.start_date = datetime(
            day=1, month=1, year=self.gui_data.year).date()
        self.gui_data.end_date = datetime(
            day=31, month=12, year=self.gui_data.year).date()
        self.updateMomStoreContent()
        self.updateTotalLabels()

    def onYearViewYearValueChanged(self, button):
        year_selector = self.gui_builder.get_object("yearViewYearValue")
        self.gui_data.year = int(year_selector.get_value())
        self.gui_data.start_date = datetime(
            day=1, month=1, year=self.gui_data.year).date()
        self.gui_data.end_date = datetime(
            day=31, month=12, year=self.gui_data.year).date()
        self.updateMomStoreContent()
        self.updateTotalLabels()

    def updateMomStoreContent(self):
        self.updateMomStoreContentInPeriod(
            self.gui_data.start_date, self.gui_data.end_date)

    def updateMomStoreContentInPeriod(self, start_date:datetime.date, end_date:datetime.date):
        momOccurredStore = self.gui_builder.get_object(
            "movementsOccurredStore")
        momOccurredStore.clear()
        moms = self.gui_data.active_profile.get_occurred_moms(
            start_date, end_date)
        for mom in moms:
            momOccurredStore.append(
                [mom.id, str(mom.time), mom.value, mom.cause])

        momPlannedStore = self.gui_builder.get_object("movementsPlannedStore")
        momPlannedStore.clear()
        moms = self.gui_data.active_profile.get_planned_moms(
            start_date, end_date)
        for mom in moms:
            momPlannedStore.append(
                [mom.id, str(mom.time), mom.value, mom.cause])

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
        self.updateTotalLabels()

    def onMomEditDialogDeleteButton(self, button):
        self.gui_data.mom.delete()

        mom_dialog = self.gui_builder.get_object("momEditDialog")
        mom_dialog.hide()
        self.updateMomStoreContent()
        self.updateTotalLabels()

    def onMomEditDialogCancelButton(self, button):
        mom_dialog = self.gui_builder.get_object("momEditDialog")
        mom_dialog.hide()

    def updatePlot(self):
        self.gui_data.ax.clear()

        occurred_lom = loms.get_lom(name=loms.OCCURRED_LIST_NAME)
        bxd_occurred_lom = occurred_lom.balance_per_day(
            self.gui_data.start_date, self.gui_data.end_date)
        self.gui_data.ax.scatter(
            mp.dates.date2num(bxd_occurred_lom[0]),
            bxd_occurred_lom[1],
            label=occurred_lom.name, marker="+",
            color=occurred_lom.color)

        planned_lom = loms.get_lom(name=loms.PLANNED_LIST_NAME)
        bxd_planned_lom = planned_lom.balance_per_day(
            self.gui_data.start_date, self.gui_data.end_date)
        self.gui_data.ax.scatter(
            mp.dates.date2num(bxd_planned_lom[0]), bxd_planned_lom[1],
            label=planned_lom.name,
            marker="+",
            color=planned_lom.color)

        self.gui_data.ax.set_xlim(
            self.gui_data.start_date, self.gui_data.end_date)

        self.gui_data.ax.plot()
        self.gui_data.ax.legend()

        self.gui_data.fig.autofmt_xdate()

    def onGraphSetStartDate(self, button):
        self.gui_data.set_start_date_flag = True
        cal_dialog = self.gui_builder.get_object("GtkCalendarDialog")
        cal_dialog.run()
        cal_dialog.hide()

    def onGraphSetEndDate(self, button):
        self.gui_data.set_start_date_flag = False
        cal_dialog = self.gui_builder.get_object("GtkCalendarDialog")
        cal_dialog.run()
        cal_dialog.hide()

    def onGraphSetDateSelected(self, button):
        cal_dialog = self.gui_builder.get_object("GtkCalendarDialog")
        cal_dialog.hide()
        calendar = self.gui_builder.get_object("CalendarDialog")

        if self.gui_data.set_start_date_flag:
            self.gui_data.start_date = datetime(
                calendar.get_date().year,
                calendar.get_date().month+1,
                calendar.get_date().day)
        else:
            self.gui_data.end_date = datetime(
                calendar.get_date().year,
                calendar.get_date().month+1,
                calendar.get_date().day)

        self.updatePlot()

    def onGtkCalendarDialogClose(self, button):
        cal_dialog = self.gui_builder.get_object("GtkCalendarDialog")
        cal_dialog.hide()

    def onMenuButton(self, button):
        menu = self.gui_builder.get_object("menuPopOver")
        menu.show_all()

    def onImportButton(self, button):
        menu = self.gui_builder.get_object("menuPopOver")
        menu.hide()
        self.gui_data.is_file_been_imported_flag = True
        file_dialog = self.gui_builder.get_object("fileChooserDialog")
        file_dialog.run()
        file_dialog.hide()

    def onExportButton(self, button):
        menu = self.gui_builder.get_object("menuPopOver")
        menu.hide()
        self.gui_data.is_file_been_imported_flag = False
        file_dialog = self.gui_builder.get_object("fileChooserDialog")
        file_dialog.run()
        file_dialog.hide()

    def onFileChooserCancelButton(self, button):
        file_dialog = self.gui_builder.get_object("fileChooserDialog")
        file_dialog.hide()

    def onFileChooserOkButton(self, button):
        file_dialog = self.gui_builder.get_object("fileChooserDialog")
        plannedCheckBox = self.gui_builder.get_object(
            "FileChooserPlannedCheck")
        occurredCheckBox = self.gui_builder.get_object(
            "FileChooserOccurredCheck")
        workInProgressMessage = self.gui_builder.get_object(
            "workInProgressMessage")
        planned_lom = loms.get_lom(name=loms.PLANNED_LIST_NAME)
        occurred_lom = loms.get_lom(name=loms.OCCURRED_LIST_NAME)

        file_dialog.hide()
        if plannedCheckBox.get_active():
            workInProgressMessage.show_all()

            if self.gui_data.is_file_been_imported_flag:
                planned_lom.csv_import(file_dialog.get_file())
            else:
                planned_lom.csv_export(
                    file_dialog.get_file(),
                    self.gui_data.start_date,
                    self.gui_data.end_date)

            workInProgressMessage.hide()

        if occurredCheckBox.get_active():
            workInProgressMessage.show_all()

            if self.gui_data.is_file_been_imported_flag:
                occurred_lom.csv_import(file_dialog.get_file())
            else:
                occurred_lom.csv_export(
                    file_dialog.get_file(),
                    self.gui_data.start_date,
                    self.gui_data.end_date)

            workInProgressMessage.hide()

    def updateTotalLabels(self):
        occurred_total_label = self.gui_builder.get_object(
            "OccurredTotalLabel")
        planned_total_label = self.gui_builder.get_object(
            "PlannedTotalLabel")

        planned_total_label.set_text(
            str(self.gui_data.active_profile.get_planned_balance(
                self.gui_data.start_date,
                self.gui_data.end_date)))
        occurred_total_label.set_text(
            str(self.gui_data.active_profile.get_occurred_balance(
                self.gui_data.start_date,
                self.gui_data.end_date)))

    def onProfilesDialogManagementButton(self, button):
        profilesManagementDialog = self.gui_builder.get_object(
            "profilesManagementDialog")
        menuPopOver = self.gui_builder.get_object("ProfilesPopMenu")
        profilesManagementDialog.show_all()
        menuPopOver.hide()

    def onCloseProfilesManagementDialog(self, button, stuff):
        profilesManagementDialog = self.gui_builder.get_object(
            "profilesManagementDialog")
        profilesManagementDialog.hide()

    def onButtonCancelProfilesManagementDialog(self, button):
        profilesManagementDialog = self.gui_builder.get_object(
            "profilesManagementDialog")
        profilesManagementDialog.hide()

    def onAboutButton(self, button):
        about_dialog = self.gui_builder.get_object("aboutDialog")
        about_dialog.show_all()

    def onProfileClickedButton(self, tree_view, tree_path, tree_view_column):
        edit_profile_dialog_id = self.gui_builder.get_object(
            "editProfileDialogId")
        edit_profile_dialog_name = self.gui_builder.get_object(
            "editProfileDialogName")

        profiles_store = self.gui_builder.get_object("ProfilesListStore")

        edit_profile_dialog_id.set_text(
            str(profiles_store[int(tree_path.to_string())][0]))
        edit_profile_dialog_name.set_text(
            str(profiles_store[int(tree_path.to_string())][1]))

        edit_profile_dialog = self.gui_builder.get_object("EditProfileDialog")
        edit_profile_dialog.show_all()

    def onDeleteProfileButton(self, button):
        profiles_view = self.gui_builder.get_object("profilesListView")
        selected_rows = profiles_view.get_selection().get_selected_rows()

        profiles_store = selected_rows[0]
        selected_paths = selected_rows[1]

        for selected_item in selected_paths:
            profile_id = profiles_store[int(selected_item.to_string())][0]
            profile = profiles.get_profile(id=profile_id)

            profiles_store.remove(
                profiles_store[int(selected_item.to_string())].iter
            )
            profile.remove_profile()

        self.updateProfilesPopUpMenu()

    def onAddNewProfileButton(self, button):
        profilesListView = self.gui_builder.get_object("profilesListView")
        profiles_store = self.gui_builder.get_object("ProfilesListStore")
        new_profile = profiles.Profile(name="New Profile")
        profiles_store.append([new_profile.profile_id, new_profile.name])
        self.updateProfilesPopUpMenu()

    def onButtonCancelEditProfilesDialog(self, button):
        edit_profile_dialog = self.gui_builder.get_object("EditProfileDialog")
        edit_profile_dialog.hide()

    def onButtonSaveProfile(self, button):
        edit_profile_dialog_id = self.gui_builder.get_object(
            "editProfileDialogId")
        edit_profile_dialog_name = self.gui_builder.get_object(
            "editProfileDialogName")
        profile_id = edit_profile_dialog_id.get_text()
        new_profile_name = edit_profile_dialog_name.get_text()
        profile = profiles.get_profile(id=profile_id)
        profile.update_name(name=new_profile_name)
        edit_profile_dialog = self.gui_builder.get_object("EditProfileDialog")
        edit_profile_dialog.hide()
        self.updateProfilesPopUpMenu()

    def updateProfilesPopUpMenu(self):
        profiles_button_box = self.gui_builder.get_object(
            "ProfilesButtonBox")
        active_profile_label = self.gui_builder.get_object(
            "ActiveProfileLabel")
        default_profile_id = profiles.get_default_profile_id()

        for child in profiles_button_box.get_children():
            child.destroy()

        profiles_list_store = self.gui_builder.get_object("ProfilesListStore")
        profiles_list_store.clear()

        profiles_list = profiles.get_profiles()
        for profile in profiles_list:
            profiles_list_store.append([profile.profile_id, profile.name])
            profile_button = Gtk.Button()
            profile_button.connect("clicked", self.onSelectProfileCheckClicked)
            profile_button.set_label(
                "{} - {}".format(profile.profile_id, profile.name))

            if int(profile.profile_id) == int(default_profile_id):
                self.gui_data.active_profile = profile
                active_profile_label.set_label(
                    "{} - {}".format(profile.profile_id, profile.name))

            profiles_button_box.pack_start(profile_button, False, False, 2)
        profiles_button_box.show_all()

    def onSelectProfileCheckClicked(self, button):
        profiles_menu = self.gui_builder.get_object("ProfilesPopMenu")
        profile_id = int(button.get_label().split("-")[0])
        profiles.set_default_profile_id(profile_id)
        self.updateProfilesPopUpMenu()
        profiles_menu.hide()
        self.updateTotalLabels()
        self.updateMomStoreContent()



