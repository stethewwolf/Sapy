#!/usr/bin/env python

from datamgr import DataMgr
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

_app_title="sapy"

class main_window(Gtk.Window):
    def __init__ (self, data_mgr):
        self=Gtk.Window()
        self.data_mgr=data_mgr
        self.connect("delete-event", Gtk.main_quit)

    def run(self):
        #self.show_all()
        Gtk.main()

if __name__ == "__main__":
    win = main_window(DataMgr("test.json"))
    Gtk.main()
    Gtk.gtk_widget_show()


#class Handlers():
#    def __init__(self,builder,data):
#        self.builder=builder
#        self.data=data
#
#    def onDeleteWindow(self, *args):
#        gtk.main_quit(*args)
#
#    def onButtonPressed(self, button):
#        print("button pressed")
#
#    def gtk_filedialog_show(self, *args):
#        chooser = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_OPEN,buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
#        response = chooser.run()
#        if response == gtk.RESPONSE_OK:
#            print chooser.get_filename(), 'selected'
#        elif response == gtk.RESPONSE_CANCEL:
#            print 'Closed, no files selected'
#
#        self.data.load_json(chooser.get_filename() )
#
#        chooser.destroy()
#
#