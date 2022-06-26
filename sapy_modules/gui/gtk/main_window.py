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
from sapy_modules.gui.gtk.pages import Home_Page, Lom_Page
from sapy_modules.core import loms

class Main_Window_View(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.show_all()
        self.connect("destroy", Gtk.main_quit)

        # main window features
        self.tite = "Sapy"
        self.resize(1000, 800)

        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        self.controller = Main_Window_Controller(self)

    def main(self):
        self.show_all()
        Gtk.main()


class Main_Window_Controller(object):
    def __init__(self, view):
        self.view = view
        self.loms = loms.get_loms()
        self.pages_list = dict()

        self.home_page = Home_Page(self.view)

        # gen pages list
        self.pages_list['Home'] = self.home_page

        for lom in self.loms:
            self.pages_list[lom.name] = Lom_Page(self.view, lom, \
                                                 self.home_page.controller.update_plot)

        for page_name in self.pages_list:
            self.view.notebook.append_page(self.pages_list[page_name],Gtk.Label(page_name))

    def add_lom_page(self,lom):
        self.pages_list[lom.name] = Lom_Page(self.view, lom, self.home_page.controller.update_plot)
        self.view.notebook.append_page(self.pages_list[lom.name],Gtk.Label(lom.name))
        self.view.notebook.show_all()

    def update_lom_page_name(self, old_name, new_name):
        lom_page = self.pages_list[old_name]
        self.view.notebook.set_tab_label_text(lom_page,new_name)
        self.pages_list[new_name] = self.pages_list[old_name]
        del self.pages_list[old_name]

    def remove_lom_page(self, lom_name):
       lom_page = self.pages_list[lom_name]
       page_idx = self.view.notebook.page_num(lom_page)
       self.view.notebook.remove_page(page_idx)
       del self.pages_list[lom_name]






