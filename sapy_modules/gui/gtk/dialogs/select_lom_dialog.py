#
#   File : select_lom_dialog.py
#   Author : stefano prina <stethewwolf@gmail.com>
#

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class select_lom_dialog_view(Gtk.MessageDialog):
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

class select_lom_dialog_controller(object):
    def __init__(self):
        #TODO: only one lom is selected per time, when you selcet one, other
        #       are deselected
        pass

