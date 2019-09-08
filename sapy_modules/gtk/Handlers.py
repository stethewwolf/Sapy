
#import gi
#gi.require_version('Gtk', '3.0')
#from gi.repository import Gtk
from sapy_modules.core import LoggerFactory

class Handlers:
    def onDestroy(self, *args):
        LoggerFactory.getLogger( str( self.__class__ ) ).info("onDestroy Called")
        #Gtk.main_quit()
        exit(0)

