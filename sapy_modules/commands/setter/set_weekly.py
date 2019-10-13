#
#   File : set_weekly.py
#   Author : stefano prina <stethewwolf@null.net>
#

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
from sapy_modules.core import SapyConstants
from sapy_modules.commands.command import Command
import sapy_modules.core.values as SapyValues

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