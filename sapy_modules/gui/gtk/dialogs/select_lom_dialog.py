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

        box = self.get_content_area()

        label = Gtk.Label("select one list")

        box.pack_start( label, True, True, 0 )

        self.lom_list = []

        for spr in  parent.controller.lom_list:
            button = Gtk.CheckButton(label=spr.name)
            self.lom_list.append(button)
            box.pack_start( button, True, True, 0 )

        self.show_all()

    def get_selected_item(self):
        ret = ""
        for btn in self.lom_list:
            if btn.get_active():
                ret = btn.get_label()
                break
        return ret

class Select_Lom_Dialog_Controller(object):
    def __init__(self):
        #TODO: only one lom is selected per time, when you selcet one, other
        #       are deselected
        pass

