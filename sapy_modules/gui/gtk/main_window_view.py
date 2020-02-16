#
#   File : sapy
#   Author : stefano prina <stethewwolf@null.net>
#

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class main_window_view(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)
        self.connect("destroy", Gtk.main_quit)
        self.show_all()

    def main(self):
        Gtk.main()
    
        
