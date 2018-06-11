#!/usr/bin/env python
#
#   File : gui.py
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

from sapy_lib.mom import Mom
import datetime
import sapy_lib.gui_dialogs as dialogs
from sapy_lib.datamgr import DataMgr
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure
#import matplotlib.pyplot as plt
import matplotlib

class LomTab(Gtk.Box):
    def __init__(
            self,
            controller
            ):
        Gtk.Box.__init__(
                self,
                orientation=Gtk.Orientation.VERTICAL,
                spacing=20
                )
        self.set_border_width(10)
        self.__controller = controller

        self.__treeview = Gtk.TreeView(self.__controller.mom_store)
        column_id = Gtk.TreeViewColumn("ID", Gtk.CellRendererText(), text=0)
        self.__treeview.append_column(column_id)
        column_price = Gtk.TreeViewColumn("Price", Gtk.CellRendererText(), text=1)
        self.__treeview.append_column(column_price)
        column_cause = Gtk.TreeViewColumn("Cause", Gtk.CellRendererText(), text=2)
        self.__treeview.append_column(column_cause)
        column_time = Gtk.TreeViewColumn("Time", Gtk.CellRendererText(), text=3)
        self.__treeview.append_column(column_time)
        render_delete = Gtk.CellRendererToggle()
        render_delete.connect("toggled",self.__controller.toggle_delete_mom)
        column_delete = Gtk.TreeViewColumn(
                "Delete", 
                render_delete, 
                active=4
                )
        self.__treeview.append_column(column_delete)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(
            Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(self.__treeview)
        self.pack_start(scrolled_window, True, True, 10)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        button = Gtk.Button(label="add")
        button.connect("clicked",self.__controller.create_mom)
        hbox.add(button)
        button = Gtk.Button(label="remove")
        button.connect("clicked",self.__controller.delete_mom)
        hbox.add(button)
        self.pack_end(hbox, False, False, 10)

        button = Gtk.Button(label="import from csv")
        button.connect("clicked",self.__controller.parent.import_csv, self.__controller.lom)
        hbox.add(button)
        self.pack_end(hbox, False, False, 10)


class LomTabCtr(object):
    def __init__(self, parent, lom_id):
        self.parent = parent
        self.lom_id = lom_id
        self.lom = self.parent.data.get_lom(
            self.lom_id,
            self.parent.start_date, 
            self.parent.end_date
            )

        self.mom_store = Gtk.ListStore(int, float, str, str, bool)
        self.view = LomTab(self)

        if self.lom :
            for mom in self.lom.movements :
                self.mom_store.append([
                    mom.mom_id(),
                    mom.get_value(),
                    mom.cause(),
                    str(mom.time()),
                    False
                    ])

    def create_mom(self, widget):
        dialog = dialogs.NewMomDialogCtr(self.view)
        response = dialog.run()

        if response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            return
        #elif response == Gtk.ResponseType.OK:

        mom = dialog.get_mom() 
        dialog.destroy()

        mom_id = self.lom.insert(mom)
        self.parent.data.add_mom(self.lom,mom.to_dict())
        self.mom_store.append([
            mom_id,
            mom.get_value(),
            mom.cause(),
            str(mom.time()),
            False
            ])
        self.parent.__main_tab.plot()
        
    def delete_mom(self, widget):
        treeiter = self.mom_store.get_iter_first()
        while treeiter != None:
            nexiter = self.mom_store.iter_next(treeiter)

            if self.mom_store[treeiter][4]:
                mom  = self.lom.get_mom_by_id( 
                    self.mom_store[treeiter][0]
                    )
                self.lom.remove(mom)
                self.parent.data.remove_mom(self.lom,mom)
                self.mom_store.remove(treeiter)

            treeiter = nexiter
        self.parent.__main_tab.plot()
            
    def toggle_delete_mom(self, widget, path):
        self.mom_store[path][4] = not self.mom_store[path][4]


class MainTab(Gtk.Box):
    def __init__(
            self, 
            controller
            ):
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.HORIZONTAL, spacing = 20)
        self.__controller = controller
        self.set_border_width(10)
        self.canvas = None

        # left side
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 20)
        self.pack_start(vbox, False, False, 10)
        label = Gtk.Label("Lom list")
        vbox.pack_start(label, False, False, 10)
        self.__treeview = Gtk.TreeView(self.__controller.lom_store)

        column_id = Gtk.TreeViewColumn("ID", Gtk.CellRendererText(), text = 0)
        self.__treeview.append_column(column_id)
        column_name = Gtk.TreeViewColumn("Name", Gtk.CellRendererText(), text = 1)
        self.__treeview.append_column(column_name)
        render_visible = Gtk.CellRendererToggle()
        render_visible.connect(
                "toggled",self.__controller.toggle_visible_lom)
        column_visible = Gtk.TreeViewColumn(
                "Visible", 
                render_visible, 
                active = 2
                )
        self.__treeview.append_column(column_visible)
        render_delete = Gtk.CellRendererToggle()
        render_delete.connect(
                "toggled", self.__controller.toggle_delete_lom)
        column_delete = Gtk.TreeViewColumn(
                "Delete", 
                render_delete, 
                active = 3
                )
        self.__treeview.append_column(column_delete)
        vbox.pack_start(self.__treeview, False, True, 10)

        hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 20)
        button = Gtk.Button(label = "add")
        button.connect("clicked", self.__controller.create_lom)
        hbox.pack_start(button, False, False, 10)
        button = Gtk.Button(label = "remove")
        button.connect("clicked", self.__controller.delete_lom)
        hbox.pack_end(button, False, False, 10)
        vbox.pack_end(hbox, False, False, 10)
 
        # right side
        self.right_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 20)
        self.pack_end(self.right_box, True, True, 10)
        
        # bottom labels
        #hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 20)
        #self.enda_date_lable = Gtk.Label(
        #        self.__controller.start_drawing_date)
        #vbox.pack_end(hbox, False, False, 10)

        # bottom buttons
        hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 20)

        button = Gtk.Button(label = "set start date")
        button.connect("clicked", self.__controller.set_start_drawing_date)
        hbox.pack_start(button, False, False, 10)
        
       # button = Gtk.Button(label = "refresh plot")
       # button.connect("clicked", self.__controller.plot)
       # hbox.pack_start(button, False, False, 10)


        button = Gtk.Button(label = "set end date")
        button.connect("clicked", self.__controller.set_end_drawing_date)
        hbox.pack_end(button, False, False, 10)

        self.right_box.pack_end(hbox, False, False, 10)

        self.canvas = FigureCanvas(self.__controller.figure)  # a gtk.DrawingArea
        self.right_box.pack_start(self.canvas, True, True, 10)
 

class MainTabCtr(object):
    def __init__(
            self, 
            parent = None,
            ):
        self.parent = parent
        self.title = "Main Tab"
        self.lom_store = Gtk.ListStore(int, str, bool, bool)
        self.view_id = -1
        self.simple_lom_list = self.parent.data.get_simple_loms()

        for lom in self.simple_lom_list :
            self.lom_store.append([
                lom.lom_id(),
                lom.name(),
                lom.is_visible(),
                False
                ])
        
        # manage plot
        # example at:
        # https://matplotlib.org/examples/user_interfaces/embedding_in_gtk.html
        #
        # http://gtk3-matplotlib-cookbook.readthedocs.io/en/latest/enteringdata.html
        self.figure = Figure( figsize=(1, 1), dpi=100)
        #self.subplot = self.figure.add_subplot(111)
        self.view = MainTab(self)
        self.plot() 

    def toggle_visible_lom(self, widget, path):
        self.lom_store[path][2] = not self.lom_store[path][2]

        lom = [lom for lom in self.simple_lom_list \
                if lom.lom_id() == self.lom_store[path][0]][0]

        lom.visible(
                not lom.is_visible()
                )
        self.parent.data.update_lom(lom)
        self.plot()

    def toggle_delete_lom(self, widget, path):
        self.lom_store[path][3] = not self.lom_store[path][3]

    def create_lom(self, widget):
        dialog = dialogs.NewLomDialogCtr(self.view)
        response = dialog.run()

        if response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            return
        
        lom = dialog.get_lom()
        lom_id = self.parent.data.insert_lom(lom)
        self.simple_lom_list.append(lom)

        self.lom_store.append([
            lom_id,
            lom.name(),
            lom.is_visible(),
            False
            ])
        
        self.parent.insert_tab(lom)
        dialog.destroy()

    def delete_lom(self, widget):
        treeiter = self.lom_store.get_iter_first()
        while treeiter != None:
            nexiter = self.lom_store.iter_next(treeiter)

            if self.lom_store[treeiter][3]:
                for lom in self.simple_lom_list:
                    if lom.lom_id() == self.lom_store[treeiter][0]:
                        self.parent.delete_tab(lom)
                        self.lom_store.remove(treeiter)
                        self.parent.data.remove_lom(lom)

            treeiter = nexiter

    def plot(self, widget = None):
        self.figure.clear()
        self.subplot = self.figure.add_subplot(111)
        drawing_data = self.parent.data.get_graph_data(
            self.parent.start_date, 
            self.parent.end_date
            )

        for lom in drawing_data:
            dates = matplotlib.dates.date2num(lom[0])
            self.subplot.scatter(dates, lom[1], label=lom[2])
        
        self.subplot.set_xlim(self.parent.start_date, self.parent.end_date)
        self.figure.autofmt_xdate()
        self.figure.legend()

    def set_start_drawing_date(self, widget = None):
        dialog = dialogs.CalendarDialogsCtr(None)
        response = dialog.run()

        if response  == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            return

        self.parent.start_date = datetime.datetime(
                dialog.get_time()[0],
                dialog.get_time()[1],
                dialog.get_time()[2]
                )
        dialog.destroy()
        self.plot()

    def set_end_drawing_date(self, widget = None):
        dialog = dialogs.CalendarDialogsCtr(None)
        response = dialog.run()

        if response  == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            return

        self.parent.end_date = datetime.datetime(
                dialog.get_time()[0],
                dialog.get_time()[1],
                dialog.get_time()[2]
                )
        dialog.destroy()
        self.plot()


class Gui(Gtk.Window):
    def __init__(self, controller = None):
        self.__controller = controller
        Gtk.Window.__init__(self, title="Sapy")
        self.connect("delete-event", Gtk.main_quit)
        self.set_border_width(3)
        self.set_default_size(800, 600)
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)
   
    def append_tab(self, tab, title):
        return self.notebook.append_page(tab, title)

    def detach_tab(self, tab):
        self.notebook.remove_page(tab.view_id)

    def run(self):
        self.show_all()


class GuiCtr(object):
    def __init__(self, data, parent = None):
        self.__parent = parent
        self.data = data
        self.start_date = datetime.datetime.now() - datetime.timedelta(days=15)
        self.end_date = datetime.datetime.now() + datetime.timedelta(days=15)
        self.__view = Gui(self)
        self.__main_tab = MainTabCtr(self)
        self.__tab_list = []
        self.__view.append_tab(self.__main_tab.view,Gtk.Label(self.__main_tab.title))

        for lom in self.data.get_simple_loms():
            tab_tmp = LomTabCtr(self, lom.lom_id())
            self.__tab_list.append(tab_tmp)
            tab_tmp.view_id = self.__view.append_tab(tab_tmp.view,Gtk.Label(lom.name()))

    def run(self):
        self.__view.run()
        Gtk.main()

    def delete_tab(self, lom):
        for tab in self.__tab_list :
            if tab.lom.lom_id() == lom.lom_id():
                self.__tab_list.remove(tab)
                self.__view.detach_tab(tab)

    def insert_tab(self, lom):
        tab_tmp = LomTabCtr(self,lom.lom_id())
        self.__tab_list.append(tab_tmp)
        tab_tmp.view_id = self.__view.append_tab(tab_tmp.view,Gtk.Label(lom.name()))
        self.__view.show_all()

    def import_csv(self, widget, lom):
        dialog = dialogs.FilegDialogCtr(widget)
        response = dialog.run()

        if response  == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            return

        self.data.from_csv(
            dialog.get_file_name(),
            lom
            )

        for lom_tab in self.__tab_list:
            if lom_tab.lom_id == lom.lom_id():
                for mom in lom.get_moms():
                    lom_tab.mom_store.append([
                        mom.mom_id(),
                        mom.get_value(),
                        mom.cause(),
                        str(mom.time()),
                        False
                    ])


        dialog.destroy()