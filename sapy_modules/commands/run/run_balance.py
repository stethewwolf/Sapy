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
import sapy_modules.core.values as SapyValues
from sapy_modules.commands.command import Command
import datetime
import sapy_modules.sapy.lom as loms

class RunBalance ( Command ):
    short_arg = "b"
    long_arg = "balance"
    cmd_help = "print the actual balance of the list"
    cmd_type = None
    cmd_action = "store_true"

    def __init__( self, param ):
        super().__init__()
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))

    def run( self ):
        self.logger.debug("start")

        l = SapyValues.get_value('lom') 

        ed = SapyValues.get_value('end_date')
        
        print('------------------------------')
        print(l.name)
        print('------------------------------')
        print(' balance : ' + str( l.balance(end_date=ed)) )
        print('------------------------------')
        self.logger.debug("end")