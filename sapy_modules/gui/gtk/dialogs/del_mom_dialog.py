#
#   File : add_mom_dialog.py
#   Author : stefano prina <stethewwolf@gmail.com>
#


import gi, datetime
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import sapy_modules.sapy.mom as moms


class del_mom_dialog_view(Gtk.MessageDialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "add new mom", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(150, 100)

        box = self.get_content_area()

        label = Gtk.Label("Are you shure to delete selected movements of money")

        box.add(label)
        self.show_all()

class del_mom_dialog_controller(object):
    def __init__(self):
        pass 
