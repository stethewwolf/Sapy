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
#

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Select_Lom_Dialog_View(Gtk.MessageDialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Select List", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(150, 100)

        self.parent = parent

        box = self.get_content_area()

        self.lom_button_box = Gtk.VButtonBox()

        box.pack_start( self.lom_button_box, False, False, 0 )

        self.controller = Select_Lom_Dialog_Controller(self)

        self.show_all()

    def get_selected_item(self):
        ret = ""
        
        for btn in self.lom_button_box.get_children():
            if btn.get_active():
                ret = btn.get_label()
                break

        return ret


class Select_Lom_Dialog_Controller(object):
    def __init__(self, view):
        self.view = view
        for lom in view.parent.controller.lom_list:
            btn = Lom_List_Item(lom, view.lom_button_box)
            view.lom_button_box.add(btn)
            if lom.id == view.parent.controller.lom.id:
                btn.set_active(True)
            

class Lom_List_Item(Gtk.ToggleButton):
    def __init__(self, lom, button_box):
        Gtk.ToggleButton.__init__(self, label=lom.name)
        self.button_box = button_box
        self.connect("clicked", self.on_button_clicked)

    def on_button_clicked(self, button):
        for btn in self.button_box.get_children():
            if btn.get_active() and btn.get_label() != self.get_label() :
                print("active")
                self.set_active(False)
            else:
                print("not active")

        
        #self.do_toggled()
        #self.set_active(True)
        
