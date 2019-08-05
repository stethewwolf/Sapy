
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Handlers:
    def onDestroy(self, *args):
        Gtk.main_quit()
        exit(0)
