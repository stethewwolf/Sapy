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
from sapy_modules.gui.gtk.dialogs import Add_Mom_Dialog_View, \
        Del_Mom_Dialog_View, Update_Mom_Dialog_View, No_Item_Selected, \
        Csv_Structure_Display_Message


# -- Buttons

# -- -- Add Mom Button
class Sapy_Add_Mom_Button(Gtk.Button):
    def __init__(self, parent, gtkWindow):
        Gtk.Button.__init__(self)
        self.set_label("Add")
        self.connect("clicked",self.on_button_clicked)
        self.gtkWindow = gtkWindow
        self.lom_ctrl = parent.parent.controller

    def on_button_clicked(self, widget):
        dialog = Add_Mom_Dialog_View(self.gtkWindow)

        if dialog.run() == Gtk.ResponseType.OK:
            new_mom = dialog.get_mom()
            self.lom_ctrl.add_mom(new_mom)

        dialog.destroy()

class Sapy_Del_Mom_Button(Gtk.Button):
    def __init__(self, parent, gtkWindow):
        Gtk.Button.__init__(self)
        self.set_label("Del")
        self.connect("clicked",self.on_button_clicked)
        self.gtkWindow = gtkWindow
        self.lom_ctrl = parent.parent.controller

    def on_button_clicked(self, widget):

        if self.lom_ctrl.has_mom_selected():
            dialog = Del_Mom_Dialog_View(self.gtkWindow)

            if dialog.run() == Gtk.ResponseType.OK:
                self.lom_ctrl.del_mom()

            dialog.destroy()
        else:
            dialog = No_Item_Selected(self.gtkWindow)
            dialog.run()
            dialog.destroy()

class Sapy_Edit_Mom_Button(Gtk.Button):
    def __init__(self, parent, gtkWindow):
        Gtk.Button.__init__(self)
        self.set_label("Edit")
        self.connect("clicked",self.on_button_clicked)
        self.gtkWindow = gtkWindow
        self.lom_ctrl = parent.parent.controller

    def on_button_clicked(self, widget):
        if self.lom_ctrl.has_mom_selected():
            for mom_row in self.lom_ctrl.moms_store:
                if mom_row[0] == True:
                    mom = self.lom_ctrl.lom.get_mom(id=mom_row[1])

                    dialog = Update_Mom_Dialog_View(self.gtkWindow,mom)

                    if dialog.run() == Gtk.ResponseType.OK:
                        dialog.run_update_mom()

                    dialog.destroy()
        else:
            dialog = No_Item_Selected(self.gtkWindow)
            dialog.run()
            dialog.destroy()

        self.lom_ctrl.update_lom_list()

class Sapy_Export_Button(Gtk.Button):
    def __init__(self, parent, gtkWindow):
        Gtk.Button.__init__(self)
        self.set_label("Export")
        self.connect("clicked",self.on_button_clicked)
        self.gtkWindow = gtkWindow
        self.lom_ctrl = parent.parent.controller

    def on_button_clicked(self, widget):
        pass

class Sapy_Import_Button(Gtk.Button):
    def __init__(self, parent, gtkWindow):
        Gtk.Button.__init__(self)
        self.set_label("Import")
        self.connect("clicked",self.on_button_clicked)
        self.gtkWindow = gtkWindow
        self.lom_ctrl = parent.parent.controller

    def on_button_clicked(self, widget):
        dialog = Csv_Structure_Display_Message(self.gtkWindow)
        dialog.run()
        dialog.destroy()

        dialog = Gtk.FileChooserDialog("Select file to import", self.gtkWindow, Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        filter = Gtk.FileFilter()
        filter.set_name("CSV")
        filter.add_pattern("*.csv")
        filter.add_pattern("*.CSV")

        dialog.add_filter(filter)

        if dialog.run() == Gtk.ResponseType.OK:
            self.lom_ctrl.lom.csv_import(dialog.get_file())

        dialog.destroy()

# ----
class Lom_Page_Toolbar(Gtk.ButtonBox):
    def __init__ (self, parent):
        Gtk.ButtonBox.__init__(self)
        self.set_property("expand", False)
        self.gtkWindow = parent.gtkWindow
        self.parent = parent

        self.add(Sapy_Add_Mom_Button(self, self.gtkWindow))

        self.add(Sapy_Del_Mom_Button(self, self.gtkWindow))

        self.add(Sapy_Edit_Mom_Button(self, self.gtkWindow))

        self.add(Sapy_Import_Button(self, self.gtkWindow))

        #self.add(sapy_export_button(self.gtkWindow))



