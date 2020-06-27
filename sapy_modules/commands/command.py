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
#

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
from sapy_modules.core import SapyConstants

class Command (object):
    short_arg = SapyConstants.COMMANDS.CMD.SHORT_ARG
    long_arg = SapyConstants.COMMANDS.CMD.LONG_ARG
    cmd_help = SapyConstants.COMMANDS.CMD.HELP
    cmd_type = SapyConstants.COMMANDS.CMD.TYPE
    cmd_action = SapyConstants.COMMANDS.CMD.ACTION

    def __init__( self, param = None ):
        self.cfg = SingleConfig.getConfig()

    def run( self ):
        pass