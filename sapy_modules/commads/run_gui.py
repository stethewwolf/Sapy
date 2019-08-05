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

import sapy_modules.config as SingleConfig
import sapy_modules.mlogger as loggerFactory
import sapy_modules.gtk.Handlers as myHandlers
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class RunGui( object ):
    def __init__( self ):
        self.cfg = SingleConfig.getConfig()
        self.logger = loggerFactory.getLogger( str( self.__class__ ))

    def run( self ):
        builder = Gtk.Builder()
        builder.add_from_file("/home/stethewwolf/Progetti/Sapy/glade/sapy.glade")
        builder.connect_signals( myHandlers.Handlers())

        window = builder.get_object("window1")
        window.show_all()
        
        

        Gtk.main()
