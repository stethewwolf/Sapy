#!/usr/bin/env python
#
#   File : gui_dialogs.py
#   Author : stefano prina
#
# MIT License
#
# Copyright (c) 2017 Stefano Prina <stethewwolf@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#     The above copyright notice and this permission notice shall be included in all
#     copies or substantial portions of the Software.
#
#     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#     IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#     FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#     AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#     LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#     OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#     SOFTWARE.

import gi
import datetime
from sapy_lib.mom import Mom
from sapy_lib.lom import Lom
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class NewMomDialog(Gtk.Dialog):
    def __init__(
            self, 
            parent, 
            info,
            time_dialog,
            ):
        #TODO: fix Gtk-Message: GtkDialog mapped without a transient parent. This is discouraged.
        # parent instead of None
        Gtk.Dialog.__init__(self, "New Mom", None, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)
        box = self.get_content_area()
        grid = Gtk.Grid()
        box.add(grid)

        label_price = Gtk.Label("price")
        adjustment = Gtk.Adjustment(0, -99999, 99999, 0.1, 1, 0)
        info["price"] = Gtk.SpinButton()
        info["price"].set_adjustment(adjustment)
        info["price"].set_digits(2)
        info["price"].set_numeric(True)
        grid.add(label_price)
        grid.attach_next_to( 
                info["price"],
                label_price, 
                Gtk.PositionType.RIGHT, 
                2, 1
                )

        label_cause = Gtk.Label("Cause")
        info["cause"] = Gtk.Entry()
        grid.attach_next_to(
                label_cause, 
                label_price, 
                Gtk.PositionType.BOTTOM, 
                1, 1
                )
        grid.attach_next_to( 
                info["cause"],
                label_cause, 
                Gtk.PositionType.RIGHT, 
                2, 1
                )
        
        label_agent = Gtk.Label("Agent")
        info["agent"] = Gtk.Entry()
        grid.attach_next_to(
                label_agent, 
                label_cause, 
                Gtk.PositionType.BOTTOM, 
                1, 1
                )
        grid.attach_next_to( 
                info["agent"],
                label_agent, 
                Gtk.PositionType.RIGHT, 
                2, 1
                )
        
        label_payee = Gtk.Label("Payee")
        info["payee"] = Gtk.Entry()
        grid.attach_next_to(
            label_payee, 
            label_agent, 
            Gtk.PositionType.BOTTOM, 
            1, 1
            )
        grid.attach_next_to( info["payee"],
            label_payee, 
            Gtk.PositionType.RIGHT, 
            2, 1
            )
        
        label_time = Gtk.Label("Time")
        self.time_button = Gtk.Button("Time")
        self.time_button.connect("clicked",time_dialog) 
        grid.attach_next_to(
                label_time, 
                label_payee, 
                Gtk.PositionType.BOTTOM, 
                1, 1
                )
        grid.attach_next_to( 
                self.time_button,
                label_time, 
                Gtk.PositionType.RIGHT, 
                2, 1
                )
        self.show_all()

class NewMomDialogCtr(object):
    def __init__(self, parent):
        self.__parent = parent
        self.__time = datetime.datetime.now()
        self.__info = {
                "price" : -1,
                "cause" : None,
                "agent" : None,
                "payee" : None,
                "time" : None
                }
        self.__view = NewMomDialog(
                self.__parent,
                self.__info,
                self.display_time_dialog
                )


    def get_mom(self):
        mom = Mom()
        mom.price(float(self.__info["price"].get_value()))
        mom.cause(self.__info["cause"].get_text())
        mom.agent(self.__info["agent"].get_text())
        mom.payee(self.__info["payee"].get_text())
        mom.time(self.__time)
                
        return mom
    
    def display_time_dialog ( self, widget ):
        calendar = CalendarDialogsCtr(self.__view)
        calendar.run()
        self.__time = datetime.datetime(
                calendar.get_time()[0],
                calendar.get_time()[1],
                calendar.get_time()[2],
                calendar.get_time()[3],
                calendar.get_time()[4],
                )
        calendar.destroy()

    def run(self):
        return self.__view.run()
    
    def destroy(self):
        return self.__view.destroy()



class CalendarDialogs(Gtk.Dialog):
    def __init__(self, parent):
        #TODO: fix Gtk-Message: GtkDialog mapped without a transient parent. This is discouraged.
        # parent instead of None
        Gtk.Dialog.__init__(self,"Calendar", None, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        
        self.calendar = Gtk.Calendar()
        box = self.get_content_area()
        box.pack_start(Gtk.Label("Date"), False, False, 10)
        box.pack_start(self.calendar, True, True, 10)

        box.pack_start(Gtk.Label("Hours"), False, False, 10)
        hours_adjustment = Gtk.Adjustment(0, 0, 24, 1, 1, 0)
        self.hours_button = Gtk.SpinButton()
        self.hours_button.set_adjustment(hours_adjustment)
        self.hours_button.set_numeric(True)
        box.pack_start(self.hours_button, False, False, 10)

        box.pack_start(Gtk.Label("Minutes"), False, False, 10)
        min_adjustment = Gtk.Adjustment(0, 0, 59, 1, 1, 0)
        self.minutes_button = Gtk.SpinButton()
        self.minutes_button.set_adjustment(min_adjustment)
        self.minutes_button.set_numeric(True)
        box.pack_start(self.minutes_button, False, False, 10)
        self.show_all()



class CalendarDialogsCtr(object):
    def __init__(self, parent):
        self.__parent = parent
        self.__view = CalendarDialogs(self.__parent)

    def run(self):
        return self.__view.run()

    def destroy(self):
        self.__date = self.__view.calendar.get_date()
        return self.__view.destroy()

    def get_time(self):
        return (
                self.__view.calendar.get_date()[0],
                self.__view.calendar.get_date()[1]+1,
                self.__view.calendar.get_date()[2],
                self.__view.hours_button.get_value_as_int(),
                self.__view.minutes_button.get_value_as_int()
                )
         
 

class WarningDialog(Gtk.Dialog):
    def __init__(self, parent, message):
        Gtk.Dialog.__init__(self,"Calendar", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        
        self.label = Gtk.Label(message)
        box = self.get_content_area()
        box.add(self.label)

        self.show_all()


class WarningDialogsCtr(object):
    def __init__(self, parent, message):
        self.__parent = message
        self.__parent = parent
        slef.view = WarningDialogs(self.__parent)


class NewLomDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self,"Calendar", None, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = Gtk.Label("Insert the name of the new lom")

        box = self.get_content_area()
        box.add(label)

        self.lom_name = Gtk.Entry()
        self.lom_name.set_text("New Lom")
        box.add(self.lom_name)
  
        self.show_all()


class NewLomDialogCtr(object):
    def __init__(self, parent):
        self.__parent = parent
        self.__view = NewLomDialog(self.__parent)

    def run(self):
        return self.__view.run()
    
    def destroy(self):
        return self.__view.destroy()

    def get_lom(self):
        return Lom(self.__view.lom_name.get_text())

class FileDialog(Gtk.FileChooserDialog):
    def __init__(self, parent):
        Gtk.FileChooserDialog.__init__(self,"Open File", None, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        
        csv_filter = Gtk.FileFilter()
        csv_filter.set_name("All files")
        csv_filter.add_pattern("*")
        self.add_filter(csv_filter)
        csv_filter = Gtk.FileFilter()
        csv_filter.set_name("CSV")
        csv_filter.add_pattern("*.csv")
        self.add_filter(csv_filter)

        self.show_all()


class FilegDialogCtr(object):
    def __init__(self, parent):
        self.__parent = parent
        self.__view = FileDialog(self.__parent)
    def run(self):
        return self.__view.run()
    
    def destroy(self):
        return self.__view.destroy()

    def get_file_name(self):
        return self.__view.get_filename()



