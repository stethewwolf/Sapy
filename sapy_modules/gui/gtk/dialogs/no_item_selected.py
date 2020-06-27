# Sapy
# Copyright (C) 2018 stefano prina <stethewwolf@null.net> <stethewwolf@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import gi, datetime
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class No_Item_Selected(Gtk.MessageDialog):
    def __init__(self, parent):
        Gtk.MessageDialog.__init__(
                self,
                parent,
                0,
                Gtk.MessageType.INFO,
                Gtk.ButtonsType.OK,
                "No Item Selected",
               )

        self.set_default_size(150, 100)

        self.format_secondary_text(
            "Before perform this action select an item in movements list"
        )

        self.show_all()