# Sapy
# Copyright (C) 2018 stefano prina <stefano-prina@outlook.it> <stethewwolf@gmail.com>
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

__all__ = [ 'Main_Window_Controller', 'Sapy_Main_Toolbar', 'Main_Window_View', 'dialogs']

# deprecated to keep older scripts who import this from breaking
from sapy_modules.gui.gtk.main_window_view import Main_Window_View
from sapy_modules.gui.gtk.main_window_toolbar import Sapy_Main_Toolbar
from sapy_modules.gui.gtk.main_window_controller import Main_Window_Controller
