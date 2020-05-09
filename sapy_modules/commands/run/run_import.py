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
import sapy_modules.sapy.mom as moms
import sapy_modules.commands.setter.set_end as se
import csv, pathlib
import sapy_modules.sapy.lom as loms
import sapy_modules.core.values as SapyValues

class RunImport ( Command ):
    short_arg = SapyConstants.COMMANDS.RUN_IMPORT.SHORT_ARG
    long_arg = SapyConstants.COMMANDS.RUN_IMPORT.LONG_ARG
    cmd_help = SapyConstants.COMMANDS.RUN_IMPORT.HELP
    cmd_type = SapyConstants.COMMANDS.RUN_IMPORT.TYPE
    cmd_action = SapyConstants.COMMANDS.RUN_IMPORT.ACTION

    def __init__( self, param ):
        super().__init__()
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))
        self.file = pathlib.Path( param )


    def run( self ):
        self.logger.debug("start")

        l = SapyValues.get_value('lom') 

        mlist = []
        with self.file.open('r') as data_file:
            data = csv.DictReader( data_file, fieldnames=[
                'date',
                'cause',
                'value'
            ] )

            for raw in data:
                
                
                
                mlist.append( moms.Mom( 
                    day = se.parse_date( raw['date'], self.logger ).day,
                    month = se.parse_date( raw['date'], self.logger ).month,
                    year = se.parse_date( raw['date'], self.logger ).year,
                    cause = raw['cause'],
                    value = float( raw['value'] )
                 ) ) 

        l.add(mlist)

        self.logger.debug("end")