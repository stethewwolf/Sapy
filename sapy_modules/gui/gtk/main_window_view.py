#
#   File : sapy
#   Author : stefano prina <stethewwolf@null.net>
#

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import sapy_modules.gui.gtk.main_window_toolbar as tlb

class main_window_view(Gtk.Window):

    def __init__(self, controller):
        Gtk.Window.__init__(self)
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        self.controller = controller

        # main window features
        self.tite = "Sapy"
        self.resize(400, 600)

        # main container
        self.main_listbox = Gtk.ListBox()

        # menu button row
        row = Gtk.ListBoxRow()

        row.add(tlb.sapy_main_toolbar(self))

        self.main_listbox.add(row)

        # calendar row
        row = Gtk.ListBoxRow()
        self.calendar = Gtk.Calendar()
        row.add(self.calendar)

        self.main_listbox.add(row)

        # lom panes row
        row = Gtk.ListBoxRow()
        store = Gtk.ListStore(str, str, float)
        self.tree = Gtk.TreeView(store)
        row.add(self.tree)

        title = Gtk.CellRendererText()
        author = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Title and Author") 
        column.pack_start(title, True)
        column.pack_start(author, True)
        
        column.add_attribute(title, "text", 0)
        column.add_attribute(author, "text", 1)

        self.tree.append_column(column)

        self.main_listbox.add(row)

        self.add(self.main_listbox)

    def main(self):
        self.show_all()
        Gtk.main()
    
        
