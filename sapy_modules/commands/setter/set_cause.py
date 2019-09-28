#
#   File : set_cause.py
#   Author : stefano prina <stethewwolf@null.net>
#

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
from sapy_modules.core import SapyConstants
from sapy_modules.commands.command import Command
import sapy_modules.core.values as SapyValues

class SetCause ( Command ):
    short_arg = SapyConstants.COMMANDS.SET_CAUSE.SHORT_ARG
    long_arg = SapyConstants.COMMANDS.SET_CAUSE.LONG_ARG
    cmd_help = SapyConstants.COMMANDS.SET_CAUSE.HELP
    cmd_type = SapyConstants.COMMANDS.SET_CAUSE.TYPE
    cmd_action = SapyConstants.COMMANDS.SET_CAUSE.ACTION

    def __init__( self, param ):
        super().__init__()
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))
        self.__param = param

    def run( self ):
        self.logger.debug("start")

        SapyValues.set_value( 'cause', self.__param )

        self.logger.debug("end")