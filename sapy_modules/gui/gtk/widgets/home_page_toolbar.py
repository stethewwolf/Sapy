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
from sapy_modules.gui.gtk.dialogs import No_Item_Selected, \
        Csv_Structure_Display_Message, Add_Lom_Dialog_View, \
        Del_Lom_Dialog_View, Update_Lom_Dialog_View
import sapy_modules.sapy.lom as loms

# -- Buttons

# -- -- Add Mom Button
class Sapy_Add_Lom_Button(Gtk.Button):
    def __init__(self, parent, gtkWindow):
        Gtk.Button.__init__(self)
        self.set_label("Add")
        self.connect("clicked",self.on_button_clicked)
        self.gtkWindow = gtkWindow
        self.home_ctrl = parent.parent.controller

    def on_button_clicked(self, widget):
        dialog = Add_Lom_Dialog_View(self.gtkWindow)

        if dialog.run() == Gtk.ResponseType.OK:
            new_lom = dialog.controller.get_lom()
            self.home_ctrl.add_lom_tab(new_lom)
            self.home_ctrl.update_loms()

        dialog.destroy()

class Sapy_Del_Lom_Button(Gtk.Button):
    def __init__(self, parent, gtkWindow):
        Gtk.Button.__init__(self)
        self.set_label("Del")
        self.connect("clicked",self.on_button_clicked)
        self.gtkWindow = gtkWindow
        self.home_ctrl = parent.parent.controller

    def on_button_clicked(self, widget):
        if self.home_ctrl.has_lom_selected():
            dialog = Del_Lom_Dialog_View(self.gtkWindow)

            if dialog.run() == Gtk.ResponseType.OK:
                self.home_ctrl.del_lom()

            dialog.destroy()
        else:
            dialog = No_Item_Selected(self.gtkWindow)
            dialog.run()
            dialog.destroy()

class Sapy_Edit_Lom_Button(Gtk.Button):
    def __init__(self, parent, gtkWindow):
        Gtk.Button.__init__(self)
        self.set_label("Edit")
        self.connect("clicked",self.on_button_clicked)
        self.gtkWindow = gtkWindow
        self.home_ctrl = parent.parent.controller

    def on_button_clicked(self, widget):
        if self.home_ctrl.has_lom_selected():
            for lom_row in self.home_ctrl.lists_store:
                if lom_row[0] == True:
                    lom = loms.get_lom(id=lom_row[1])

                    dialog = Update_Lom_Dialog_View(self.gtkWindow,lom)

                    if dialog.run() == Gtk.ResponseType.OK:
                        dialog.controller.run_update_lom()

                    dialog.destroy()
        else:
            dialog = No_Item_Selected(self.gtkWindow)
            dialog.run()
            dialog.destroy()
        self.home_ctrl.update_loms()
        self.home_ctrl.update_plot()

# ----
class Home_Page_Toolbar(Gtk.ButtonBox):
    def __init__ (self, parent):
        Gtk.ButtonBox.__init__(self)
        self.set_property("expand", False)
        self.gtkWindow = parent.gtkWindow
        self.parent = parent

        self.add(Sapy_Add_Lom_Button(self, self.gtkWindow))
        self.add(Sapy_Del_Lom_Button(self, self.gtkWindow))
        self.add(Sapy_Edit_Lom_Button(self, self.gtkWindow))

