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


import argparse
import importlib
from sapy_modules.core import LoggerFactory
from sapy_modules.core import SapyConstants
from sapy_modules.commands.run import *
from sapy_modules.commands.setter import *
from sapy_modules.commands.tasks import *

class CommandLine_Parser( object ):
    def __init__( self ):
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))

        self.parser = argparse.ArgumentParser( prog=SapyConstants.APP.NAME, description=SapyConstants.APP.DESCRIPTION )

        self.rcl = [ 
            RunAdd, 
            RunGraph,
            RunGui,
            RunImport,
            RunList,
            RunRemove,
            RunVersion,
            RunBalance
            ]

        self.scl = [ 
            SetDaily,
            SetEnd,
            SetId,
            SetMonthly,
            SetLom,
            SetStart,
            SetValue,
            SetWeekly,
            SetCause,
            SetDate,
            SetName
            ]

        self.tcl = [ 
            NewYear,
            NewMonth,
            EndWeek,
            EndMonth
        ]
        
        for cmd in self.rcl + self.scl + self.tcl:
            if cmd.short_arg:
                if cmd.cmd_type:
                    self.parser.add_argument(  
                        "--"+cmd.long_arg,
                        "-"+cmd.short_arg,
                        type = cmd.cmd_type,
                        help = cmd.cmd_help
                    )
                else:
                    self.parser.add_argument(  
                        "--"+cmd.long_arg,
                        "-"+cmd.short_arg,
                        action = cmd.cmd_action,
                        help = cmd.cmd_help
                    )
            elif cmd.long_arg:
                if cmd.cmd_type:
                    self.parser.add_argument(  
                        "--"+cmd.long_arg,
                        type = cmd.cmd_type,
                        help = cmd.cmd_help
                    )
                else:
                    self.parser.add_argument(  
                        "--"+cmd.long_arg,
                        action = cmd.cmd_action,
                        help = cmd.cmd_help
                    )

    def parse( self ):
        command_list = []
        
        self.logger.debug('add set_env command')
        command_list.append( SetEnv() )

        self.logger.debug('parse starts')

        args = self.parser.parse_args()

        for cmd in self.scl:
            if getattr( args, cmd.long_arg.replace("-","_") ) :
                self.logger.debug("passed option --" + cmd.long_arg)
                command_list.append( cmd( getattr( args, cmd.long_arg.replace("-","_") ) ) )

        count = 0
        for cmd in self.rcl:
            if getattr( args, cmd.long_arg.replace("-","_") ) :
                self.logger.debug("passed option --" + cmd.long_arg)
                command_list.append( cmd( getattr( args, cmd.long_arg.replace("-","_") ) ) )
                count += 1

            if count > 0 :
                self.logger.warn("it is possible use only one task")
                break

        count = 0
        for cmd in self.tcl:
            if getattr( args, cmd.long_arg.replace("-","_") ) :
                self.logger.debug("passed option --" + cmd.long_arg)
                command_list.append( cmd( getattr( args, cmd.long_arg.replace("-","_") ) ) )
                count += 1

            if count > 1 :
                self.logger.warn("it is possible use only one task")
                break


        self.logger.debug('parse ends')
        
        return command_list
