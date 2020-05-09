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

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
from sapy_modules.core import SapyConstants
from sapy_modules.commands.command import Command

class RunVersion ( Command ):
    short_arg = SapyConstants.COMMANDS.RUN_VERSION.SHORT_ARG
    long_arg = SapyConstants.COMMANDS.RUN_VERSION.LONG_ARG
    cmd_help = SapyConstants.COMMANDS.RUN_VERSION.HELP
    cmd_type = SapyConstants.COMMANDS.RUN_VERSION.TYPE
    cmd_action = SapyConstants.COMMANDS.RUN_VERSION.ACTION

    def __init__( self, param ):
        super().__init__()
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))

    def run( self ):
        self.logger.debug("start")

        print(SapyConstants.APP.NAME + " - " + SapyConstants.APP.VERSION )
        print("\t" + SapyConstants.APP.AUTHORS )

        self.logger.debug("end")