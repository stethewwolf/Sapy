#
#   File : sapy
#   Author : stefano prina <stethewwolf@null.net>
#

from sapy_modules.gui.gtk.main_window_view import main_window_view
import sapy_modules.sapy.lom as loms

class main_window_controller(object):

    def __init__(self):
        self.lom_list = loms.get_loms()
        self.view = main_window_view(self)

    def run (self):
        self.view.main()
