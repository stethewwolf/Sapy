# Sapy
# Copyright (C) 2018 stefano prina <stethewwolf@null.net> <stethewwolf@gmail.com>
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
from sapy_modules.gui.gtk.dialogs import Select_Lom_Dialog_View, Add_Mom_Dialog_View, Del_Mom_Dialog_View, Update_Mom_Dialog_View, Plot_Graph_Dialog_View

from matplotlib.figure import Figure

# -- Buttons
# -- -- Select Lom Button
class Sapy_Select_Lom_Button(Gtk.Button):
    def __init__(self, gtkWindow):
        Gtk.Button.__init__(self)
        self.set_label("List")
        self.connect("clicked",self.on_button_clicked)
        self.gtkWindow = gtkWindow

    def on_button_clicked(self, widget):
        dialog = Select_Lom_Dialog_View(self.gtkWindow)

        if dialog.run() == Gtk.ResponseType.OK:
            lom = dialog.get_selected_item()
            if lom: 
                self.gtkWindow.controller.set_list(lom)

        dialog.destroy()

# -- -- Add Mom Button
class Sapy_Add_Mom_Button(Gtk.Button):
    def __init__(self, gtkWindow):
        Gtk.Button.__init__(self)
        self.set_label("Add")
        self.connect("clicked",self.on_button_clicked)
        self.gtkWindow = gtkWindow

    def on_button_clicked(self, widget):
        dialog = Add_Mom_Dialog_View(self.gtkWindow)

        if dialog.run() == Gtk.ResponseType.OK:
            new_mom = dialog.get_mom()
            self.gtkWindow.controller.add_mom(new_mom)

        dialog.destroy()

class Sapy_Del_Mom_Button(Gtk.Button):
    def __init__(self, gtkWindow):
        Gtk.Button.__init__(self)
        self.set_label("Del")
        self.connect("clicked",self.on_button_clicked)
        self.gtkWindow = gtkWindow

    def on_button_clicked(self, widget):
        dialog = Del_Mom_Dialog_View(self.gtkWindow)

        if dialog.run() == Gtk.ResponseType.OK:
            self.gtkWindow.controller.del_mom()

        dialog.destroy()

class Sapy_Edit_Mom_Button(Gtk.Button):
    def __init__(self, gtkWindow):
        Gtk.Button.__init__(self)
        self.set_label("Edit")
        self.connect("clicked",self.on_button_clicked)
        self.gtkWindow = gtkWindow

    def on_button_clicked(self, widget):
        for mom_row in self.gtkWindow.controller.moms_store:
            if mom_row[4] == True:
                mom = self.gtkWindow.controller.lom.get_mom(id=mom_row[0])

                dialog = Update_Mom_Dialog_View(self.gtkWindow,mom)
                
                if dialog.run() == Gtk.ResponseType.OK:
                    dialog.run_update_mom()
        
                dialog.destroy()
        
        self.gtkWindow.controller.rebuild_list()

class Sapy_Graph_Button(Gtk.Button):
    def __init__(self, gtkWindow):
        Gtk.Button.__init__(self)
        self.set_label("Graph")
        self.connect("clicked",self.on_button_clicked)
        self.gtkWindow = gtkWindow

    def on_button_clicked(self, widget):
        dialog = Plot_Graph_Dialog_View(self.gtkWindow)
        dialog.run()
        dialog.destroy()
        pass

class Sapy_Export_Button(Gtk.Button):
    def __init__(self, gtkWindow):
        Gtk.Button.__init__(self)
        self.set_label("Export")
        self.connect("clicked",self.on_button_clicked)
        self.gtkWindow = gtkWindow

    def on_button_clicked(self, widget):
        pass

class Sapy_Import_Button(Gtk.Button):
    def __init__(self, gtkWindow):
        Gtk.Button.__init__(self)
        self.set_label("Import")
        self.connect("clicked",self.on_button_clicked)
        self.gtkWindow = gtkWindow

    def on_button_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Select file to import", self.gtkWindow, Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        if dialog.run() == Gtk.ResponseType.OK:
            self.gtkWindow.controller.lom.csv_import(dialog.get_file())
        
        dialog.destroy()

# ----
class Sapy_Main_Toolbar(Gtk.ButtonBox):
    def __init__ (self, window):
        Gtk.ButtonBox.__init__(self)
        self.gtkWindow = window
        self.set_property("expand", False)
        print(self.get_property("expand"))

        self.add(Sapy_Select_Lom_Button(self.gtkWindow))

        self.add(Sapy_Add_Mom_Button(self.gtkWindow))

        self.add(Sapy_Del_Mom_Button(self.gtkWindow))

        self.add(Sapy_Edit_Mom_Button(self.gtkWindow))

        self.add(Sapy_Graph_Button(self.gtkWindow))

        self.add(Sapy_Import_Button(self.gtkWindow))

        #self.add(sapy_export_button(self.gtkWindow))



