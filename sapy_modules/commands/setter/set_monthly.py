#
#   File : set_expected.py
#   Author : stefano prina <stethewwolf@null.net>
#

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
from sapy_modules.core import SapyConstants
from sapy_modules.commands.command import Command
import sapy_modules.core.values as SapyValues

class SetMonthly ( Command ):
    short_arg = SapyConstants.COMMANDS.SET_MONTHLY.SHORT_ARG
    long_arg = SapyConstants.COMMANDS.SET_MONTHLY.LONG_ARG
    cmd_help = SapyConstants.COMMANDS.SET_MONTHLY.HELP
    cmd_type = SapyConstants.COMMANDS.SET_MONTHLY.TYPE
    cmd_action = SapyConstants.COMMANDS.SET_MONTHLY.ACTION

    def __init__( self, param ):
        super().__init__()
        self.logger = LoggerFactory.getLogger( str( self.__class__ ) )

    def run( self ):
        self.logger.debug("start")

        SapyValues.set_value( 'frequency', SapyConstants.FREQUENCY.MONTHLY )

        self.logger.debug("end")