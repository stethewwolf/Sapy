import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import sapy_modules.gui.gtk.handlers as myHandlers

builder = None

def init():
    global builder

    if not builder :
        builder = Gtk.Builder()
        builder.add_from_file("sapy_modules/gui/glade/sapy.glade")
        builder.connect_signals(myHandlers.Handlers())

def get_object(object_name):
    global builder
    return builder.get_object(object_name)
