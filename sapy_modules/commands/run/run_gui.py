#   Author : stefano prina
#
# MIT License
#
# Copyright (c) 2017 Stefano Prina <stethewwolf@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without sestriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#     The above copyright notice and this permission notice shall be included in all
#     copies or substantial portions of the Software.
#
#     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#     IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#     FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#     AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#     LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#     OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#     SOFTWARE.

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
from sapy_modules.core import SapyConstants
from sapy_modules.commands.command import Command
import sapy_modules.gtk.Handlers as myHandlers
# import gi
# gi.require_version('Gtk', '3.0')
# from gi.repository import Gtk

class RunGui( Command ):
    short_arg = SapyConstants.COMMANDS.RUN_GUI.SHORT_ARG
    long_arg = SapyConstants.COMMANDS.RUN_GUI.LONG_ARG
    cmd_help = SapyConstants.COMMANDS.RUN_GUI.HELP
    cmd_type = SapyConstants.COMMANDS.RUN_GUI.TYPE
    cmd_action = SapyConstants.COMMANDS.RUN_GUI.ACTION

    def __init__( self, param ):
        super().__init__()
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))

    def run( self ):
        self.logger.debug("start")

        self.logger.warn("not implemented")

        self.logger.debug("end")
 #       builder = Gtk.Builder()
 #       builder.add_from_file("glade/sapy.glade")
 #       builder.connect_signals( myHandlers.Handlers())

 #       window = builder.get_object("main_window")
 #       window.show_all()

 #       ins_store = Gtk.ListStore(str, float)

 #       in_list = builder.get_object("IncomeListView")


 #       Gtk.main()