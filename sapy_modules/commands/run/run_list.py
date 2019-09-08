#
#   File : run_graph.py
#   Author : stefano prina <stethewwolf@null.net>
#

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
from sapy_modules.core import SapyConstants
from sapy_modules.commands.command import Command

class RunList ( Command ):
    short_arg = SapyConstants.COMMANDS.RUN_LIST.SHORT_ARG
    long_arg = SapyConstants.COMMANDS.RUN_LIST.LONG_ARG
    cmd_help = SapyConstants.COMMANDS.RUN_LIST.HELP
    cmd_type = SapyConstants.COMMANDS.RUN_LIST.TYPE
    cmd_action = SapyConstants.COMMANDS.RUN_LIST.ACTION

    def __init__( self, param ):
        super().__init__()
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))

    def run( self ):
        self.logger.debug("start")

        self.logger.warn("not implemented")

        self.logger.debug("end")