#
#   File : sapy
#   Author : stefano prina <stethewwolf@null.net>
#

from sapy_modules.gui.gtk.main_window_view import main_window_view

class main_window_controller(object):

    def __init__(self):
        self.view = main_window_view()
        

    def run (self):
        self.view.main()
