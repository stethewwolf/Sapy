#
#   File : set_start.py
#   Author : stefano prina <stethewwolf@null.net>
#

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
from sapy_modules.core import SapyConstants
from sapy_modules.commands.command import Command
from sapy_modules.commands.setter.set_end import SetEnd
import sapy_modules.core.values as SapyValues

class SetStart ( Command ):
    short_arg = SapyConstants.COMMANDS.SET_START.SHORT_ARG
    long_arg = SapyConstants.COMMANDS.SET_START.LONG_ARG
    cmd_help = SapyConstants.COMMANDS.SET_START.HELP
    cmd_type = SapyConstants.COMMANDS.SET_START.TYPE
    cmd_action = SapyConstants.COMMANDS.SET_START.ACTION

    def __init__( self, param ):
        super().__init__()
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))
        self.__param = param

    def run( self ):
        self.logger.debug("start")

        SapyValues.set_value( 'start_date', SetEnd.parse_date( self.__param, self.logger ) )

        self.logger.debug("end")