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
from sapy_modules.sapy import loms

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

        self,view.notebook.append_page(Home_Page(self.view),Gtk.Label("Home"))
        self.update_pages_list()

    def update_pages_list(self):

        for lom in self.loms:
            self.view.notebook.insert_page(Lom_Page(self.view, lom), Gtk.Label(lom.name), 1)
        

