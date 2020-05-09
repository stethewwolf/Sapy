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

from sapy_modules.core import LoggerFactory
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sapy_modules.commands.run.run_list import RunList

class Handlers:
    def onDestroy(self, *args):
        LoggerFactory.getLogger(str( self.__class__ ) ).debug("onDestroy Called")
        Gtk.main_quit()
        exit(0)

    def open_lom_list(self, *args):
        LoggerFactory.getLogger(str( self.__class__ ) ).debug("open_lom_list Called")
        builder = Gtk.Builder()
        builder.add_from_file("sapy_modules/gui/glade/sapy.glade")

        lom_store = Gtk.ListStore(int,str)

        for l in RunList('lom').list_lom():
            lom_store.append([l.id, l.name])

        lom_tree_view = Gtk.TreeView(lom_store)
        lom_tree_view.append_column( Gtk.TreeViewColumn("Id", Gtk.CellRendererText(), text=0))
        lom_tree_view.append_column( Gtk.TreeViewColumn("Name", Gtk.CellRendererText(), text=1))
        lom_tree_view.append_column( Gtk.TreeViewColumn("Seleceted", Gtk.CellRendererToggle(), text=1))
        
        lomListBox = builder.get_object("LomListBox")

        lomListBox.pack_start(lom_tree_view, True, True, 1)
        
        dialog = builder.get_object("gtkdialog_chooe_list")
        dialog.show_all() 
        #dialog.run()

    def close_lom_list(self, *args):
        LoggerFactory.getLogger(str( self.__class__ ) ).debug("close_lom_list Called")
        builder = Gtk.Builder()
        builder.add_from_file("sapy_modules/gui/glade/sapy.glade")

        dialog = builder.get_object("gtkdialog_chooe_list")
        dialog.hide()
        #dialog.destroy()


