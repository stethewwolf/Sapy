#
#   File : set_db.py
#   Author : stefano prina <stethewwolf@null.net>
#

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
from sapy_modules.core import SapyConstants
from sapy_modules.commands.command import Command

class SetDb ( Command ):
    short_arg = SapyConstants.COMMANDS.SET_DB.SHORT_ARG
    long_arg = SapyConstants.COMMANDS.SET_DB.LONG_ARG
    cmd_help = SapyConstants.COMMANDS.SET_DB.HELP
    cmd_type = SapyConstants.COMMANDS.SET_DB.TYPE
    cmd_action = SapyConstants.COMMANDS.SET_DB.ACTION

    def __init__( self ):
        super().__init__( )
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))

    def run( self ):
        self.logger.debug("start")

        self.logger.warn("not implemented")

        self.logger.debug("end")