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


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sapy_modules.sapy import Lom
import matplotlib.colors as mcolors

class Add_Lom_Dialog_View(Gtk.MessageDialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "add new list", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.controller = Add_Lom_Dialog_Controller(self)
        self.set_default_size(150, 100)

        box = self.get_content_area()
        grid = Gtk.Grid()

        name_label = Gtk.Label("Name")
        self.name_entry = Gtk.Entry()
        self.name_entry.set_placeholder_text("name")
        grid.add(name_label)

        grid.attach_next_to(
                self.name_entry,
                name_label,
                Gtk.PositionType.RIGHT,
                1, 1
                )

        color_label = Gtk.Label("Color")
        self.color_combo = Gtk.ComboBox.new_with_model(self.controller.color_store)
        self.color_combo.connect("changed", self.controller.on_color_changed)
        renderer_text = Gtk.CellRendererText()
        self.color_combo.pack_start(renderer_text, True)
        self.color_combo.add_attribute(renderer_text, "text", 0)

        grid.attach_next_to(
                color_label,
                name_label,
                Gtk.PositionType.BOTTOM,
                1, 1
                )

        grid.attach_next_to(
                self.color_combo,
                color_label,
                Gtk.PositionType.RIGHT,
                1, 1
                )

        box.add(grid)
        self.show_all()

class Add_Lom_Dialog_Controller(object):
    def __init__(self, view):
        self.view = view
        self.color_store = Gtk.ListStore(str)
        colors = mcolors.CSS4_COLORS.keys()

        self.color = 'black'

        for color in colors:
            self.color_store.append([color])

    def on_color_changed(self, combo):
        c_iter = combo.get_active_iter()
        if c_iter is not None:
            model = combo.get_model()
            self.color = model[c_iter][0]

    def get_lom(self):
        l_name = self.view.name_entry.get_text()
        l_color = self.color
        l_visible = False
        return Lom(name=l_name,color=l_color,visible=l_visible)


