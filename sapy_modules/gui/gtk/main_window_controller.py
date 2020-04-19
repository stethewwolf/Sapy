#
#   File : main_window_controller.py
#   Author : stefano prina <stethewwolf@gmail.com>
#

from sapy_modules.gui.gtk.main_window_view import main_window_view
import sapy_modules.sapy.lom as loms
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import datetime


class main_window_controller(object):

    def __init__(self):
        self.lom_list = loms.get_loms()
        self.lom = None
        self.view = None
        self.moms_store = Gtk.ListStore(int, str, float, str, bool) # id cause, value, date
        self.set_list(self.lom_list[0].name)
        self.view = main_window_view(self)

    def set_list(self, lom_name):
        self.lom = loms.get_lom(name=lom_name)

        if not self.view:
            date = datetime.datetime.today().date()
        else:
            raw_date = self.view.calendar.get_date()
            date = datetime.date(year = raw_date.year, month = raw_date.month+1, day = raw_date.day)

        sd = date - datetime.timedelta(days=15) # start date
        ed = date + datetime.timedelta(days=15) # end date

        moms = self.lom.get_moms(start_date=sd, end_date=ed)

        self.moms_store.clear()

        if len(moms) == 0:
            self.moms_store.append([-1, "-", 0, "-", False])
        else :
            for mom in self.lom.get_moms(start_date=sd, end_date=ed):
                self.moms_store.append([mom.id, mom.cause, mom.value, mom.time.strftime('%d-%m-%Y'), False])

        pass

    def rebuild_list(self, widget=None, event=None):
        print("list updated")
        if not self.view:
            date = datetime.datetime.today().date()
        else:
            raw_date = self.view.calendar.get_date()
            print(raw_date)
            date = datetime.date(year = raw_date.year, month = raw_date.month+1, day = raw_date.day)

        sd = date - datetime.timedelta(days=15) # start date
        ed = date + datetime.timedelta(days=15) # end date

        moms = self.lom.get_moms(start_date=sd, end_date=ed)

        self.moms_store.clear()

        if len(moms) == 0:
            self.moms_store.append([-1, "-", 0, "-", False])
        else :
            for mom in self.lom.get_moms(start_date=sd, end_date=ed):
                self.moms_store.append([mom.id, mom.cause, mom.value, mom.time.strftime('%d-%m-%Y'), False])

        pass


    def add_mom(self, mom):
        self.lom.add([mom])
        self.moms_store.append([mom.id, mom.cause, mom.value, mom.time.strftime('%d-%m-%Y'), False])

    def del_mom(self):
        for mom_row in self.moms_store:
            if mom_row[4]:
                del_mom = self.lom.get_mom(mom_row[0])

                if del_mom:
                    del_mom.delete()
            
                self.moms_store.remove(mom_row.iter)

    def run (self):
        self.view.main()
