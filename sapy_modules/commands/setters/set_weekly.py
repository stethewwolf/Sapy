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

from sapy_modules.utils import loggers as LoggerFactory
from sapy_modules.utils import config as SingleConfig
from sapy_modules.utils import constants as SapyConstants
from sapy_modules.utils import values as SapyValues
from sapy_modules.commands.command import Command

class SetWeekly ( Command ):
    short_arg = SapyConstants.COMMANDS.SET_WEEKLY.SHORT_ARG
    long_arg = SapyConstants.COMMANDS.SET_WEEKLY.LONG_ARG
    cmd_help = SapyConstants.COMMANDS.SET_WEEKLY.HELP
    cmd_type = SapyConstants.COMMANDS.SET_WEEKLY.TYPE
    cmd_action = SapyConstants.COMMANDS.SET_WEEKLY.ACTION

    def __init__( self, param = None):
        super().__init__()
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))

    def run( self ):
        self.logger.debug("start")

        SapyValues.set_value( 'frequency', SapyConstants.FREQUENCY.WEEKLY )

        self.logger.debug("end")