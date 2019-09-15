#
#   File : set_expecetd.py
#   Author : stefano prina <stethewwolf@null.net>
#

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
from sapy_modules.core import SapyConstants
from sapy_modules.commands.command import Command
import sapy_modules.core.values as SapyValues

class SetExpected ( Command ):
    short_arg = SapyConstants.COMMANDS.SET_EXPECTED.SHORT_ARG
    long_arg = SapyConstants.COMMANDS.SET_EXPECTED.LONG_ARG
    cmd_help = SapyConstants.COMMANDS.SET_EXPECTED.HELP
    cmd_type = SapyConstants.COMMANDS.SET_EXPECTED.TYPE
    cmd_action = SapyConstants.COMMANDS.SET_EXPECTED.ACTION

    def __init__( self, param ):
        super().__init__( )
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))

    def run( self ):
        self.logger.debug("start")

        SapyValues.set_value( 'lom', SapyConstants.LOMS.EXPCTD )

        self.logger.debug("end")